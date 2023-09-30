import socket
import threading
import json

class Server:
    def __init__(self, listen_ip, port):
        self.listen_ip = listen_ip
        self.port = port
        self.variables = {}
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.listen_ip, self.port))
        self.socket.listen(2)

    def create_variable(self, name):
        if name not in self.variables:
            self.variables[name] = 0
            return "Variable created."
        else:
            return "Variable already exists."

    def set_variable(self, name, value):
        if name in self.variables:
            self.variables[name] = value
            return "Variable set."
        else:
            return "Variable does not exist."

    def get_variable(self, name):
        if name in self.variables:
            return self.variables[name]
        else:
            return "Variable does not exist."

    def handle_client(self, client_socket):
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            request = json.loads(data)
            action = request["action"]
            name = request["name"]

            if action == "create":
                response = self.create_variable(name)
            elif action == "set":
                value = request["value"]
                response = self.set_variable(name, value)
            elif action == "get":
                response = self.get_variable(name)

            client_socket.send(json.dumps(response).encode())

    def start(self):
        while True:
            client_socket, client_address = self.socket.accept()
            print("Accepted connection from", client_address)
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()
            
def get_ip_address():
    hostname1 = socket.gethostname()
    ip_address1 = socket.gethostbyname(hostname1)
    return ip_address1

if __name__ == '__main__':
    print("DD2DSD Server is running here!")
    print("on LOCAL ip:",get_ip_address())
    server = Server(get_ip_address(),8200)
    server.start()