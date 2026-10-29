import http.server
import json
import os
import socket
import urllib.request
import datetime


def outbound_ip():
    try:
        with urllib.request.urlopen("https://api.ipify.org", timeout=8) as r:
            return r.read().decode().strip()
    except Exception as exc:  # noqa: BLE001
        return "error:" + type(exc).__name__


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):  # noqa: N802
        payload = {
            "service": "ip-rotate-probe",
            "hostname": socket.gethostname(),
            "pid": os.getpid(),
            "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "outbound_ip": outbound_ip(),
        }
        body = json.dumps(payload, indent=2).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):  # noqa: N802
        pass


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    http.server.HTTPServer(("0.0.0.0", port), Handler).serve_forever()
