from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import requests
from bs4 import BeautifulSoup

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        url = data['url']
        result_message = self.inspect_source(url)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes(result_message, "utf-8"))

    def inspect_source(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                html_content = response.text
                soup = BeautifulSoup(html_content, 'html.parser')
                elements_with_source = soup.find_all(attrs={"source": True})
                source_urls = [element.get('source') for element in elements_with_source]
                if source_urls:
                    result_message = "Source URLs found:<br>" + "<br>".join(source_urls)
                else:
                    result_message = "No source URLs found in the inspected elements."
            else:
                result_message = "Failed to fetch URL. Status code: " + str(response.status_code)
        except Exception as e:
            result_message = "An error occurred: " + str(e)
        return result_message

def run_server():
    host = ('localhost', 8000)
    server = HTTPServer(host, RequestHandler)
    print('Server running on http://localhost:8000')
    server.serve_forever()

if __name__ == '__main__':
    run_server()
