# Run:  python touchline_server.py   (keep this window open during the match)
import http.server, os
HERE = os.path.dirname(os.path.abspath(__file__))
PAGE = 'touchline_football_overlay_v3.html'
STYLESHEET = 'touchline_football_overlay_v3.css'
PORT = 8080
state = b'null'

class H(http.server.BaseHTTPRequestHandler):
    def _send(self, body, ctype):
        self.send_response(200)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)
    def do_GET(self):
        if self.path.startswith('/api/state'):
            return self._send(state, 'application/json')
        if self.path.split('?', 1)[0] == '/' + STYLESHEET:
            with open(os.path.join(HERE, STYLESHEET), 'rb') as f:
                return self._send(f.read(), 'text/css; charset=utf-8')
        with open(os.path.join(HERE, PAGE), 'rb') as f:
            self._send(f.read(), 'text/html; charset=utf-8')
    def do_POST(self):
        global state
        state = self.rfile.read(int(self.headers.get('Content-Length', 0)))
        self._send(b'ok', 'text/plain')
    def log_message(self, *a): pass

print(f'Touchline running:  controller http://localhost:{PORT}/   overlay http://localhost:{PORT}/?overlay=1')
http.server.ThreadingHTTPServer(('127.0.0.1', PORT), H).serve_forever()
