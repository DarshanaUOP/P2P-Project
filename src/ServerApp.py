import socket
from utils import custom_print, custom_print_success, custom_print_error
class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.storage = set()
    
    # Function to add a peer to the storage
    def add_peer(self, msg):
        self.storage.add(" ".join(msg.split()[1:]))
        return self.storage

    # Function to drop a peer from the storage
    def drop_peer(self, msg):
        try:
            self.storage.remove(" ".join(msg.split()[1:]))
        except KeyError:
            pass
        return self.storage

    # Function to get the list of peers, excluding the requesting peer
    def get_peers(self, data):
        requesting_peer = " ".join(data.split()[1:])
        filtered_peers = [peer for peer in self.storage if peer != requesting_peer]
        return len(filtered_peers), " ".join(list(filtered_peers))

    # Function to start the bootstrap server
    def start_bootstrap_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('0.0.0.0', self.port))
        server_socket.listen(5)
        custom_print_success(f"Bootstrap server running on {self.ip}:{self.port}")

        while True:
            client_socket, addr = server_socket.accept()
            data = self.read_message(client_socket)
            if data.startswith("REG"):
                self.add_peer(data)
                custom_print_success(f"Added peer: {data}", len(self.storage))
                peer_count, peers = self.get_peers(data)
                response = "0020 REGOK " + str(peer_count) + " " + peers
            elif data.startswith("UNREG"):
                custom_print(f"Removed peer: {data}")
                self.drop_peer(data)
                response = "0020 UNROK 0"
            else:
                response = "0010 ERROR"
                custom_print_error(f"Error: {data}")
            client_socket.send(response.encode())
            client_socket.close()

    # Function to read a message from the client socket
    def read_message(self, client_socket):
        length_str = client_socket.recv(5).decode()
        if not length_str:
            return None
        length = int(length_str)
        message = client_socket.recv(length).decode()
        return message

if __name__ == "__main__":
    server = Server("127.0.0.1",5555)
    server.start_bootstrap_server()

