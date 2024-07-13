import socket

# Function to add a peer to the storage
def add_peer(msg, storage):
    storage.add(" ".join(msg.split()[1:]))
    return storage

# Function to drop a peer from the storage
def drop_peer(msg, storage):
    try:
        storage.remove(" ".join(msg.split()[1:]))
    except KeyError:
        pass
    return storage

# Function to get the list of peers, excluding the requesting peer
def get_peers(data, storage):
    requesting_peer = " ".join(data.split()[1:])
    filtered_peers = [peer for peer in storage if peer != requesting_peer]
    return len(filtered_peers), " ".join(list(filtered_peers))

# Function to start the bootstrap server
def start_bootstrap_server(ip, port, storage):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(5)
    print(f"Bootstrap server running on {ip}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        data = read_message(client_socket)
        print(f"Received data: `{data}`")
        
        if data.startswith("REG"):
            add_peer(data, storage)
            peer_count, peers = get_peers(data, storage)
            response = "0020 REGOK " + str(peer_count) + " " + peers
        elif data.startswith("UNREG"):
            response = "0020 UNROK 0"
        else:
            response = "0010 ERROR"
        print(storage)
        client_socket.send(response.encode())
        client_socket.close()

# Function to read a message from the client socket
def read_message(client_socket):
    length_str = client_socket.recv(5).decode()
    if not length_str:
        return None
    length = int(length_str)
    message = client_socket.recv(length).decode()
    return message

if __name__ == "__main__":
    peer_storage = set()
    start_bootstrap_server("127.0.0.1", 5555, peer_storage)
