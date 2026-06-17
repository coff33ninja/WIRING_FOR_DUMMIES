#!/usr/bin/env python3
"""Documentation server for Wiring for Dummies — entry point."""

import http.server
import urllib.parse
import webbrowser
from pathlib import Path

from server.config import DIR, MIME, PORT, self_ip
from server.pages import (
    serve_component,
    serve_fundamental,
    serve_index,
    serve_index_page,
    serve_missed,
    serve_project,
    serve_search,
)


class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print(f"  {args[0]} {args[1]} {args[2]}")

    def _send(self, body, mime="text/html; charset=utf-8", status=200):
        if isinstance(body, Exception):
            import traceback
            tb = "".join(traceback.format_exception(type(body), body, body.__traceback__))
            body = f"<pre>{tb}</pre>"
            mime = "text/html; charset=utf-8"
            status = 500
        body = body.encode("utf-8") if isinstance(body, str) else body
        self.send_response(status)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.end_headers()
        self.wfile.write(body)

    def _serve_static(self, path):
        if path.lstrip("/").startswith("server/"):
            self._send("Forbidden", "text/plain", 403)
            return
        filepath = Path(DIR) / path.lstrip("/")
        if not filepath.exists() or not filepath.is_file():
            self._send("Not Found", "text/plain", 404)
            return
        ext = filepath.suffix.lower()
        mime = MIME.get(ext, "application/octet-stream")
        self._send(filepath.read_bytes(), mime)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.rstrip("/") or "/"
        params = urllib.parse.parse_qs(parsed.query)

        try:
            if path == "/":
                self._send(serve_index()); return
            if path == "/index":
                self._send(serve_index_page()); return
            if path == "/missed":
                self._send(serve_missed()); return
            if path == "/search":
                q = params.get("q", [""])[0]
                self._send(serve_search(q)); return
            if path.startswith("/components/"):
                name = path.split("/components/")[-1]
                self._send(serve_component(name)); return
            if path.startswith("/fundamentals/"):
                name = path.split("/fundamentals/")[-1]
                self._send(serve_fundamental(name)); return
            if path.startswith("/projects/"):
                name = path.split("/projects/")[-1]
                self._send(serve_project(name)); return
            self._serve_static(path)
        except Exception as e:
            self._send(e)


def main():

    print("  WIRING FOR DUMMIES")
    print("  ───────────────────────")
    print(f"  Serving:  {DIR}")
    print(f"  Local:    http://localhost:{PORT}")
    print(f"  Network:  http://{self_ip()}:{PORT}")
    print(f"  Search:   http://localhost:{PORT}/search?q=resistor")
    print(f"  Scanner:  http://localhost:{PORT}/missed")
    print("  ───────────────────────")
    print("  Press Ctrl+C to stop")

    try:
        server = http.server.HTTPServer(("0.0.0.0", PORT), Handler)
        webbrowser.open(f"http://localhost:{PORT}")
        server.serve_forever()
    except OSError:
        print(f"\n  [!] Port {PORT} is in use. Try: python main.py 8080")
    except KeyboardInterrupt:
        print("\n  Server stopped.")
        server.server_close()


if __name__ == "__main__":
    main()
