from bootstrap_server import BootstrapServerConnection
import sys
import time
from ClientAPI import start_server 

class Node:
    def __init__(self, ip, port, name):
        self.ip = ip
        self.port = port
        self.name = name

def connect_to_bootstrap_server(bs_node, my_node):
    with BootstrapServerConnection(bs_node, my_node) as conn:
        while len(conn.users) == 0:
            print("No other users connected")
            time.sleep(5)
            print("Re Connecting to bootstrap server...")
            conn.reconnect()
        print("Connected users:", len(conn.users))
        for u in conn.users:
            print('⇒', str(u))
# Usage example
if __name__ == "__main__":
    if (len(sys.argv) != 6):
        print("Usage: python3 Client.py <bootstrap_ip> <bootstrap_port> <node_ip> <node_port> <node_name>")
        sys.exit(1)
    bs_node = Node(sys.argv[1], int(sys.argv[2]), "bootstrap")
    my_node = Node(sys.argv[3], int(sys.argv[4]), sys.argv[5])
    connect_to_bootstrap_server(bs_node, my_node)
    start_server(my_node.port, './')

