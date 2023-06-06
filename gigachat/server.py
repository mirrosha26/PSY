import socket
import threading

class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_sockets = []
        self.client_names = []

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print("Сервер чата запущен на {}:{}".format(self.host, self.port))

        while True:
            client_socket, client_address = self.server_socket.accept()
            print("Подключение от {}:{}".format(client_address[0], client_address[1]))

            client_name = client_socket.recv(1024).decode()
            self.client_names.append(client_name)
            self.client_sockets.append(client_socket)

            self.broadcast("Server", "{} присоединился к чату!".format(client_name))

            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_name))
            client_thread.start()

    def handle_client(self, client_socket, client_name):
        while True:
            try:
                message = client_socket.recv(1024).decode()
                if message:
                    self.broadcast(client_name, message)
            except Exception as e:
                print("Ошибка при обработке сообщения от клиента:", e)
                index = self.client_sockets.index(client_socket)
                self.client_sockets.remove(client_socket)
                client_socket.close()
                client_name = self.client_names[index]
                self.client_names.remove(client_name)
                self.broadcast("Server", "{} покинул чат.".format(client_name))
                break
                
    def broadcast(self, sender, message):
        for client_socket in self.client_sockets:
            try:
                client_socket.send("{}: {}".format(sender, message).encode())
            except socket.error as e:
                print("Ошибка при отправке сообщения:", e)

if __name__ == "__main__":
    server = ChatServer("localhost", 8001)
    server.start()
