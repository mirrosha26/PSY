import socket
import threading

class ChatClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.client_socket.connect((self.host, self.port))
        nickname = input("Enter your nickname: ")
        self.client_socket.send(nickname.encode())

        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

        self.send_messages()

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                print(message)
            except:
                print("Error receiving messages.")
                self.client_socket.close()
                break

    def send_messages(self):
        while True:
            message = input()
            self.client_socket.send(message.encode())

if __name__ == "__main__":
    client = ChatClient("localhost", 8000)
    client.connect()
