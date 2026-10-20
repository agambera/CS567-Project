"""
Simple backend for our agentic AI demo.

It does two things:
  1. Shows the website (everything in the frontend folder)
  2. Sends the code from a file in SampleCode when the page asks for it

How to run it (from the project folder):
    python3 backend/server.py
Then go to http://localhost:8000 in your browser.
"""

import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

PORT = 1234

# Folders this server uses
this_folder = Path(__file__).resolve().parent
website_folder = this_folder.parent / "frontend"
code_folder = this_folder / "SampleCode"
bug_folder = this_folder / "bugs"


class Server(SimpleHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        # Show files from the frontend folder
        super().__init__(*args, directory=str(website_folder), **kwargs)

    def end_headers(self):
        # Lets the page still work if it's opened with Live Server instead
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()

    def do_GET(self):
        # The page asks for code by going to /code/<file name>
        if self.path.startswith("/code/"):
            file_name = self.path.replace("/code/", "", 1)
            self.send_code(file_name)
        # The page asks for bugs by going to /bugs/<file name>
        elif self.path.startswith("/bugs/"):
            file_name = self.path.replace("/bugs/", "", 1)
            self.send_bugs(file_name)
        else:
            # Anything else is a normal website file (index.html, etc.)
            super().do_GET()

    def send_code(self, file_name):
        file = (code_folder / file_name).resolve()

        # Only send .py files that are inside SampleCode.
        # This keeps the answer keys (the .txt files) hidden from participants.
        if file.parent != code_folder or file.suffix != ".py" or not file.exists():
            self.send_reply(404, {"error": "Could not find " + file_name})
            return

        self.send_reply(200, {"name": file.name, "code": file.read_text()})

    def send_bugs(self, file_name):
        file = (bug_folder / file_name).resolve()
        if file.parent != bug_folder or file.suffix != ".json" or not file.exists():
            self.send_reply(404, {"error": "Could not find " + file_name})
            return

        self.send_reply(200, {"name": file.name, "bugs": json.loads(file.read_text())["bugs"]})

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
