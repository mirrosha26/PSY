import socket
import threading

class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = []
        self.nicknames = []

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()

        print("Server started on {}:{}".format(self.host, self.port))

        while True:
            client_socket, client_address = self.server_socket.accept()
            print("New connection from {}".format(client_address))
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def handle_client(self, client_socket):
        client_name = client_socket.recv(1024).decode()
        self.nicknames.append(client_name)
        self.clients.append(client_socket)
        self.broadcast("Server", "{} joined the chat!".format(client_name))
        client_socket.send("Welcome to the chat, {}!".format(client_name).encode())

        while True:
            try:
                message = client_socket.recv(1024).decode()
                self.broadcast(client_name, message)
            except:
                index = self.clients.index(client_socket)
                self.clients.remove(client_socket)
                client_socket.close()
                nickname = self.nicknames[index]
                self.nicknames.remove(nickname)
                self.broadcast("Server", "{} left the chat.".format(nickname))
                break

    def broadcast(self, sender, message):
        for client_socket in self.clients:
            client_socket.send("{}: {}".format(sender, message).encode())

if __name__ == "__main__":
    server = ChatServer("localhost", 8000)
    server.start()
