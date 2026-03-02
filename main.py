import pickle
from functools import wraps
from pathlib import Path

from address_book import AddressBook, Record

DATA_FILE = Path("addressbook.pkl")


def save_data(book):
    with open(DATA_FILE, "wb") as f:
        pickle.dump(book, f)


def load_data():
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, "rb") as f:
                return pickle.load(f)
        except Exception:
            return AddressBook()
    return AddressBook()


def input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except IndexError:
            return "Enter correct arguments."
        except KeyError:
            return "Contact not found."
    return inner


def parse_input(user_input: str):
    parts = user_input.strip().split()
    if not parts:
        return "", []
    return parts[0].lower(), parts[1:]


@input_error
def add_contact(args, book):
    name, phone = args[0], args[1]
    record = book.find(name)

    if record is None:
        record = Record(name)
        book.add_record(record)
        record.add_phone(phone)
        return "Contact added."

    record.add_phone(phone)
    return "Contact updated."


@input_error
def change_contact(args, book):
    name, old_phone, new_phone = args[0], args[1], args[2]
    record = book.find(name)
    if record is None:
        raise KeyError
    record.edit_phone(old_phone, new_phone)
    return "Contact updated."


@input_error
def show_phone(args, book):
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError
    if not record.phones:
        return "No phones found."
    return "; ".join(p.value for p in record.phones)


@input_error
def show_all(args, book):
    if not book.data:
        return "Address book is empty."
    return "\n".join(str(record) for record in book.data.values())


@input_error
def add_birthday(args, book):
    name, birthday = args[0], args[1]
    record = book.find(name)
    if record is None:
        raise KeyError
    record.add_birthday(birthday)
    return "Birthday added."


@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError
    if record.birthday is None:
        return "Birthday not set."
    return str(record.birthday)


@input_error
def birthdays(args, book):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays."
    result = ["Upcoming birthdays:"]
    for item in upcoming:
        result.append(f"{item['name']}: {item['congratulation_date']}")
    return "\n".join(result)


def main():
    book = load_data()
    print("Welcome to the assistant bot!")

    handlers = {
        "add": add_contact,
        "change": change_contact,
        "phone": show_phone,
        "all": show_all,
        "add-birthday": add_birthday,
        "show-birthday": show_birthday,
        "birthdays": birthdays,
    }

    try:
        while True:
            user_input = input("Enter a command: ")
            command, args = parse_input(user_input)

            if command in ["close", "exit"]:
                print("Good bye!")
                break

            if command == "hello":
                print("How can I help you?")
                continue

            handler = handlers.get(command)
            if handler:
                print(handler(args, book))
            else:
                print("Invalid command.")
    finally:
        save_data(book)


if __name__ == "__main__":
    main()