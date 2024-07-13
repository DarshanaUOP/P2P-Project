import socket

# Mock Server
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
            response = "0020 REGOK 2 127.0.0.1 5001 node1 127.0.0.1 5002 node2"
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
