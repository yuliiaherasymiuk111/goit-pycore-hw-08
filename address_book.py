from collections import UserDict
from datetime import datetime, date, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        value = str(value).strip()
        if not value:
            raise ValueError("Name cannot be empty.")
        super().__init__(value)


class Phone(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        new_value = str(new_value).strip()
        if not (new_value.isdigit() and len(new_value) == 10):
            raise ValueError("Phone number must contain exactly 10 digits.")
        self._value = new_value

    def __init__(self, value):
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            birthday_dt = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

        super().__init__(birthday_dt)

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        phone = str(phone)
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return
        raise ValueError("Phone not found.")

    def edit_phone(self, old_phone, new_phone):
        old_phone = str(old_phone)
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                return
        raise ValueError("Old phone not found.")

    def find_phone(self, phone):
        phone = str(phone)
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday_str):
        self.birthday = Birthday(birthday_str)

    def __str__(self):
        phones_str = "; ".join(p.value for p in self.phones) if self.phones else "no phones"
        birthday_str = str(self.birthday) if self.birthday else "no birthday"
        return f"Contact name: {self.name.value}, phones: {phones_str}, birthday: {birthday_str}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name) or self.data.get(name.title())

    def delete(self, name):
        self.data.pop(name, None)

    def get_upcoming_birthdays(self):
        today = date.today()
        upcoming = []

        for record in self.data.values():
            if record.birthday is None:
                continue

            bday = record.birthday.value

            # обробка високосного року
            try:
                birthday_this_year = bday.replace(year=today.year)
            except ValueError:
                # якщо 29 лютого і рік не високосний → 28 лютого
                birthday_this_year = date(today.year, 2, 28)

            if birthday_this_year < today:
                try:
                    birthday_this_year = bday.replace(year=today.year + 1)
                except ValueError:
                    birthday_this_year = date(today.year + 1, 2, 28)

            if 0 <= (birthday_this_year - today).days <= 7:
                congratulation_date = birthday_this_year

                if congratulation_date.weekday() == 5:
                    congratulation_date += timedelta(days=2)
                elif congratulation_date.weekday() == 6:
                    congratulation_date += timedelta(days=1)

                upcoming.append(
                    {
                        "name": record.name.value,
                        "congratulation_date": congratulation_date.strftime("%d.%m.%Y"),
                    }
                )

        return upcoming