
from classes import AddressBook
from commands import add_birthday, add_contact, birthdays, change_contact, show_all, show_birthday, show_phone 




def parse_input(user_input):
    """
    Parse user input into command and arguments.

    Args:
        user_input (str): рядок, введений користувачем.

    Returns:
        tuple: (command, args), де command (str) — команда, 
            args (list[str]) — список аргументів.
    """

    user_input = user_input.strip()

    if not user_input:
        return None, []
    # Розбиваємо введений рядок на частини
    command, *args = user_input.split()
    # Видаляємо зайві пробіли і приводимо команду до нижнього регістру
    command = command.strip().lower()
    return command, args




def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)
        args = args[0]
        if command in ["close", "exit"]:
            print("Good bye!")
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