from bootstrap_server import BootstrapServerConnection
import sys
import time
from ClientAPI import start_server, search, ls, download_file, CustomHandler
import threading
import os
import socketserver
import random


class Node:
    def __init__(self, ip, port, name):
        self.ip = ip
        self.port = port
        self.name = name

class Client:
    def __init__(self, bs_ip, bs_port, my_ip, my_port, my_name, servePath):
        self.bootstrap_node = Node(bs_ip, bs_port, "bootstrap")
        self.my_node = Node(my_ip, my_port, my_name)
        self.thread = threading.Thread(target=self.__worker__, args=())
        self.servePath = servePath
        self.fileServerPort = random.randint(5500, 6000)
        self.thread.start()
        self.connection = self.connect_to_bootstrap_server(self.bootstrap_node, self.my_node)
        print("Ready to serve files")
        while True:
            pass

    def connect_to_bootstrap_server(self, bs_node, my_node):
        with BootstrapServerConnection(bs_node, my_node) as conn:
            while len(conn.users) == 0:
                print("No other users connected")
                time.sleep(5)
                print("Reconnecting to bootstrap server...")
                conn.reconnect()
            print("Connected users:", len(conn.users))
            for user in conn.users:
                print('⇒', str(user))
            return conn

    def __worker__(self):
        try:
            print("File Server Started at port", self.fileServerPort, ". Serving files from ", self.servePath)
            start_server(self.fileServerPort, self.servePath)
        except:
            print("Error starting file server", file=sys.stderr) 


if __name__ == "__main__":
    if len(sys.argv) != 6 and len(sys.argv) != 7:
        print("Usage: python3 Client.py <bootstrap_ip> <bootstrap_port> <node_ip> <node_port> <node_name> <serve_path>")
        sys.exit(1)
    client = Client(sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), sys.argv[5], sys.argv[6])
