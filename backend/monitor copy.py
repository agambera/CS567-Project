import glob, json, os, time
from datetime import datetime

DIR = os.path.expanduser("~/.claude/projects/-Users-kylerhixon-Desktop-Claude-Playground")
LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "claudeLog")
offsets, seen = {}, set()

def entries(e):
    msg, sid = e.get("message", {}), e.get("sessionId", "?")[:8]
    content = msg.get("content")
    # transcript times are UTC ("...Z"); convert to this computer's local time
    ts = datetime.fromisoformat(e["timestamp"].replace("Z", "+00:00")).astimezone().strftime("%Y-%m-%d %H:%M:%S") if "timestamp" in e else "?"
    if e.get("type") == "user" and isinstance(content, str):
        yield ts, sid, "prompt", f"chars={len(content)}", content.replace("\n", " ")[:300]
    if e.get("type") == "assistant":
        for c in content or []:
            if c.get("type") == "tool_use":
                yield ts, sid, "tool", c["name"], json.dumps(c["input"])[:300]
        if msg.get("id") in seen:
            return
        seen.add(msg.get("id"))
        u = msg.get("usage", {})
        yield ts, sid, "tokens", msg.get("model", "?"), f"in={u.get('input_tokens', 0)} out={u.get('output_tokens', 0)} cache_read={u.get('cache_read_input_tokens', 0)} cache_write={u.get('cache_creation_input_tokens', 0)}"

while True:
    for path in glob.glob(f"{DIR}/*.jsonl"):
        with open(path) as f:
            f.seek(offsets.get(path, 0))
            lines = [l for l in f.readlines() if l.endswith("\n")]  # skip half-written line
            offsets[path] = offsets.get(path, 0) + sum(len(l.encode()) for l in lines)
        with open(LOG, "a") as log:
            for line in lines:
                for row in entries(json.loads(line)):
                    log.write(" | ".join(row) + "\n")
    time.sleep(1)
