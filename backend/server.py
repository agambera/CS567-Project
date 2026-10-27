"""
Simple backend for our agentic AI demo.
"""

import json
import subprocess
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlsplit, parse_qs

PORT = 1234

this_folder = Path(__file__).resolve().parent
website_folder = this_folder.parent / "frontend"
code_folder = this_folder / "SampleCode"
bugs_folder = this_folder / "bugs"


class Server(SimpleHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(website_folder), **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()

    def do_GET(self):
        # split "/code/gradebook.py?level=Low" into the path and the level
        url = urlsplit(self.path)
        path = url.path
        level = parse_qs(url.query).get("level", ["none"])[0]

        if path.startswith("/code/"):
            file_name = path.replace("/code/", "", 1)
            print(f"Session started at level: {level}")
            self.send_code(file_name)
        elif path.startswith("/bugs/"):
            file_name = path.replace("/bugs/", "", 1)
            print(f"Sending bugs for level: {level}")
            self.send_bugs(file_name)
        elif path.startswith("/run/"):
            file_name = path.replace("/run/", "", 1)
            print(f"Running code for level: {level}")
            self.run_code(file_name)
        else:
            super().do_GET()

    def send_code(self, file_name):
        file = (code_folder / file_name).resolve()
        if file.parent != code_folder or file.suffix != ".py" or not file.exists():
            self.send_reply(404, {"error": "Could not find " + file_name})
            return
        self.send_reply(200, {"name": file.name, "code": file.read_text()})

    def send_bugs(self, file_name):
        file = (bugs_folder / file_name).resolve()
        if file.parent != bugs_folder or file.suffix != ".json" or not file.exists():
            self.send_reply(404, {"error": "Could not find " + file_name})
            return
        self.send_reply(200, json.loads(file.read_text()))

    def run_code(self, file_name):
        # actually run the sample code so the agent terminal shows real output
        file = (code_folder / file_name).resolve()
        if file.parent != code_folder or file.suffix != ".py" or not file.exists():
            self.send_reply(404, {"error": "Could not find " + file_name})
            return
        try:
            result = subprocess.run(
                [sys.executable, "-u", file.name],
                cwd=code_folder, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, timeout=10)
            output = result.stdout
            exit_code = result.returncode
        except subprocess.TimeoutExpired:
            output = "Program took too long and was stopped."
            exit_code = "timeout"
        # hide the full folder path so the output looks like it ran in SampleCode
        output = output.replace(str(code_folder) + "/", "")
        self.send_reply(200, {"output": output, "exit_code": exit_code})

    def send_reply(self, status, data):
        reply = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(reply)))
        self.end_headers()
        self.wfile.write(reply)


if __name__ == "__main__":
    print(f"Server running at http://localhost:{PORT}")
    HTTPServer(("localhost", PORT), Server).serve_forever()