from collections import UserDict
from datetime import datetime, timedelta

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except ValueError as e:
            return str(e)
        except IndexError:
            return "Enter user name."
    return inner

def validate_phone(value):
    if not value.isdigit() or len(value) !=10:
        raise ValueError("Phone number must be 10 digits long")

def validate_date(value):
    try: 
        datetime.strptime(value, '%d.%m.%Y')
    except ValueError:
        raise ValueError("Invalid date format. Must be DD.MM.YYYY")

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name field cannot be empty")
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        validate_phone(value)
        super().__init__(value)
        
class Birthday(Field):
    def __init__(self, value):
        validate_date(value)
        super().__init__(value)        

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None
    
    def add_birthday(self, birthday):
        validate_date(birthday)
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]   
             
    def get_birthdays_per_week(self):
        today = datetime.today()
        next_week = today + timedelta(days=7)
        birthdays = []
        for record in self.data.values():
            if record.birthday:
                birthdate = datetime.strptime(record.birthday.value, '%d.%m.%Y')
                if today <= birthdate <= next_week:
                    birthdays.append(f"{record.name.value} ({birthdate.strftime('%d.%m')})")
        return birthdays        
            
@input_error
def parse_input(user_input, book):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args, book

@input_error
def add_contact(args, book):
    name, phone = args
    record = Record(name)
    record.add_phone(phone)
    book.add_record(record)
    return "Contact added."

@input_error
def change_phone(args, book):
    if len(args) == 2:
        name, new_phone = args
        record = book.find(name)
        if record:
            record.edit_phone(record.phones[0].value, new_phone)
            return f"{name}'s phone updated to {new_phone}."
        else:
            raise KeyError
        
@input_error    
def phone_username(args, book):
    name = args[0]
    record = book.find(name)
    return record.phones[0].value if record else "Contact not found"  

@input_error        
def all_contacts(args, book):
    if not book:
        return "Contact list is empty."
    result = ""
    for record in book.data.values():
        result += str(record) + "\n"
    return result 

@input_error  
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return f"Birthday added for {name}"
    else:
        raise KeyError
          
@input_error  
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    return record.birthday.value if record and record.birthday else "Contact not found"

@input_error  
def birthdays(args, book):
    birthdays_list = book.get_birthdays_per_week()
    return "\n".join(birthdays_list) if birthdays_list else "No birthdays in the next week"

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args, book = parse_input(user_input, book)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))    
        elif command == "change":
            print(change_phone(args, book))
        elif command == "phone":
            print(phone_username(args, book))
        elif command == "all":
            print(all_contacts(args, book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))        
        else:
            print("Invalid command.")
            
if __name__ == "__main__":
    main()