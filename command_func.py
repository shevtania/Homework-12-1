from addressrecords import  AddressBook, Record, Name, Phone, Birthday
from decorator import input_error
address_book = AddressBook()

def hello():
    result = 'How can I help you?'
    return result

def exit(): 
    return 'exit'    

@input_error
def add_contact(name, phone = None, birthday = None):
    
    if  address_book.search_record(name):
        return 'This contact cannot be added, it already exists.'
    
   # if phone and (not birthday):
    #    record = Record(Name(name), None, Birthday(birthday))
    if phone and  (not birthday):
        record = Record(Name(name), Phone(phone), None)
    elif (not phone) and (not birthday):
        record = Record(Name(name), None, None)
    else:
        record = Record(Name(name), Phone(phone), Birthday(birthday))    
    address_book.add_record(record)
   
    return f'{record}'

@input_error
def add_phone(*args):
    name, phone = args
    if  not address_book.search_record(name):
        return "This phone cann't be added, contact doesn't exist."
    record = address_book.search_record(name)
    record.add_phone(Phone(phone))
    
    return f'Added {phone} in contact: {name}'

@input_error
def del_phone(*args):
    name, phone = args
    record = address_book.search_record(name)
    if  not address_book.search_record(name):
        return "This phone cann't be deleted, contact doesn't exist."
    record = address_book.search_record(name)
    result = record.del_phone(Phone(phone))
    
    return result

@input_error
def change_phone(*args):
    name, old_phone, new_phone = args
    record = address_book[name]
    result = record.change_phone(Phone(old_phone), Phone(new_phone))
   
    return result

@input_error
def phone_from_name(name):
       
    if not address_book.search_record(name):
        return f'This contact is not the book.'
    record = address_book.search_record(name)
    return f'{record.show_all_phones()}'


def  show_all_contacts(num_contacts_on_page = 5):
    result = ''
    num = 1
    if not address_book:
        return f'There are no contacts in the book.'

    iterator =  address_book.iterator(int(num_contacts_on_page))
    is_continue = 'y'  
    for page in iterator:
        print(f'page {num}')
        for line in page:
            print(line)
        num += 1
        is_continue = input('Do you want to continue? (Y/n)) ')
        if is_continue == 'y':
            continue
        elif is_continue == 'n':
            break
        else:
            raise ValueError("You must write 'y' or 'n'")

    return  result

def search_by_symbols(symbols):
    rec_list = []
    if symbols.isnumeric():
        rec_list = address_book.search_phone_by_sym(symbols)
    else:
        rec_list = address_book.search_name_by_sym(symbols)

    if not rec_list:
        return f'Nothing found'    

    return '\n'.join(str(i) for i in rec_list)


@input_error
def add_birthday(*args):
    name, date = args
    record = address_book.search_record(name)
    record.add_birthday(date)
    return f'Added {date} in contact: {name}'

@input_error
def get_days_to_birthday(name):
    if  not address_book.search_record(name):
        return "This command cann't be completed, contact doesn't exist."
    record = address_book.search_record(name)
    result = record.days_to_birthday()
    return f'Days to {name} birthday is {result}'
