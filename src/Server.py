import socket

def start_bootstrap_server(ip, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(5)
    print(f"Bootstrap server running on {ip}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        data = client_socket.recv(1024).decode()
        if data.startswith("REG"):
            response = " 0020 REGOK 2 127.0.0.1 5001 node1 127.0.0.1 5002 node2"
        elif data.startswith("UNREG"):
            response = " 0020 UNROK 0"
        else:
            response = " 0010 ERROR"
        client_socket.send(response.encode())
        client_socket.close()

if __name__ == "__main__":
    start_bootstrap_server("127.0.0.1", 5555)
