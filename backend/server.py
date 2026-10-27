"""
Simple backend for our agentic AI demo.
"""

import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

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
        if self.path.startswith("/code/"):
            file_name = self.path.replace("/code/", "", 1)
            self.send_code(file_name)
        elif self.path.startswith("/bugs/"):
            file_name = self.path.replace("/bugs/", "", 1)
            self.send_bugs(file_name)
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
        file = (bugs_folder / file_name).resolve()
        print(f"Looking for: {file}")
        print(f"Bugs folder: {bugs_folder.resolve()}")
        print(f"File exists: {file.exists()}")

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