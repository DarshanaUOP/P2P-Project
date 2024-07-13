import socket

storage =  set()
# Mock Server
def add_peer(msg):
    global storage
    storage.add(" ".join(msg.split()[1:]))
    return storage

def get_peers(data):
    global storage
    requesting_peer = " ".join(data.split()[1:])
    filtered = [peer for peer in storage if peer != requesting_peer]
    return len(filtered), " ".join(list(filtered))

def start_bootstrap_server(ip, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(5)
    print(f"Bootstrap server running on {ip}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        data = read_message(client_socket)
        print(f"Received data: `{data}`")
        
        if data.startswith("REG"):
            add_peer(data)
            peer_count, peers = get_peers(data)
            response = "0020 REGOK " + str(peer_count) + " " + peers
        elif data.startswith("UNREG"):
            response = "0020 UNROK 0"
        else:
            response = "0010 ERROR"
        
        client_socket.send(response.encode())
        client_socket.close()

def read_message(client_socket):
    # Read the first 4 bytes to get the message length
    length_str = client_socket.recv(5).decode()
    if not length_str:
        return None
    length = int(length_str)
    
    # Read the rest of the message
    message = client_socket.recv(length).decode()
    return message

if __name__ == "__main__":
    start_bootstrap_server("127.0.0.1", 5555)
