import http.server
import socketserver
import os
import urllib.parse
import fnmatch
import json

DIRECTORY = './'
class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # Override the translate_path method to change the root directory
        path = http.server.SimpleHTTPRequestHandler.translate_path(self, path)
        relpath = os.path.relpath(path, os.getcwd())
        fullpath = os.path.join('./', relpath)
        return fullpath

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path == '/search':
            query = urllib.parse.parse_qs(parsed_path.query)
            pattern = query.get('pattern', ['*'])[0]
            matches = self.find_files(DIRECTORY, pattern)
            print(f"Found {len(matches)} files matching {pattern}")
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {
                "status": "success",
                "results": [os.path.relpath(match, DIRECTORY) for match in matches]
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            super().do_GET()

    def find_files(self, directory, pattern):
        matches = []
        pattern = '*' + pattern + '*'
        for root, dirs, files in os.walk(directory):
            for filename in fnmatch.filter(files, pattern):
                matches.append(os.path.join(root, filename))
        return matches


Handler = CustomHandler

def start_server(port, directory):
    os.chdir(directory)
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print(f"Serving HTTP on port {port}")
        httpd.serve_forever()
