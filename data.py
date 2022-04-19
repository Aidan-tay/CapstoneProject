class Field:
    
    def __init__(self, name, label):
        self.name = name
        self.label = label

    def __repr__(self):
        return (
            f'{self.__class__.__name__}('
            f'name="{self.name}", '
            f'label="{self.label}"'
            ')'
        )

    def validate(self):
        pass

class String(Field):

    def validate(self, value):
        if value == "":    # presence check
            return False
        
        return isinstance(self, str)    # type check


class Integer(Field):

    def validate(self, value):
        if value == "":    # presence check
            return False
        
        return isinstance(value, int)    # type check


class Age(Field):

    def validate(self, value):
        if value == "":    # presence check
            return False
        elif not isinstnace(value, int):    # type check
            return False
        elif 0 < value < 100:    # range check
            return False
        else:
            return True


class Year(Field):

    def validate(self, value):
        if value == "":    # presence check
            return False
        elif not isinstance(value, int):    # type check
            return False
        elif 2000 < year < 2100:   # range check
            return False
        else:
            return True


class Date(Field):
    """
    Dates are in the format yyyymmdd
    """
    
    def validate(self, value):
        if value == "":    # presence check
            return False
        elif not isinstance(value, int):    # type check
            return False
        elif (2000 < value // 10000 < 2100) and (1 <= value % 100 <= 31) and (1 <= value // 100 & 100 <= 12):   # length check
            return True 
        else:
            return False


class Category(String):

    def __init__(self, name, label, default):
        self.name = name
        self.label = label
        self.default = default
        