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
        '''
        Checks for an empty string or a string that is too long
        '''
        if type(arg) != str:
            raise TypeError(f'{arg} is not string data type')
        elif arg == "":
            raise InvalidDataError("A field can not be empty")
        elif len(arg) > 500:
            raise InvalidDataError("A field is too long.")

        return True

class OptionalString(Field):
    def __init__(self, name: str, label: str):
        super().__init__(name, label)

    def validate(cls, arg: str): 
        '''
        Checks for string data type and length of string
        '''
        if type(arg) != str:
            raise TypeError(f'{arg} is not string data type')
        elif len(arg) > 500:
            raise InvalidDataError("A field is too long.")

        return True


class Integer(Field):
    def __init__(self, name: str, label: str):
        super().__init__(name, label)

    @classmethod
    def validate(cls, arg: str): 
        '''
        Checks if the arg is numeric and not empty
        '''
        if arg == "":
            raise InvalidDataError("A field can not be empty")
            
        if not isinstance(arg, int) and not arg.isnumeric():
            raise TypeError(f'{arg} is not a number.')

        return True

class OptionalInteger(Field):
    def __init__(self, name: str, label: str):
        super().__init__(name, label)

    @classmethod
    def validate(cls, arg: str):
        '''
        Checks if the arg is numeric
        '''
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
        '''
        Checks for valid age for a JC student
        '''
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
        '''
        Checks for a valid year
        '''
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
        '''
        Checks for a valid date in YYYYMMDD format
        '''
        if date_text == "":
            raise InvalidDataError("A field can not be empty")
            
        try:
            datetime.datetime.strptime(date_text, '%Y%m%d')
        except TypeError:
            raise TypeError('Date is invalid.')
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYYMMDD")

class OptionalDate(Field):
    def __init__(self, name: str, label: str):
        super().__init__(name, label)
        
    @classmethod
    def validate(cls, date_text: str):
        '''
        Checks for a valid date in YYYYMMDD format or a empty string
        '''
        if date_text == "":
            return True
            
        try:
            datetime.datetime.strptime(date_text, '%Y%m%d')
        except TypeError:
            raise TypeError('Date is invalid.')
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYYMMDD")
        
class Category(Field):
    def __init__(self, name: str, label: str):
        super().__init__(name, label)
        
    @classmethod
    def validate(cls, arg):
        '''
        Checks for valid category
        '''
        if arg not in ["Achievement", "Enrichment", "Leadership", "Service"]:
            raise InvalidDataError('Category must be Achievement, Enrichment, Leadership or Service')
            
        
