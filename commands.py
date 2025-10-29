from classes import Record
from colorama import Fore



from colorama import Fore
import traceback

def input_error(func):
    """
    Декоратор для обробки типових помилок під час виконання команд.

    Обгортає функції, які взаємодіють з адресною книгою, 
    і перехоплює стандартні виключення.

    Обробляє:
        - ValueError: коли кількість або формат аргументів некоректний.
        - KeyError: коли контакт або інший ключ не знайдено.
        - IndexError: коли не вистачає аргументів.
        - TypeError: коли виклик функції зроблено з неправильними типами або кількістю аргументів.
        - AttributeError: коли звернення до неіснуючих атрибутів (наприклад, record = None).
        - Exception: будь-яка інша непередбачена помилка (для налагодження).
    """

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except ValueError:
            return f"{Fore.RED}Enter the correct arguments for the command.{Fore.RESET}"

        except KeyError:
            return f"{Fore.YELLOW}Contact not found.{Fore.RESET}"

        except IndexError:
            return f"{Fore.RED}Not enough arguments. Check the command usage.{Fore.RESET}"

        except TypeError:
            return f"{Fore.RED}Invalid arguments or missing parameters. Please check your input.{Fore.RESET}"

        except AttributeError:
            return f"{Fore.RED}Action failed: object does not exist. Possibly contact not found.{Fore.RESET}"

        except Exception as e:
            print(f"{Fore.RED}[DEBUG] Unexpected error:{Fore.RESET}", e)
            traceback.print_exc()
            return f"{Fore.RED}An unexpected error occurred. Check the logs for details.{Fore.RESET}"

    return inner

def parse_input(user_input):
    """
    Розбиває введений користувачем рядок на команду та аргументи.
    Повертає кортеж (command, args).
    """
    command, *args = user_input.split()
    command = command.strip().lower()
    return command, args


@input_error
def add_contact(args, book):
    """
    Додає новий контакт або оновлює існуючий.
    Формат: add <name> <phone>
    """
    name, phone, *_ = args
    record = book.find(name)
    message = 'Contact updated'
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added"
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args, book):
    """
    Змінює номер телефону для існуючого контакту.
    Формат: change <name> <old_phone> <new_phone>
    """
    name, old_phone, new_phone, *_ = args
    record = book.find(name)

    if record is None:
        return f"Contact {name} not found"
    
    if old_phone not in [p.value for p in record.phones]:
        return f"Phone '{old_phone}' not found for '{name}'"
        
    for p in record.phones:
        if p.value == old_phone:
            p.value = new_phone
            break
    
    return f"Phone for {name} changed from {old_phone} to {new_phone}."


@input_error
def show_phone(args, book):
    """
    Показує всі телефони для вказаного контакту.
    Формат: phone <name>
    """
    phones = []
    name, = args
    record = book.find(name)

    for p in record.phones:
        phones.append(p.value)

    return f"Contact {name} have {len(phones)} phones : {'\n'.join(phones)}"


@input_error
def show_all(book):
    """
    Показує всі контакти з адресної книги.
    """
    return "\n".join(str(record) for record in book.data.values())


@input_error
def add_birthday(args, book):
    """
    Додає дату народження для вказаного контакту.
    Формат: add-birthday <name> <DD.MM.YYYY>
    """
    name, birthday_str = args
    record = book.find(name)
    if record is None:
        return f"Contact {name} not found"
    record.add_birthday(birthday_str)
    return f"Birthday for {name} added successfuly"


@input_error
def show_birthday(args, book):
    """
    Показує дату народження контакту.
    Формат: show-birthday <name>
    """
    name, = args
    record = book.find(name)
    if record is None:
        return f"Contact '{name}' not found"
    if record.birthday is None:
        return f"not birthday set for {name}"
    return f"{name}'s birthday is {record.birthday.value}"


@input_error
def birthdays(book):
    """
    Показує список контактів з днями народження,
    які наближаються найближчим часом.
    """
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "Not upcoming birthdays"
    lines = [f"{item['name']}: {item['birthday']}" for item in upcoming]
    return '\n'.join(lines)