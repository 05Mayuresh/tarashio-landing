"""Local preview server for the landing page that tells browsers never to cache,
so every reload shows the latest index.html (plain `python -m http.server` lets
browsers reuse stale copies)."""
import http.server, functools, sys, os

class NoCache(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, max-age=0")
        super().end_headers()

port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
root = sys.argv[2] if len(sys.argv) > 2 else os.path.dirname(os.path.abspath(__file__))
handler = functools.partial(NoCache, directory=root)
print(f"Serving {root} at http://localhost:{port}")
http.server.ThreadingHTTPServer(("127.0.0.1", port), handler).serve_forever()
