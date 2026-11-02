"""
Simple backend for our agentic AI demo.
"""

import json
import subprocess
import sys
import tempfile
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
        query = parse_qs(url.query)
        level = query.get("level", ["none"])[0]
        # "?bugs=gradeBook.json&fixed=1,3" means: apply the patches for bugs 1 and 3
        bug_file = query.get("bugs", [""])[0]
        fixed = [n for n in query.get("fixed", [""])[0].split(",") if n]

        if path.startswith("/code/"):
            file_name = path.replace("/code/", "", 1)
            if not fixed:
                participant = query.get("participant", ["?"])[0]
                experiment = query.get("experiment", ["?"])[0]
                print(f"Session started: participant {participant}, experiment {experiment}, level {level}")
            self.send_code(file_name, bug_file, fixed)
        elif path.startswith("/bugs/"):
            file_name = path.replace("/bugs/", "", 1)
            print(f"Sending bugs for level: {level}")
            self.send_bugs(file_name)
        elif path.startswith("/run/"):
            file_name = path.replace("/run/", "", 1)
            print(f"Running code for level: {level} (fixed bugs: {fixed or 'none'})")
            self.run_code(file_name, bug_file, fixed)
        else:
            super().do_GET()

    def find_code(self, file_name):
        file = (code_folder / file_name).resolve()
        if file.parent != code_folder or file.suffix != ".py" or not file.exists():
            return None
        return file

    def patched_code(self, file, bug_file, fixed):
        # start from the original code and apply the patch of every fixed bug
        code = file.read_text()
        if not fixed:
            return code
        bugs_file = (bugs_folder / bug_file).resolve()
        if bugs_file.parent != bugs_folder or bugs_file.suffix != ".json" or not bugs_file.exists():
            return code
        for bug in json.loads(bugs_file.read_text())["bugs"]:
            if str(bug["number"]) in fixed:
                for patch in bug.get("patch", []):
                    code = code.replace(patch["old"], patch["new"], 1)
        return code

    def send_code(self, file_name, bug_file, fixed):
        file = self.find_code(file_name)
        if file is None:
            self.send_reply(404, {"error": "Could not find " + file_name})
            return
        self.send_reply(200, {"name": file.name, "code": self.patched_code(file, bug_file, fixed)})

    def send_bugs(self, file_name):
        file = (bugs_folder / file_name).resolve()
        if file.parent != bugs_folder or file.suffix != ".json" or not file.exists():
            self.send_reply(404, {"error": "Could not find " + file_name})
            return
        self.send_reply(200, json.loads(file.read_text()))

    def run_code(self, file_name, bug_file, fixed):
        # actually run the sample code (with the accepted fixes applied) so the
        # page shows real output. A temporary copy is run so the original is never changed.
        file = self.find_code(file_name)
        if file is None:
            self.send_reply(404, {"error": "Could not find " + file_name})
            return
        with tempfile.TemporaryDirectory() as temp_folder:
            temp_file = Path(temp_folder) / file.name
            temp_file.write_text(self.patched_code(file, bug_file, fixed))
            try:
                result = subprocess.run(
                    [sys.executable, "-u", file.name],
                    cwd=temp_folder, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    text=True, timeout=10)
                output = result.stdout
                exit_code = result.returncode
            except subprocess.TimeoutExpired:
                output = "Program took too long and was stopped."
                exit_code = "timeout"
            # hide the full folder path so the output looks like it ran in SampleCode
            # (resolved path first: on macOS /var/... is really /private/var/...)
            output = output.replace(str(temp_file.resolve().parent) + "/", "").replace(temp_folder + "/", "")
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