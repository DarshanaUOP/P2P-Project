import http.server
import socketserver
import os
import base64 

DIRECTORY = './'

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        path = http.server.SimpleHTTPRequestHandler.translate_path(self, path)
        relpath = os.path.relpath(path, os.getcwd())
        fullpath = os.path.join('./', relpath)
        return fullpath

Handler = CustomHandler

# Function to start the server
def start_server(port, directory):
    os.chdir(directory)
    with socketserver.TCPServer(("", port), Handler) as httpd:
        custom_print_success(f"Serving HTTP on port {port}")
        httpd.serve_forever()

def custom_print(*message):
    print(*message)

def custom_print_error(*message):
    print("\033[31m×", *message, "\033[0m")

def custom_print_success(*message):
    print("\033[32m¤", *message, "\033[0m")

def encode_base64(message=""):
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message

def decode_base64(base64_message=""):
    base64_bytes = base64_message.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')
    return message
