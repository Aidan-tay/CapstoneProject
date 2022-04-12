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

        return True


class Integer(Field):
    def __init__(self, name: str, label: str):
        super().__init__(name, label)

    @classmethod
    def validate(cls, arg: int): 
        if type(arg) != int:
            raise TypeError(f'{arg} is not integer data type')

        return True

class Age(Field):
    def __init__(self, name: str, label: str):
        super().__init__(name, label)

    @classmethod
    def validate(cls, arg: int): 
        if type(arg) != int:
            raise TypeError(f'{arg} is not integer data type')

        if 20 > arg > 0: #check that age is of acceptable range for a JC student 
            raise RangeError(f'{arg} is out of acceptable range')

        return True 
            

class Year(Field):
    def __init__(self, name: str, label: str):
        super().__init__(name, label)
        
    @classmethod
    def validate(cls, arg: int):
        
        if type(arg) != int:
                raise TypeError(f'{arg} is not integer data type')
    
        if 3000 > arg > 2000: #limit to the 21th century 
            raise RangeError(f'{arg} is out of acceptable range')
    
        return True
        
class Date(Field):
    def __init__(self, name: str, label: str):
        super().__init__(name, label)
        
    @classmethod
    def validate(cls, date_text: str):
        try:
            datetime.strptime(date_text, '%Y%m%d')
        except TypeError:
            raise TypeError('Wrong data type, should be string')
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYYMMDD")
        
class Category(Field):
    def __init__(self, name: str, label: str):
        super().__init__(name, label)
        
    @classmethod
    def validate(cls, arg, conditions):
        if arg not in conditions:
            raise InvalidDataError('Role or category not found')
            
        
