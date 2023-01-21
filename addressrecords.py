from collections import UserDict
import  datetime 
import re
import pickle

class Field():
    def __init__(self, value):
        self._value = None
        self.value = value
        
    @property
    def value(self):
        return self._value
         
    @value.setter
    def value(self, value):
        self._value = value

class Name(Field):

    @Field.value.setter
    def value(self, value):
        if value.isnumeric():
            raise ValueError("Name must contain only letters and space")
        self._value = value
        
      

class Phone(Field):

    @Field.value.setter
    def value(self, value):
        if not (len(value) >= 10 or len(value) <= 12):
            raise ValueError("Phone must have 10-12 numbers")

        if not value.isnumeric():
            raise ValueError('Phone must include only numbers')
        self._value = value

    def __eq__(self, other):
       return self.value == other.value
    
    def __str__(self) -> str:
        return self.value
             
class Birthday(Field): 
 #birthday must be string in format suitable for transformation in data-object 
    # %d Day of the month as a zero-padded decimal number.
    # %m Month as a zero-padded decimal number.
    # %Y Year with century as a decimal number.

    @Field.value.setter
    def value(self, value):
        if not re.fullmatch(r'\d{2}\.\d{2}\.\d{4}', value):
            raise ValueError("Birthday must be dd.mm.yyyy")

        birthday = (datetime.datetime.strptime(value, '%d.%m.%Y')).date()   
        current_day = datetime.date.today()
        if birthday > current_day:
            raise ValueError('Bad date of birthday')
        self._value = value
    
    def __str__(self) -> str:
        return self.value         

class Record():
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None):
    #def __init__(self, name):
        self.name = name
        self.phone_list = []
        if phone:
            self.phone_list.append(phone)
        self.birthday = birthday
        

      
    def add_phone(self, phone: Phone):
        self.phone_list.append(phone)
        return  

    def del_phone(self, phone: Phone):
        if phone in self.phone_list:
            self.phone_list.remove(phone) 
            return  f'{phone} in contact is deleted.'
        return "This phone doesn't exist, please try again."
        
    def change_phone(self, old_phone: Phone, new_phone: Phone):
        if old_phone in self.phone_list:
            self.phone_list.remove(old_phone)
            self.phone_list.append(new_phone)     
            return "Phone changed"
        return "This contact doesn't exist, please try again."  
    
    def search_phone(self, char_phone: str):
        result = False
        for phone in self.phone_list:
            if re.search(char_phone, phone.value):
                result = True
        return result

    def  show_all_phones(self):
        phones = ', '.join(str(p) for p in self.phone_list)
       
        return f'{phones}'
    
    def __repr__(self) -> str:
        if not self.birthday:
            birthday = "empty"
        else:
            birthday =  self.birthday.value
        if not self.phone_list: 
            phones = 'empty'
        else:
            phones =  self.show_all_phones()  
            
        #return  f'Name: {self.name.value}, birthday: {birthday},  phones: {phones}'    
        return "Name: {:<10}| Birthday: {:<12}| Phones: {:<12}".format(self.name.value, birthday, phones)
        
    def add_birthday(self, date):
        self.birthday = Birthday(date)
        return  

    def days_to_birthday(self):
        if not self.birthday:
            return "unknown, because no information."
        birthday = (datetime.datetime.strptime(self.birthday.value, '%d.%m.%Y')).date()   
        current_day = datetime.date.today()
        current_year = current_day.year    
        birthday_nearest = birthday.replace(year = current_year)   
        interval = (birthday_nearest - current_day).days
        if interval < 0:
            birthday_nearest = birthday.replace(year = current_year + 1)   
            interval = (birthday_nearest - current_day).days
    
        return interval

    

class AddressBook(UserDict):
    def __init__(self):
        self.data = {}

    def add_record(self, record: Record):
        self.data[record.name.value] = record
        return 

    def search_record(self, name: str):
        return self.data.get(name)  

    def search_name_by_sym(self, chars_name: str):
        name_coincidence = []
        for key in self.data.keys():
            if re.search(chars_name, key, flags=re.IGNORECASE):
                name_coincidence.append(self.data[key])
        return name_coincidence

    def search_phone_by_sym(self, chars_phone: str):
        phone_coincidence = []
        for value in self.data.values():
            if value.search_phone(chars_phone):
                phone_coincidence.append(value)
        return phone_coincidence        

    #def get_one_record(self, name):
    #    return self.data.get(name)  
    #self_name 
    #def show_all_contacts(self):
    #    return self.data

    def iterator(self, number_of_rec):
        page = []
        keys_len = len(list(self.data.keys()))
        for i in  range(0, keys_len, number_of_rec):
            slice = list(self.data.keys())[i:i+number_of_rec]
            for key in slice:
               page.append(self.data[key])
            yield page
            page = []
            slice = []

    def __str__(self):
       return  '\n'.join(str(record) for record in self.data.values())
       

    def serializer(self):
        if not self.data:
            return 'Address book is empty'
        with open('address_book.txt', "wb") as fh:
            pickle.dump(self.data, fh)
        return 'Address book saved'

    def deserializer(self):
        try:
            with open('address_book.txt', "rb") as fh:
                self.data = pickle.load(fh)
                res = 'Address book loaded'
        except  FileNotFoundError:
            res = 'No file address_book.txt'
        return res

    
