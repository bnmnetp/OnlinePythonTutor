from flask import Flask, request, Response, make_response
from flask.json import jsonify
import json
import subprocess

# at some point maybe worry about Access-Control-Allow-Origin: *
# but for now this isn't an issue for command line usage.

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello Class!"


# docker run -m 512M --rm --user=netuser --net=none --cap-drop all pgbovine/cokapi-java:v1 /tmp/run-java-backend.sh '{"usercode": "public class Test { public static void main(String[] args) { int x=42; x+=1; x+=1; x+=1;} }", "options": {}, "args": [], "stdin": ""}'
@app.route("/tracejava", methods=["POST"])
def tracejava():
    #code = request.args["src"]
    code = request.form.get("src")
    docker_args = [
        "docker",
        "run",
        "-m",
        "512M",
        "--rm",
        "--user=netuser",
        "--net=none",
        "--cap-drop",
        "all",
        "pgbovine/cokapi-java:v1",
        "/tmp/run-java-backend.sh",
    ]
    runspec = {}
    runspec["usercode"] = code
    runspec["options"] = {}
    runspec["args"] = []
    runspec["stdin"] = ""
    docker_args.append(json.dumps(runspec))
    res = subprocess.run(docker_args, capture_output=True)
    resp = make_response(res.stdout)
    resp.headers['Content-type'] = 'application/json'
    return resp

# docker run -t -i --rm --user=netuser --net=none --cap-drop all pgbovine/opt-cpp-backend:v1 python /tmp/opt-cpp-backend/run_cpp_backend.py "int main() {int x=12345;}" c
@app.route("/tracec", methods=["POST"])
def tracec():
    code = request.form.get("src")
    docker_args = [
        "docker",
        "run",
        "-t",
        "-i",
        "--rm",
        "--user=netuser",
        "--net=none",
        "--cap-drop",
        "all",
        "pgbovine/opt-cpp-backend:v1",
        "python",
        "/tmp/opt-cpp-backend/run_cpp_backend.py",
        code,
        "c"
    ]
    res = subprocess.run(docker_args, capture_output=True)
    resp = make_response(res.stdout)
    resp.headers['Content-type'] = 'application/json'
    return resp



@app.route("/tracecpp", methods=["POST"])
def tracecpp():
    code = request.form.get("src")
    docker_args = [
        "docker",
        "run",
        "-t",
        "-i",
        "--rm",
        "--user=netuser",
        "--net=none",
        "--cap-drop",
        "all",
        "pgbovine/opt-cpp-backend:v1",
        "python",
        "/tmp/opt-cpp-backend/run_cpp_backend.py",
        code,
        "cpp"
    ]
    res = subprocess.run(docker_args, capture_output=True)
    resp = make_response(res.stdout)
    resp.headers['Content-type'] = 'application/json'
    return resp

