
from classes import AddressBook
from commands import add_birthday, add_contact, birthdays, change_contact, show_all, show_birthday, show_phone 
import pickle


def save_data(data, filename='addressbook.pkl'):
    """
    Save the AddressBook into a file using pickle.

    Args:
        data (AddressBook): AddressBook instance to save.
        filename (str, optional): Path to the file. Defaults to 'addressbook.pkl'.
    """
    with open(filename, 'wb') as file:
        pickle.dump(data, file)

def load_data(filename='addressbook.pkl'):
    """Loading AddressBook from file
    filename: path to file, where is saving AddressBook"""
    try:
        with open(filename, 'rb') as file:
            data = pickle.load(file)
            return data
    except FileNotFoundError:
        return AddressBook()
    


def parse_input(user_input):
    """
    Parse user input into command and arguments.

    Args:
        user_input (str): рядок, введений користувачем.

    Returns:
        tuple: (command, args), де command (str) — команда, 
            args (list[str]) — список аргументів.
    """
    # Розбиваємо введений рядок на частини
    command, *args = user_input.split()
    # Видаляємо зайві пробіли і приводимо команду до нижнього регістру
    command = command.strip().lower()
    return command, args


def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)
        args = args[0]
        if command in ["close", "exit"]:
            print("Good bye!")
            save_data(book)
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(args)
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(book))

        else:
            print("Invalid command.")



# Запуск програми
if __name__ == "__main__":
    main()