"""
Author(s): Jakub Man <man@highpps.net>

A simple HTTP server serving an HTML file and an endpoint
for an EventSource simulating IP address upload.
"""

import time
from http.server import HTTPServer, BaseHTTPRequestHandler


class SSEHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # Serve the HTML file
            try:
                with open("index.html", "rb") as file:
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/html')
                    self.end_headers()
                    self.wfile.write(file.read())
            except FileNotFoundError:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"File index.html was not found.")
        elif self.path == '/upload':
            # Simulate the upload process with SSE
            self.send_response(200)
            # Notice the content type is event-stream
            self.send_header('Content-Type', 'text/event-stream')
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('Connection', 'keep-alive')
            self.end_headers()

            total_ips = 10_000_000

            # Send a message to the info channel
            self.wfile.write(f'event: info\n'.encode('utf-8'))
            self.wfile.write(f'data: {{"total": {total_ips}}}\n\n'.encode('utf-8'))
            self.wfile.flush()

            for index in range(0, total_ips, 100_000):
                self.wfile.write(f'event: progress\n'.encode('utf-8'))
                self.wfile.write(f'data: {index}\n\n'.encode('utf-8'))
                self.wfile.flush()
                time.sleep(0.1)  # Simulate time delay for each batch upload

            # Send completion message
            self.wfile.write(f'event: done\n'.encode('utf-8'))
            self.wfile.write(f'data: Upload done.\n\n'.encode('utf-8'))
            self.wfile.flush()
        else:
            self.send_response(404)
            self.end_headers()


def run(server_class=HTTPServer, handler_class=SSEHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Serving on port {port}")
    httpd.serve_forever()


if __name__ == '__main__':
    run()
