"""Local preview server. Run from the project root: python3 case-study/_src/serve.py 8770

Works like `python3 -m http.server`, with two differences: browsers are told not to keep files,
so a rebuild always shows up, and it answers byte-range requests, which Safari needs to play video.
"""
import os
import re
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer


class Handler(SimpleHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'
    remaining = None

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Accept-Ranges', 'bytes')
        super().end_headers()

    def send_head(self):
        self.remaining = None
        path = self.translate_path(self.path)
        match = re.fullmatch(r'bytes=(\d*)-(\d*)', self.headers.get('Range', ''))
        if not match or not any(match.groups()) or not os.path.isfile(path):
            return super().send_head()
        first, last = match.groups()
        size = os.path.getsize(path)
        start = int(first) if first else max(size - int(last), 0)
        end = min(int(last), size - 1) if first and last else size - 1
        if start > end:
            self.send_error(416)
            return None
        source = open(path, 'rb')
        source.seek(start)
        self.remaining = end - start + 1
        self.send_response(206)
        self.send_header('Content-Type', self.guess_type(path))
        self.send_header('Content-Range', f'bytes {start}-{end}/{size}')
        self.send_header('Content-Length', str(self.remaining))
        self.end_headers()
        return source

    def copyfile(self, source, outputfile):
        try:
            if self.remaining is None:
                super().copyfile(source, outputfile)
            while self.remaining:
                chunk = source.read(min(self.remaining, 1 << 16))
                if not chunk:
                    break
                outputfile.write(chunk)
                self.remaining -= len(chunk)
        except (BrokenPipeError, ConnectionResetError):
            self.close_connection = True   # the browser stopped this download, as it does when seeking


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8770
    print(f'http://localhost:{port}/case-study/', flush=True)
    ThreadingHTTPServer(('', port), Handler).serve_forever()
