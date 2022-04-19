import datetime

class RangeError(Exception):
    pass

class InvalidDataError(Exception):
    pass
    
class Field:
    def __init__(self, name: str, label: str):
        self.name = name
        self.label = label 

        
class String(Field):
    def __init__(self, name: str, label: str):
        super().__init__(name, label)

    @classmethod
    def validate(cls, arg: str): 
        if type(arg) != str:
            raise TypeError(f'{arg} is not string data type')
        elif arg == "":
            raise InvalidDataError("A field can not be empty")

        return True

class OptionalString(Field):
    def __init__(self, name: str, label: str):
        super().__init__(name, label)

    def validate(cls, arg: str): 
        if type(arg) != str:
            raise TypeError(f'{arg} is not string data type')

        return True


class Integer(Field):
    def __init__(self, name: str, label: str):
        super().__init__(name, label)

    @classmethod
    def validate(cls, arg: str): 
        if arg == "":
            raise InvalidDataError("A field can not be empty")
            
        if not arg.isnumeric():
            raise TypeError(f'{arg} is not a number.')

        return True

class OptionalInteger(Field):
    def __init__(self, name: str, label: str):
        super().__init__(name, label)

    @classmethod
    def validate(cls, arg: str): 
        if arg == "":
            return True
            
        if not arg.isnumeric():
            raise TypeError(f'{arg} is not a number.')

        return True

class Age(Field):
    def __init__(self, name: str, label: str):
        super().__init__(name, label)

    @classmethod
    def validate(cls, arg: int): 
        if arg == "":
            raise InvalidDataError("A field can not be empty")
            
        if not arg.isnumeric():
            raise TypeError(f'{arg} is not a number.')

        elif int(arg) > 20 or int(arg) < 10: #check that age is of acceptable range for a JC student 
            raise RangeError(f'{arg} is out of acceptable range')

        return True 
            

class Year(Field):
    def __init__(self, name: str, label: str):
        super().__init__(name, label)
        
    @classmethod
    def validate(cls, arg: int):
        if arg == "":
            raise InvalidDataError("A field can not be empty")
            
        if not arg.isnumeric():
            raise TypeError(f'{arg} is not a number.')
    
        elif 3000 < int(arg) or int(arg) < 2000: #limit to the 21th century 
            raise RangeError(f'{arg} is out of acceptable range')
    
        return True
        
class Date(Field):
    def __init__(self, name: str, label: str):
        super().__init__(name, label)
        
    @classmethod
    def validate(cls, date_text: str):
        if date_text == "":
            raise InvalidDataError("A field can not be empty")
            
        try:
            datetime.strptime(date_text, '%Y%m%d')
        except TypeError:
            raise TypeError('Date is invalid.')
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYYMMDD")

class OptionalDate(Field):
    def __init__(self, name: str, label: str):
        super().__init__(name, label)
        
    @classmethod
    def validate(cls, date_text: str):
        if date_text == "":
            return True
            
        try:
            datetime.strptime(date_text, '%Y%m%d')
        except TypeError:
            raise TypeError('Date is invalid.')
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYYMMDD")
        
class Category(Field):
    def __init__(self, name: str, label: str):
        super().__init__(name, label)
        
    @classmethod
    def validate(cls, arg):
        if arg not in ["Achievement", "Enrichment", "Leadership", "Service"]:
            raise InvalidDataError('Category not found')
            
        
