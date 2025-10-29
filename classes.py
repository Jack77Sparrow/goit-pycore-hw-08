from collections import UserDict
from typing import List, Optional, Union
from datetime import datetime, timedelta, date
import pickle

class Field:
    """
    Базовий клас для полів запису.
    Зберігає значення поля у атрибуті `value`.
    Може використовуватися як для імені, телефону, дня народження тощо.
    """

    def __init__(self, value: str):
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    """
    Клас для імені контакту.
    Наслідує Field, додаткових методів не потребує.
    """

    pass


class Phone(Field):
    """
    Клас для номера телефону з валідацією.
    Номер повинен бути рядком з 10 цифр.
    """

    def __init__(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Phone must be a string of digits")
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone must be 10 digits")
        super().__init__(value)


class Birthday(Field):
    """
    Клас для дати народження.
    Формат: DD.MM.YYYY.
    Виконує перевірку формату при створенні.
    """

    def __init__(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")  # перевіряємо формат дати
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(value)


class Record:
    """
    Запис одного контакту: ім'я + список телефонів + опційно день народження.
    Містить методи для роботи з телефонами та датою народження.
    """

    def __init__(self, name: Union[str, Name]):
        # підтримка як рядка, так і об'єкта Name
        self.name: Name = name if isinstance(name, Name) else Name(name)
        self.phones: List[Phone] = []
        self.birthday: Optional[Birthday] = None

    def add_birthday(self, value):
        """Додає день народження контакту."""
        self.birthday = Birthday(value)

    def add_phone(self, phone: str) -> None:
        """
        Додає телефон до контакту.
        Перевіряє дублікати, щоб уникнути повторень.
        """
        p = Phone(phone)
        if any(existing.value == p.value for existing in self.phones):
            return
        self.phones.append(p)

    def find_phone(self, phone: str) -> Optional[Phone]:
        """Повертає телефон за номером або None, якщо не знайдено."""
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def remove_phone(self, phone: str) -> bool:
        """Видаляє телефон. Повертає True, якщо видалено, інакше False."""
        found = self.find_phone(phone)
        if found:
            self.phones.remove(found)
            return True
        return False

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        """
        Замінює старий телефон на новий.
        Використовує add_phone та remove_phone для перевірки валідності.
        """
        if not self.find_phone(old_phone):
            raise ValueError("Phone not found")
        self.add_phone(new_phone)
        self.remove_phone(old_phone)

    def __str__(self) -> str:
        phones_str = "; ".join(p.value for p in self.phones) or "(no phones)"
        return f"Contact name: {self.name.value}, phones: {phones_str}"


class AddressBook(UserDict):
    """
    Книга контактів, обгортка над словником.
    Ключі — імена контактів, значення — об'єкти Record.
    Підтримує додавання, видалення та пошук контактів.
    Також містить функції для роботи з днями народження.
    """

    def add_record(self, record: Record) -> None:
        """Додає Record до книги контактів."""
        self.data[record.name.value] = record

    def find(self, name: str) -> Optional[Record]:
        """Повертає Record за ім'ям або None, якщо не знайдено."""
        return self.data.get(name)

    def delete(self, name: str) -> Optional[Record]:
        """Видаляє запис з книги та повертає його, або None."""
        return self.data.pop(name, None)

    # ---------------- Додаткові методи для роботи з датами ----------------
    def string_to_date(self, date_string):
        """Перетворює рядок у форматі YYYY.MM.DD на об'єкт date."""
        return datetime.strptime(date_string, "%Y.%m.%d").date()

    def date_to_string(self, date_obj):
        """Перетворює об'єкт date на рядок у форматі YYYY.MM.DD."""
        return date_obj.strftime("%Y.%m.%d")

    def prepare_user_list(self, user_data):
        """
        Перетворює список словників з даними користувачів
        у список з іменами та об'єктами date для дня народження.
        """
        prepared_list = []
        for user in user_data:
            prepared_list.append({
                "name": user["name"],
                "birthday": self.string_to_date(user["birthday"])
            })
        return prepared_list

    def find_next_weekday(self, start_date, weekday):
        """
        Знаходить наступну дату з певним днем тижня (0 = понеділок).
        Якщо start_date вже після цього дня тижня, повертає наступний тиждень.
        """
        days_ahead = weekday - start_date.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return start_date + timedelta(days=days_ahead)

    def adjust_for_weekend(self, birthday):
        """
        Якщо день народження на вихідні, переносить на понеділок.
        """
        if birthday.weekday() >= 5:  # 5 = субота, 6 = неділя
            return self.find_next_weekday(birthday, 0)
        return birthday

    def get_upcoming_birthdays(self, days=7):
        """
        Повертає список контактів, у яких день народження
        буде найближчим часом (за замовчуванням 7 днів).
        Враховує перенесення на понеділок, якщо на вихідні.
        """
        upcoming_birthdays = []
        today = date.today()

        for name, record in self.data.items():
            if not record.birthday:
                continue

            birthday_date = datetime.strptime(record.birthday.value, '%d.%m.%Y').date()
            birthday_this_year = birthday_date.replace(year=today.year)

            # якщо день народження вже минув — переносимо на наступний рік
            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            days_until_birthday = (birthday_this_year - today).days
            if 0 <= days_until_birthday <= days:
                congratulation_date = self.adjust_for_weekend(birthday_this_year)
                upcoming_birthdays.append({
                    "name": name,
                    "birthday": self.date_to_string(congratulation_date)
                })

        return upcoming_birthdays

    def __str__(self) -> str:
        """Повертає рядок із усіма контактами або повідомлення про порожню книгу."""
        if not self.data:
            return "<empty address book>"
        return "\n".join(str(record) for record in self.data.values())