import socket
import logging

def read_clients(filename):
    clients = {}
    try:
        with open(filename, 'r') as file:
            for line in file:
                ip, name, password = line.strip().split(',')
                clients[ip] = (name, password)
    except FileNotFoundError:
        pass
    return clients

def write_client(filename, ip, name, password):
    with open(filename, 'a') as file:
        file.write(f"{ip},{name},{password}\n")

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logging.basicConfig(filename='server.log', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    while True:
        try:
            server_socket.bind((host, port))
            break
        except OSError:
            port += 1

    server_socket.listen(1)
    logging.info(f"Сервер запущен и начал прослушивание порта {port}")
    print(f"Сервер запущен и начал прослушивание порта {port}")

    clients_filename = 'clients.txt'
    clients = read_clients(clients_filename)

    while True:
        client_socket, client_address = server_socket.accept()
        client_ip = client_address[0]
        logging.info(f"Подключение клиента: {client_address}")

        if client_ip in clients:
            client_name, client_password = clients[client_ip]
            client_socket.sendall(f"Введите пароль, {client_name}: ".encode())
            data = client_socket.recv(1024)
            password = data.decode().strip()
            if password == client_password:
                client_socket.sendall(f"Привет, {client_name}!\n".encode())
            else:
                client_socket.sendall("Неверный пароль. Отключение...".encode())
                logging.info("Неверный пароль. Клиент отключился.")
                client_socket.close()
                continue
        else:
            client_socket.sendall("Введите ваше имя: ".encode())
            data = client_socket.recv(1024)
            client_name = data.decode().strip()

            client_socket.sendall("Введите ваш пароль: ".encode())
            data = client_socket.recv(1024)
            client_password = data.decode().strip()

            clients[client_ip] = (client_name, client_password)
            write_client(clients_filename, client_ip, client_name, client_password)
            client_socket.sendall(f"Привет, {client_name}!\n".encode())

        while True:
            data = client_socket.recv(1024)

            if not data:
                logging.info("Клиент отключился.")
                break

            message = data.decode().strip()

            if message.lower() == "exit":
                logging.info("Клиент отправил команду разрыва соединения.")
                break

            client_socket.sendall(data)
            logging.info(f"Отправка данных клиенту: {data}")

        client_socket.close()

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 12345

    print("Запуск сервера...")
    start_server(host, port)
