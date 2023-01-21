from command_func import *
from addressrecords import  AddressBook, Record, Name, Phone, Birthday


HANDLERS = {
    "hello": hello,
    "good bye": exit,
    "close": exit,
    "exit": exit,
    "add contact": add_contact,
    "add phone": add_phone,
    "del phone": del_phone,
    "change": change_phone,
    "show contacts": show_all_contacts,
    "phone": phone_from_name,
    "add birthday": add_birthday,
    "days to birthday": get_days_to_birthday,
    "search": search_by_symbols
    }

def parser_input(user_input):
    command, *args = user_input.split()
    handler = None
    command = command.lower()
   
    while command  not in HANDLERS:
        if args:
            command = command + ' ' + args[0].lower()
            args = args[1:]    
        else:
           break
    handler = HANDLERS.get(command)
    return handler, *args
        
      
def main():
    load_status = address_book.deserializer()
    print(load_status)
    
    while True:
        user_input = input("Input command: ")
        handler, *args = parser_input(user_input)
        if handler:
            result = handler(*args)
        else:
            result = f'Unknown command'    
        
        if result == 'exit':
            save_status = address_book.serializer()
            print(save_status)
            print("Good bye!")
            break
        print(result)
        


if __name__ == "__main__":
   

    main()

