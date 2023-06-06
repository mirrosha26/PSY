import socket

def start_client(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket.connect((host, port))
        print("Соединение с сервером установлено.")
        
        data = client_socket.recv(1024)
        message = data.decode().strip()
        if message.startswith("Введите ваше имя"):
            name = input(message + ": ")
            client_socket.sendall(name.encode())

            data = client_socket.recv(1024)
            message = data.decode().strip()
            
            if message.startswith("Введите ваш пароль"):
                password = input(message + ": ")
                client_socket.sendall(password.encode())
                data = client_socket.recv(1024)
                print(data.decode().strip())
            else:
                print(data.decode().strip())
        else:
            print(message)

        while True:
            message = input("Введите строку для отправки серверу (для выхода введите 'exit'): ")
            
            if not message:
                continue
            
            if message.lower() == "exit":
                break
            
            client_socket.sendall(message.encode())
            print("Отправка данных серверу:", message)
            
            data = client_socket.recv(1024)
            print("Прием данных от сервера:", data.decode())
        
    finally:
        client_socket.close()
        print("Разрыв соединения с сервером.")

if __name__ == "__main__":
    host = input("Введите имя хоста (по умолчанию 127.0.0.1): ") or "127.0.0.1"
    port = input("Введите номер порта (по умолчанию 12345): ") or 12345
    
    print("Запуск клиента...")
    start_client(host, int(port))
