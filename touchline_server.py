# Run:  python3 touchline_server.py   (keep this window open during the match)
import http.server, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
PORT = 8080
STATE_FILE = os.path.join(HERE, 'state.json')
PAGES = {'/': ('touchline.html', 'text/html; charset=utf-8'),
         '/touchline.css': ('touchline.css', 'text/css; charset=utf-8')}
FONTS = {'.woff2': 'font/woff2', '.woff': 'font/woff', '.ttf': 'font/ttf', '.otf': 'font/otf'}
MAX_BODY = 2_000_000

try:
    with open(STATE_FILE, 'rb') as f:
        state = f.read() or b'null'
except OSError:
    state = b'null'

class H(http.server.BaseHTTPRequestHandler):
    def _send(self, body, ctype, code=200):
        self.send_response(code)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)

    def _file(self, path, ctype):
        try:
            with open(path, 'rb') as f:
                self._send(f.read(), ctype)
        except OSError:
            self._send(b'not found', 'text/plain', 404)

    def do_GET(self):
        p = self.path.split('?', 1)[0]
        if p == '/api/state':
            return self._send(state, 'application/json')
        if p in PAGES:
            name, ctype = PAGES[p]
            return self._file(os.path.join(HERE, name), ctype)
        if p in ('/logo/home', '/logo/away'):
            return self._file(os.path.join(HERE, 'logo_' + p[6:] + '.png'), 'image/png')
        if p.startswith('/fonts/'):
            full = os.path.realpath(os.path.join(HERE, p.lstrip('/')))
            ext = os.path.splitext(full)[1].lower()
            if full.startswith(os.path.join(HERE, 'fonts') + os.sep) and ext in FONTS:
                return self._file(full, FONTS[ext])
        self._send(b'not found', 'text/plain', 404)

    def do_POST(self):
        global state
        n = int(self.headers.get('Content-Length', 0))
        if n > MAX_BODY:
            return self._send(b'too large', 'text/plain', 413)
        body = self.rfile.read(n)
        p = self.path.split('?', 1)[0]
        if p == '/api/state':
            try:
                json.loads(body)
            except ValueError:
                return self._send(b'bad json', 'text/plain', 400)
            state = body
            with open(STATE_FILE, 'wb') as f:
                f.write(body)
            return self._send(b'ok', 'text/plain')
        if p in ('/api/logo/home', '/api/logo/away'):
            with open(os.path.join(HERE, 'logo_' + p[10:] + '.png'), 'wb') as f:
                f.write(body)
            return self._send(b'ok', 'text/plain')
        self._send(b'not found', 'text/plain', 404)

    def log_message(self, *a): pass

try:
    srv = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), H)
except OSError:
    sys.exit(f'Port {PORT} is already in use. Close the other Touchline window (or change PORT) and try again.')
print(f'Touchline running:  controller http://localhost:{PORT}/   overlay http://localhost:{PORT}/?overlay=1')
srv.serve_forever()
