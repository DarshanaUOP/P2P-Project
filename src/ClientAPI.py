import http.server
import socketserver
import os
import urllib.parse
import fnmatch
import json
import time
import sys
import requests

DIRECTORY = './'

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
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
        elif parsed_path.path == '/list':
            query = urllib.parse.parse_qs(parsed_path.query)
            dir_path = query.get('dir', [''])[0]

            resFile = []
            resDir = []
            for path in os.listdir(dir_path):
                if os.path.isfile(os.path.join(dir_path, path)):
                    resFile.append(path)
                else:
                    resDir.append(path)

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {
                "files": resFile,
                "dirs": resDir,
                "status": "success"
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

# Function to start the server
def start_server(port, directory):
    os.chdir(directory)
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print(f"Serving HTTP on port {port}")
        httpd.serve_forever()

# Function to download a file from the server
def download_file(file_path, server_url="http://localhost:8000"):
    try:
        if not os.path.exists(DIRECTORY + "/".join(file_path.split('/')[:-1])):
            os.makedirs(DIRECTORY + "/".join(file_path.split('/')[:-1]))

        url = f"{server_url}/{file_path}"
        print('Downloading from:', url)
        response = requests.get(url, stream=True)
        response.raise_for_status()

        local_filename = os.path.join(DIRECTORY + os.path.basename(file_path))
        print(local_filename)
        with open(local_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    except:
        print("Error downloading file:", file_path, file=sys.stderr)

# Function to search for files on the server
def search_files(server_url, pattern):
    url = f"{server_url}/search?pattern={pattern}"
    response = requests.get(url)
    response.raise_for_status()
    search_results = response.json()
    if search_results['status'] == 'success':
        return search_results['results']
    else:
        print("Search failed:", search_results, file=sys.stderr)
        return []

# Function to list files and directories on the server
def ls_files(server_url, pattern):
    url = f"{server_url}/list?dir={pattern}"
    response = requests.get(url)
    response.raise_for_status()
    search_results = response.json()
    if search_results['status'] == 'success':
        return search_results['dirs'], search_results['files']
    else:
        print("Execution failed:", search_results, file=sys.stderr)
        return [], []

# Function to search for files across multiple servers
def search(conn, pattern):
    success = False
    while not success:
        try:
            for u in conn.users:
                search_results = []
                search_results.append(search_files(f"http://{u.ip}:{u.port}", pattern))
                print("Search results from:", f"http://{u.ip}:{u.port}")
                print("---------------")
                for result in search_results:
                    for r in result:
                        print("⇒", u.name, '/', r)
                print("---------------\n\n")
            success = True
        except:
            print("Error searching for files. Reconnecting to bootstrap server...")
            time.sleep(5)
            conn.reconnect()
    return search_results

# Function to list files and directories across multiple servers
def ls(conn, path):
    con2 = conn
    success = False
    while not success:
        try:
            for u in con2.users:
                dirs, files = ls_files(f"http://{u.ip}:{u.port}", path)
                print("File list from:", f"http://{u.ip}:{u.port}{path}")
                print("---------------")
                for r in dirs:
                    print("Dir ⇒", u.name, '⇒', r)
                for r in files:
                    print("File ⇒", u.name, '⇒', r)
                print("---------------\n\n")
            success = True
        except:
            print("Error searching for files. Reconnecting to bootstrap server...")
            time.sleep(5)
            print(conn.users)
            con2 = conn.reconnect()
