def TypeError():
    return 'wrong type for data'
    
class Field:
    def __init__(self, name: str, label: str):
        self.name = name
        self.label = label 

    @classmethod
    def validate(cls): #what am i supposed to validate and what is this function supposed to return
        pass
        
class String(Field):
    def __init__(self, name: str, label: str):
        super().__init__(name, label)
    #validate function same as parent class

    @classmethod #is it supposed to be like this?
    def validate(cls): 
        if type(self.name) != str or type(self.label) != str:
            return TypeError


class Integer(Field):
    def __init__(self, name: str, label: str):
        super().__init__(name, label)

    @classmethod
    def validate(cls):
        pass

class Age(Field):
    def __init__(self, name: str, label: str):
        super().__init__(name, label)

    @classmethod
    def validate(cls, value):
        pass

class Year(Field):
    def __init__(self, name: str, label: str):
        super().__init__(name, label)
        
    @classmethod
    def validate(cls):
        pass
        
class Date(Field):
    def __init__(self, name: str, label: str):
        super().__init__(name, label)
        
    @classmethod
    def validate(cls):
        pass
        
class Role(Field):
    def __init__(self, name: str, label: str):
        super().__init__(name, label)
        
    @classmethod
    def validate(cls):
        pass
        
class Category(Field):
    def __init__(self, name: str, label: str):
        super().__init__(name, label)
        
    @classmethod
    def validate(cls):
        pass
        
