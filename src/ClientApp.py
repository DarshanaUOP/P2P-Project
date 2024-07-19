import hashlib
import os
import random
import socket
import sys
import threading
import time
from bootstrap_server import BootstrapServerConnection
from ClientAPI import start_server
import base64 

message = "Python is fun"
message_bytes = message.encode('ascii')
base64_bytes = base64.b64encode(message_bytes)
base64_message = base64_bytes.decode('ascii')

def custom_print(*message):
    print(*message)

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

class Node:
    def __init__(self, ip, port, name):
        self.ip = ip
        self.port = port
        self.name = name


class Client:
    def __init__(self, bs_ip, bs_port, my_ip, my_port, my_name, servePath):
        self.bootstrap_node = Node(bs_ip, bs_port, "bootstrap")
        self.my_node = Node(my_ip, my_port, my_name)
        self.servePath = servePath
        self.fileServerPort = random.randint(5500, 6000)
        self.connection = self.connect_to_bootstrap_server(self.bootstrap_node, self.my_node)

        self.file_server_thread = threading.Thread(target=self.__file_server_worker__, args=())
        self.udp_server_thread = threading.Thread(target=self.__udp_server_worker__, args=())
        self.command_thread = threading.Thread(target=self.__command_worker__, args=())

        self.file_server_thread.start()
        self.udp_server_thread.start()
        self.command_thread.start()

        self.resolvedMap = set([''])

        custom_print("Ready to serve files")

    def connect_to_bootstrap_server(self, bs_node, my_node):
        with BootstrapServerConnection(bs_node, my_node) as conn:
            while len(conn.users) == 0:
                custom_print("No other users connected")
                time.sleep(5)
                custom_print("Reconnecting to bootstrap server...")
                conn.reconnect()
            custom_print("Connected users:", len(conn.users))
            for user in conn.users:
                custom_print('⇒', str(user))
            return conn

    def __file_server_worker__(self):
        try:
            custom_print("File Server Started at port", self.fileServerPort, ". Serving files from ", self.servePath)
            start_server(self.fileServerPort, self.servePath)
        except Exception as e:
            custom_print("Error starting file server:", e, file=sys.stderr)

    def __udp_server_worker__(self):
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.bind((self.my_node.ip, self.my_node.port))
        custom_print(f"UDP Server started on {self.my_node.ip}:{self.my_node.port}")
        while True:
            message, address = udp_socket.recvfrom(4096)
            if message:
                message = message.decode('utf-8')
                length = int(message[:4])
                # print(address, "<-", message)
                command_message = message[4:4 + length]
                parsed_msg= command_message.split(' ')
                if(parsed_msg[0] == "RES"):
                    custom_print(f"Received response: { ' '.join(parsed_msg[2:])}", "HASH:", parsed_msg[1])
                else:
                    command, keyword, sender_ip, sender_port = command_message.split(' ', 3)
                    self.handle_command(command,decode_base64(keyword), sender_ip, int(sender_port), udp_socket)

    def handle_command(self, command, keyword, sender_ip, sender_port, udp_socket):
        try:
            if command == "search":
                responses = self.search_file(keyword)
                if f"{keyword} {sender_ip} {sender_port}" not in self.resolvedMap and responses is None:
                    self.resolvedMap.add(f"{keyword} {sender_ip} {sender_port}")
                    self.process_forward_command(f"search {keyword}".strip(), sender_ip, sender_port)
                elif responses is not None:
                    for response in responses:
                        response_m = f"RES {response}"
                        response_message = f"{len(response_m):04d}{response_m}"
                        udp_socket.sendto(response_message.encode('utf-8'), (sender_ip, sender_port))

                

            else:
                custom_print(f"Unknown command received: {command}")
        except Exception as e:
            custom_print("oops:", e, file=sys.stderr)

    def search_file(self, keyword):
        result = []
        for root, dirs, files in os.walk("./"):
            for file in files:
                if keyword in file:
                    file_path = os.path.join(root, file)
                    file_hash = self.generate_file_hash(file_path)
                    file_url = f"http://{self.my_node.ip}:{self.fileServerPort}/{file}"
                    result.append(f"{file_hash} {file_url}")
        if len(result)>0:
            return result
        return None

    @staticmethod
    def generate_file_hash(file_path):
        hash_algo = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_algo.update(chunk)
        return hash_algo.hexdigest()

    def __command_worker__(self):
        while True:
            user_input = input("")
            if user_input.strip():
                self.process_user_command(user_input.strip())

    def process_user_command(self, user_input):
        if(user_input == "help"):
            custom_print("Commands:")
            custom_print("search <keyword> - search for files with the keyword")
            return
        try:
            command, keyword = user_input.split(' ', 1)
            if command == "search":   
                keyword_encoded = encode_base64(keyword)
                encoded_input = f"{command} {keyword_encoded}"
                message = f"{len(encoded_input) + len(self.my_node.ip) + 6:04d}{encoded_input} {self.my_node.ip} {self.my_node.port}"
                for user in self.connection.users:
                    self.send_command_to_peer(user, message)
            else:   
                custom_print(f"Unknown command: {command}", keyword)
        except Exception as e:
            print("Error processing command:", e, file=sys.stderr)
    
    
    def process_forward_command(self, user_input, ip, port):
        command, keyword = user_input.split(' ', 1)
        keyword_encoded = encode_base64(keyword)
        encoded_input = f"{command} {keyword_encoded}"
        message = f"{len(encoded_input) + len(ip) + 6:04d}{encoded_input} {ip} {port}"
        for user in self.connection.users:
            if user.port != port or user.ip != ip:   
                self.send_command_to_peer(user, message)

    def send_command_to_peer(self, peer, message):
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.sendto(message.encode('utf-8'), (peer.ip, peer.port))
        custom_print(peer.ip, ':', peer.port, "->", message)


if __name__ == "__main__":
    if len(sys.argv) != 7:
        print("Usage: python3 Client.py <bootstrap_ip> <bootstrap_port> <node_ip> <node_port> <node_name> <serve_path>")
        sys.exit(1)
    client = Client(sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), sys.argv[5], sys.argv[6])
