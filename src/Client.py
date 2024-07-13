from bootstrap_server import BootstrapServerConnection
import sys
import time
from ClientAPI import start_server, search, ls, download_file
import threading

# Class to represent a Node
class Node:
    def __init__(self, ip, port, name):
        self.ip = ip
        self.port = port
        self.name = name

# Function to connect to the bootstrap server
def connect_to_bootstrap_server(bs_node, my_node):
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

# Worker function to start the file server
def worker(node):
    try:
        path = './'
        if len(sys.argv) == 7:
            path = sys.argv[6]
        print("File Server Started at port", node.port, ". Serving files from ", path)
        start_server(node.port, path)
    except:
        print("Error starting file server", file=sys.stderr)

# Function to execute a command
def execute_command(command, thread, conn):
    try:
        args = command.split()
        if args[0] == "exit":
            thread.join()
            sys.exit(0)
        elif args[0] == "search":
            search(conn, args[1])
        elif args[0] == "ls":
            if len(args) == 1:
                ls(conn, '.')
            else:
                ls(conn, args[1])
        elif args[0] == "fetch":
            file_path = args[2]
            server_url = f"http://{conn.users[0].ip}:{conn.users[0].port}"
            if conn.users[0].name != args[1]:
                server_url = f"http://{conn.users[1].ip}:{conn.users[1].port}"
            print(server_url)
            download_file(file_path, server_url)
        elif args[0] == "reset":
            conn.reconnect()
            print("Connected users:", len(conn.users))
            for u in conn.users:
                print(str(u))
        elif args[0] == "tb":
            for u in conn.users:
                print(str(u))
        elif args[0] == "help":
            print("Commands: search <pattern>, ls <path>, fetch <user> <file>, reset, exit, tb")
        else:
            print("Invalid command")
            print("Commands: search <pattern>, ls <path>, fetch <user> <file>, reset, exit, tb")
    except:
        print("Error executing command", file=sys.stderr)

# Function for the user interface
def ux(thread, conn):
    print('\n\n-----------------------------------------')
    while True:
        command = input("Command: ")
        execute_command(command, thread, conn)
        print('\n\n-----------------------------------------')

# Main function to start the client
if __name__ == "__main__":
    if len(sys.argv) != 6 and len(sys.argv) != 7:
        print("Usage: python3 Client.py <bootstrap_ip> <bootstrap_port> <node_ip> <node_port> <node_name>")
        sys.exit(1)
    bootstrap_node = Node(sys.argv[1], int(sys.argv[2]), "bootstrap")
    my_node = Node(sys.argv[3], int(sys.argv[4]), sys.argv[5])
    thread = threading.Thread(target=worker, args=(my_node,))
    thread.start()
    connection = connect_to_bootstrap_server(bootstrap_node, my_node)
    print("Ready to serve files")
    ux(thread, connection)
    thread.join()
