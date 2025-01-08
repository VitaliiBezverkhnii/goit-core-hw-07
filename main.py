from colorama import Fore
from address_book import AddressBook
from bot_helper import add_birthday, add_contact, birthdays, change_contact, parse_input, show_all, show_birthday, show_phone


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
    