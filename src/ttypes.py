# Assuming the Node class is defined in ttypes module as follows:
class Node:
    def __init__(self, ip, port, name):
        self.ip = ip
        self.port = port
        self.name = name
    def __str__(self) -> str:
        return f"{self.name} ({self.ip}:{self.port})"
