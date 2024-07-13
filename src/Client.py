from bootstrap_server import BootstrapServerConnection

class Node:
    def __init__(self, ip, port, name):
        self.ip = ip
        self.port = port
        self.name = name

# Usage example
if __name__ == "__main__":
    bs_node = Node("127.0.0.1", 5555, "bootstrap")
    my_node = Node("127.0.0.1", 5000, "my_node")
    
    with BootstrapServerConnection(bs_node, my_node) as conn:
        print("Connected users:", conn.users)
