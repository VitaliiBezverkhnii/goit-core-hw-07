from datetime import datetime
from colorama import Fore

from address_book import AddressBook, Birthday, Phone, Record
from birthdays import get_upcoming_birthdays

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "The requested contact does not exist in the phonebook."
        except IndexError:
            return "The command seems incomplete. Please provide all required arguments."
    return inner

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "added."
    if phone:
        record.add_phone(phone)
    return f"Contact {Fore.GREEN}{name}{Fore.RESET} with phone {Fore.GREEN}{phone}{Fore.RESET} {message}."

@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone = args
    record: Record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return f"Contact {Fore.GREEN}{name}{Fore.RESET} is changed."
    else:
        return f"{Fore.RED}Contact does not exist.{Fore.RESET}"
    
@input_error
def show_phone(args, book: AddressBook):
    name, = args
    record: Record = book.find(name)
    if record:
        record_phones: list[Phone] = record.phones
        return f"Contact name: {name}, phones: {', '.join(record.find_phone(phone.value).value for phone in record_phones)}"
    else:
        return f"{Fore.RED}Contact not found{Fore.RESET}"
    
@input_error
def show_all(args, book: AddressBook):
    str_contacts = f"{Fore.CYAN}All contacts:{Fore.RESET} \n"
    phones = book.get_all().values()
    if phones:
        for i, phone in enumerate(phones, start=1):
            str_contacts += f"{i}: {Fore.GREEN}{phone}{Fore.RESET}\n"
        return str_contacts[:-1]
    else:
        return f"{Fore.RED}Contacts is empty{Fore.RESET}"

@input_error
def add_birthday(args, book: AddressBook):
    name, birthday_str = args
    record: Record = book.find(name)
    message = "updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "added."
    record.add_birthday(birthday_str)
    return f"Contact {Fore.GREEN}{name}{Fore.RESET} with birthday {Fore.GREEN}{birthday_str}{Fore.RESET} {message}."

@input_error
def show_birthday(args, book):
    name, = args
    record: Record = book.find(name)
    if record:
        birthday = record.birthday
        birthday_formated = birthday.to_str_format()
        return f"Contact {Fore.GREEN}{name}{Fore.RESET} -> birthday: {Fore.GREEN}{birthday_formated}{Fore.RESET}."
    else:
        return f"{Fore.RED}Contact not found{Fore.RESET}"

@input_error
def birthdays(args, book: AddressBook):
    result = f"{Fore.CYAN}All upcoming birthdays:{Fore.RESET} \n"
    upcoming_birthdays = book.get_upcoming_birthdays()
    for i, contact in enumerate(upcoming_birthdays, start=1):
        name = contact["name"]
        congratulation_date = contact["congratulation_date"]
        result += f"{i}: {Fore.GREEN}{name}{Fore.RESET} - {Fore.GREEN}{congratulation_date}{Fore.RESET}\n"
    return result[:-1]

    
@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def main():
    print(f"{Fore.GREEN}Welcome to the assistant bot!{Fore.RESET}")
    book = AddressBook()
    while True:
        user_input = input(f"Enter a command: ").strip().lower()
        command, *args = parse_input(user_input)
        if command in ["close", "exit"]:
            print(f"{Fore.YELLOW} Good bye! {Fore.RESET}")
            break
        elif command == "hello":
            print(f"{Fore.YELLOW}How can I help you?{Fore.RESET}")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(args, book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        else:
            print(f"{Fore.RED}Invalid command.{Fore.RESET}")

if __name__ == "__main__":
    main()