import socket
import threading
from queue import Queue
from tqdm import tqdm

class PortScanner:
    def __init__(self, host):
        self.host = host
        self.open_ports = []

    def scan_port(self, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((self.host, port))
            if result == 0:
                self.open_ports.append(port)
            sock.close()
        except socket.error:
            pass

    def scan_ports(self, num_threads=10):
        queue = Queue()

        # Создание очереди портов для сканирования
        for port in range(1, 65536):
            queue.put(port)

        # Функция для сканирования портов из очереди
        def worker():
            while not queue.empty():
                port = queue.get()
                self.scan_port(port)

        # Создание и запуск потоков для сканирования
        threads = []
        for _ in range(num_threads):
            thread = threading.Thread(target=worker)
            thread.start()
            threads.append(thread)

        # Ожидание завершения всех потоков
        for thread in threads:
            thread.join()

        # Вывод открытых портов по порядку
        self.open_ports.sort()
        if len(self.open_ports) == 0:
            print("Нет открытых портов на хосте {}".format(self.host))
        else:
            print("Открытые порты на хосте {}: ".format(self.host))
            for port in self.open_ports:
                print("Порт {} открыт".format(port))

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
            except:
                print("Ошибка при получении сообщений.")
                self.client_socket.close()
                break

    def send_messages(self):
        while True:
            message = input()
            self.client_socket.send(message.encode())

if __name__ == "__main__":
    host = input("Введите имя хоста или IP-адрес: ")
    

    scanner = PortScanner(host)
    scanner_thread = threading.Thread(target=scanner.scan_ports, args=(10,))
    scanner_thread.start()

    with tqdm(total=65535) as pbar:
        while scanner_thread.is_alive():
            pbar.update(len(scanner.open_ports))
            pbar.set_postfix({"Открытых портов": len(scanner.open_ports)})
            pbar.refresh()

    scanner_thread.join()
    port = int(input("Введите номер порта: "))
    client = ChatClient(host, port)
    client.connect()
