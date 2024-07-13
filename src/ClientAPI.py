import http.server
import socketserver
import os
import urllib.parse
import fnmatch
import json
import time
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

import requests

def search_files(server_url, pattern):

    # Define the URL with the search pattern as a query parameter
    url = f"{server_url}/search?pattern={pattern}"
    
    # Make the GET request to the server
    response = requests.get(url)
    
    # Raise an exception if the request was unsuccessful
    response.raise_for_status()
    
    # Parse the JSON response
    search_results = response.json()
    
    # Check the status of the response
    if search_results['status'] == 'success':
        return search_results['results']
    else:
        print("Search failed:", search_results)
        return []

def search (conn, pattern):
   
    success = False
    while not success:
        try:
            for u in conn.users:
                search_results = []
                # Search for files matching the pattern
                search_results.append(search_files(f"http://{u.ip}:{u.port}", pattern))
                print("Search results from:", f"http://{u.ip}:{u.port}")
                print ("---------------")
                for result in search_results:
                    for r in result:
                        print("⇒",u.name,'/', r)
                print ("---------------\n\n")
            success = True
        except:
            print("Error searching for files. Reconnecting to bootstrap server...")
            time.sleep(5)
            conn.reconnect()
       
    return search_results
