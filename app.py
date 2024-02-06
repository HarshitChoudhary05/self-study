from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.request import urlopen
from urllib.parse import urlparse, parse_qs

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)

        if parsed_url.path == '/fetch':
            url = query_params.get('url', [''])[0]
            if url:
                try:
                    with urlopen(url) as response:
                        content = response.read().decode('utf-8')
                        self.send_response(200)
                        self.send_header('Content-type', 'text/plain')
                        self.end_headers()
                        self.wfile.write(content.encode('utf-8'))
                except Exception as e:
                    self.send_response(500)
                    self.end_headers()
                    self.wfile.write(b"Error fetching URL: " + str(e).encode('utf-8'))
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Please provide a valid URL.")
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Page not found.")

def run_server():
    host = ('localhost', 8000)
    server = HTTPServer(host, RequestHandler)
    print('Server running on http://localhost:8000')
    server.serve_forever()

if __name__ == '__main__':
    run_server()
