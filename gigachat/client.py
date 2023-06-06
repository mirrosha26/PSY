import socket
import threading

class ChatClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.client_socket.connect((self.host, self.port))
        nickname = input("Введите ваш никнейм: ")
        self.client_socket.send(nickname.encode())

        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

        self.send_messages()

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                print(message)
            except Exception as e:
                print("Ошибка при получении сообщений:", e)
                self.client_socket.close()
                break

    def send_messages(self):
        while True:
            try:
                message = input()
                self.client_socket.send(message.encode())
            except Exception as e:
                print("Ошибка при отправке сообщения:", e)
                self.client_socket.close()
                break

if __name__ == "__main__":
    host = input("Введите имя хоста или IP-адрес: ")
    port = int(input("Введите номер порта: "))
    client = ChatClient(host, port)
    client.connect()
