from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
import webbrowser


def serve_html():
    PORT = 8000
    handler = SimpleHTTPRequestHandler
    with TCPServer(("", PORT), handler) as httpd:
        print(f"Servindo face.html em http://localhost:{PORT}")
        webbrowser.open(f"http://localhost:{PORT}/face.html", new=2)
        httpd.serve_forever()


serve_html()
