import data

class Record:
    fields = None
    name = None
    def __init__(self, **kwargs):
        '''
        Validates and creates an instance of the object with fields specified
        '''
        for field in self.fields:
            value = kwargs[field.name]
            field.validate(value)
            setattr(self, field.name, value)

    @classmethod
    def from_dict(cls, dict):
        '''
        Converts a dictionary to a instance of the class
        '''
        return cls(**dict)

    def as_dict(self):
        '''
        Convert class to a dictionary
        '''
        fields_dict = {}
        for field in self.fields:
            fields_dict[field.name] = getattr(self, field.name)
        return fields_dict

    @classmethod
    def fields_as_dict(cls):
        '''
        Convert the fields to a dictionary, excluding any id attributes.
        key: field variable name
        value: field label
        '''
        fields_dict = {}
        for field in cls.fields:
            if field.label != "ID":
                fields_dict[field.name] = field.label
        return fields_dict

    def get(self, attr):
        '''
        Get the value of the specified attribute
        '''
        return getattr(self, attr)
                
class Club(Record):
    fields = [data.Integer("id","ID"), data.String("name", "Name of Club")]
    name = "Club"

    def __str__(self):
        return "Club"

    
class Activity(Record):
    fields = [data.Integer("id","ID"), data.String("name", "Name of Activity"), data.Date("start_date", "Start Date"), data.OptionalDate("end_date", "End Date (Optional)"), data.String("description", "Description")]
    name = "Activity"

    def __str__(self):
        return "Activity"
    
class Membership(Record):
    fields = [data.Integer("student_id", "ID"), data.Integer("club_id", "ID"), data.String("role", "Role of Member")]
    name = "Membership"

    def __str__(self):
        return "Membership"

class Participation(Record):
    fields = [data.Integer("student_id", "ID"), data.Integer("activity_id", "ID"), data.Category("category","Category"), data.String("role", "Role of Member"), data.OptionalString("award", "Award (Optional)"), data.OptionalInteger("hours", "Hours (Optional)")]
    name = "Participation"

    def __str__(self):
        return "Participation"