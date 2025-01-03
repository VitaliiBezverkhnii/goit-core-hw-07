from collections import UserDict
from datetime import date, datetime, timedelta
from functools import wraps
import re

from birthdays import get_upcoming_birthdays

class FormatPhoneNumberException(Exception):
     pass
          
          
class Field:
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
      
      def __init__(self, value):
            super().__init__(value)

class Phone(Field):

    def __init__(self, value):
        if not isinstance(value, str):
            raise ValueError("Телефонний номер повинен бути рядком")
        if not re.match(r"^\d{10}$", value):
            raise FormatPhoneNumberException(f"Невірний формат номера: {value}")
        super().__init__(value)

class Birthday(Field):

    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
    
    def to_str_format(self):
        return self.value.strftime("%d.%m.%Y")
        

class Record:
    
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone_number: str):
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number: str):
         self.phones = [phone for phone in self.phones if phone.value != phone_number]

    def edit_phone(self, old_phone_number: str, new_phone_number: str):
        for phone in self.phones:
            if phone.value == old_phone_number:
                try:
                    phone.value = Phone(new_phone_number).value
                except FormatPhoneNumberException:
                    raise
                return
        raise ValueError(f"Номер телефону не знайдено.")
    
    def find_phone(self, phone_number: str):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
    
    def add_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {', '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
       
    def add_record(self, record: Record):
           self.data[record.name.value] = record
    
    def find(self, name: str):
        return self.data.get(name, None)
    
    def get_all(self):
        return self.data

    def delete(self, name: str):
        if name in self.data:
            del self.data[name]
    
    def get_upcoming_birthdays(self) -> list:
        return get_upcoming_birthdays([
            {
                "name": name, 
                "birthday": contact.birthday.value
            } for name, contact in self.data.items()
            ])

    def __str__(self):
        return "".join(f"{record}\n" for record in self.data.values())