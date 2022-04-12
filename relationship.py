import data

class Record:
    fields = None
    def __init__(self, **kwargs):
        for field in self.fields:
            value = kwargs[field.name]
            field.validate(value)
            setattr(self, field.name, value)

    @classmethod
    def from_dict(cls, dict):
        return cls(**dict)

    def as_dict(self):
        fields_dict = {}
        for field in self.fields:
            fields_dict[field.name] = getattr(self, field.name)
        return fields_dict

    def fields_as_dict(self):
        fields_dict = {}
        for field in self.fields:
            fields_dict[field.name] = field.label
        return fields_dict

    def get(self, attr):
        return getattr(self, attr)
                
class Club(Record):
    fields = [data.Integer("id","ID"), data.String("name", "Name of Club")]
    pass
    
class Activity(Record):
    fields = [data.Integer("id","ID"), data.String("name", "Name of Activity"), data.Date("start_date", "Start Date"), data.Date("end_date", "End Date"), data.String("description", "Description")]
    pass
    
class Membership(Record):
    fields = [data.String("role", "Role of Member"), data.Integer("student_id", "Id of Student"), data.Integer("club_id", "Id of Club")]
    pass

class Participation(Record):
    fields = [data.Category("category","Category"), data.String("role", "Role of Member"), data.Integer("student_id", "Id of Student"), data.Integer("activity_id", "Id of Activity")]
    pass