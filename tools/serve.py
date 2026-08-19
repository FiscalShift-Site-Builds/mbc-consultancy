#!/usr/bin/env python3
"""Local preview server for site/.

Mirrors how Cloudflare Pages resolves URLs, so what you see locally is what
deploys: /compliance serves compliance.html, an unknown path serves 404.html
with a real 404 status, and _redirects rules are honoured.

    python3 tools/serve.py [port]      # default 8000

The contact form's /api/contact endpoint is a Cloudflare Function and is NOT
served here — posting the form locally returns 503, which the page handles by
offering the WhatsApp fallback. Use `npx wrangler pages dev site` to exercise
the real function.
"""

import http.server
import os
import re
import socketserver
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "site")
ROOT = os.path.abspath(ROOT)


def load_redirects():
    rules = {}
    path = os.path.join(ROOT, "_redirects")
    if not os.path.exists(path):
        return rules
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = re.split(r"\s+", line)
            if len(parts) >= 2:
                rules[parts[0]] = (parts[1], int(parts[2]) if len(parts) > 2 else 302)
    return rules


REDIRECTS = load_redirects()


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def log_message(self, fmt, *args):
        sys.stderr.write("  %s\n" % (fmt % args))

    def send_head(self):
        path = self.path.split("?")[0].split("#")[0]

        if path in REDIRECTS:
            target, code = REDIRECTS[path]
            self.send_response(code)
            self.send_header("Location", target)
            self.end_headers()
            return None

        # Extensionless -> .html, the way Pages resolves it.
        if path != "/" and not os.path.splitext(path)[1]:
            candidate = os.path.join(ROOT, path.lstrip("/") + ".html")
            if os.path.exists(candidate):
                self.path = path + ".html"

        full = os.path.join(ROOT, self.path.lstrip("/").split("?")[0])
        if not os.path.exists(full) and not self.path.endswith("/"):
            return self.serve_404()

        return super().send_head()

    def serve_404(self):
        page = os.path.join(ROOT, "404.html")
        if not os.path.exists(page):
            self.send_error(404)
            return None
        body = open(page, "rb").read()
        self.send_response(404)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        return __import__("io").BytesIO(body)


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", port), Handler) as httpd:
        print("Serving %s at http://127.0.0.1:%d (Ctrl-C to stop)" % (ROOT, port))
        httpd.serve_forever()


if __name__ == "__main__":
    main()
