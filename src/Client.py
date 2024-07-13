from bootstrap_server import BootstrapServerConnection
import sys
import time
from ClientAPI import start_server, search, ls, download_file
import threading

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
        return conn

def worker(node):
    try:
        path='./'
        if (len(sys.argv) == 7):
            path = sys.argv[6]
        print("File Server Started at port", node.port, ". Serving files from ", path)
        start_server(node.port, path)
    except:
        print("Error starting file server", file=sys.stderr)
    

def execute_command(command, t, conn):
    try:
        args = command.split()
        if args[0] == "exit":
            t.join()
            sys.exit(0)
        elif args[0] == "search":
            search(conn, args[1])
        elif args[0] == "ls":
            if len(args) == 1:
                ls(conn, '.')
            else:
                ls(conn, args[1])
        elif args[0] == "fetch":
            file_path=args[2]
            serverUrl = "http://" +conn.users[0].ip + ":" + str(conn.users[0].port)
            if(conn.users[0].name!= args[1]):
                serverUrl = "http://" +conn.users[1].ip + ":" + str(conn.users[1].port)
            print(serverUrl)
            download_file(file_path, serverUrl)
        else:
            print("Invalid command")
    except:
        print("Error executing command", file=sys.stderr)

def ux(t,conn):
    print('\n\n-----------------------------------------')
    while True:
        command = input("Command: ")
        execute_command(command, t, conn)
        print('\n\n-----------------------------------------')

# Usage example
if __name__ == "__main__":
    if (len(sys.argv) != 6 and len(sys.argv) != 7):
        print("Usage: python3 Client.py <bootstrap_ip> <bootstrap_port> <node_ip> <node_port> <node_name>")
        sys.exit(1)
    bs_node = Node(sys.argv[1], int(sys.argv[2]), "bootstrap")
    my_node = Node(sys.argv[3], int(sys.argv[4]), sys.argv[5])
    # Start File Server
    t = threading.Thread(target=worker, args=(my_node, ))
    t.start()
    conn = connect_to_bootstrap_server(bs_node, my_node)
    print("Ready to serve files")
    ux(t,conn)
    t.join()

