import os
import shutil


class FileManager:
    def __init__(self, root_path):
        self.root_path = os.path.abspath(root_path)
        self.current_path = self.root_path

    def change_directory(self, path):
        new_path = os.path.abspath(os.path.join(self.current_path, path))
        if new_path.startswith(self.root_path):
            if os.path.exists(new_path) and os.path.isdir(new_path):
                self.current_path = new_path
                print(f"Текущая директория изменена на: {self.current_path}")
            else:
                print("Директория не существует.")
        else:
            print("Доступ запрещен. Невозможно покинуть корневую директорию.")

    def go_up(self):
        parent_path = os.path.dirname(self.current_path)
        if parent_path.startswith(self.root_path):
            self.current_path = parent_path
            print(f"Текущая директория изменена на: {self.current_path}")
        else:
            print("Доступ запрещен. Невозможно подняться выше домашней директории.")

    def create_directory(self, name):
        dir_path = os.path.join(self.current_path, name)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"Создана директория: {dir_path}")
        else:
            print("Директория уже существует.")

    def delete_directory(self, name):
        dir_path = os.path.join(self.current_path, name)
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            os.rmdir(dir_path)
            print(f"Директория удалена: {dir_path}")
        else:
            print("Директория не существует.")

    def create_file(self, name):
        file_path = os.path.join(self.current_path, name)
        if not os.path.exists(file_path):
            open(file_path, 'w').close()
            print(f"Создан файл: {file_path}")
        else:
            print("Файл уже существует.")

    def write_to_file(self, name, content):
        file_path = os.path.join(self.current_path, name)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            with open(file_path, 'w') as file:
                file.write(content)
            print(f"Содержимое записано в файл: {file_path}")
        else:
            print("Файл не существует.")

    def view_file(self, name):
        file_path = os.path.join(self.current_path, name)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                print(f"Содержимое файла: {file_path}")
                print(file.read())
        else:
            print("Файл не существует.")

    def delete_file(self, name):
        file_path = os.path.join(self.current_path, name)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Файл удален: {file_path}")
        else:
            print("Файл не существует.")

    def copy_file(self, source, destination):
        source_path = os.path.join(self.current_path, source)
        destination_path = os.path.join(self.current_path, destination)
        if os.path.exists(source_path) and os.path.isfile(source_path):
            if not os.path.exists(destination_path):
                with open(source_path, 'rb') as src_file, open(destination_path, 'wb') as dest_file:
                    dest_file.write(src_file.read())
                print(f"Файл скопирован: {source_path} -> {destination_path}")
            else:
                print("Файл с таким именем уже существует.")
        else:
            print("Исходный файл не существует.")

    def copy_folder(self, source, destination):
        source_path = os.path.join(self.current_path, source)
        destination_path = os.path.join(self.current_path, destination)

        if os.path.exists(source_path) and os.path.isdir(source_path):
            if os.path.exists(destination_path):
                items = os.listdir(source_path)
                for item in items:
                    source_item_path = os.path.join(source_path, item)
                    destination_item_path = os.path.join(destination_path, item)
                    if os.path.isfile(source_item_path):
                        shutil.copy2(source_item_path, destination_item_path)
                print(f"Файлы скопированы: {source_path} -> {destination_path}")
            else:
                shutil.copytree(source_path, destination_path)
                print(f"Папка скопирована: {source_path} -> {destination_path}")
        else:
            print("Исходная папка не существует.")


    def move_file(self, source, destination):
        source_path = os.path.join(self.current_path, source)
        destination_path = os.path.join(self.current_path, destination)
        if os.path.exists(source_path) and os.path.isfile(source_path):
            if not os.path.exists(destination_path):
                os.rename(source_path, destination_path)
                print(f"Файл перемещен: {source_path} -> {destination_path}")
            else:
                print("Файл с таким именем уже существует.")
        else:
            print("Исходный файл не существует.")

    def rename_file(self, name, new_name):
        file_path = os.path.join(self.current_path, name)
        new_file_path = os.path.join(self.current_path, new_name)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            if not os.path.exists(new_file_path):
                os.rename(file_path, new_file_path)
                print(f"Файл переименован: {file_path} -> {new_file_path}")
            else:
                print("Файл с новым именем уже существует.")
        else:
            print("Файл не существует.")

# Определение пути к корневой директории
root_directory = input("Введите путь к корневой директории: ")

# Создание экземпляра FileManager
file_manager = FileManager(root_directory)


while True:
    print("\n=== Менеджер файлов ===")
    print("1. Сменить директорию")
    print("2. Создать директорию")
    print("3. Удалить директорию")
    print("4. Создать файл")
    print("5. Записать в файл")
    print("6. Просмотреть файл")
    print("7. Удалить файл")
    print("8. Скопировать файл")
    print("9. Переместить файл")
    print("10. Переименовать файл")
    print("11. Назад. На папку выше")
    print("12. Скоприровать содержимое папки")
    print("0. Выход")
    print("\n======")
    print(f"Вы находитесь: {file_manager.current_path}")
    choice = input("Введите номер операции: ")

    if choice == "1":
        path = input("Введите путь к директории: ")
        file_manager.change_directory(path)
    elif choice == "2":
        name = input("Введите имя директории: ")
        file_manager.create_directory(name)
    elif choice == "3":
        name = input("Введите имя директории: ")
        file_manager.delete_directory(name)
    elif choice == "4":
        name = input("Введите имя файла: ")
        file_manager.create_file(name)
    elif choice == "5":
        name = input("Введите имя файла: ")
        content = input("Введите содержимое файла: ")
        file_manager.write_to_file(name, content)
    elif choice == "6":
        name = input("Введите имя файла: ")
        file_manager.view_file(name)
    elif choice == "7":
        name = input("Введите имя файла: ")
        file_manager.delete_file(name)
    elif choice == "8":
        source = input("Введите имя исходного файла: ")
        destination = input("Введите имя целевого файла: ")
        file_manager.copy_file(source, destination)
    elif choice == "9":
        source = input("Введите имя исходного файла: ")
        destination = input("Введите имя целевого файла: ")
        file_manager.move_file(source, destination)
    elif choice == "10":
        name = input("Введите имя файла: ")
        new_name = input("Введите новое имя файла: ")
        file_manager.rename_file(name, new_name)
    elif choice == "11":
        file_manager.go_up()
    elif choice == "12":
        source = input("Введите имя исходной папки: ")
        destination = input("Введите имя целевой папки: ")
        file_manager.copy_folder(source, destination)
    
    elif choice == "0":
        break
    else:
        print("Неверный номер операции.")
