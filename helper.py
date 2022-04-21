import storage

def view_student(field_attributes):
    field_attributes["class"] = storage.find_one("Class", id=field_attributes.pop("class_id"))

    subject_list = storage.find_some("Student-Subject", student_id = field_attributes.pop("id"))
    subject_list = [storage.find_one("Subject", id=x["subject_id"])["name"] for x in subject_list]
    field_attributes["subjects"] = subject_list
    
def view_class(field_attributes):
    student_list = storage.find_some("Student", class_id = field_attributes.pop("id"))
    student_list = [x["name"] for x in student_list]
    field_attributes["students"] = student_list

def view_club(field_attributes):
    student_list = storage.find_some("Membership", club_id = field_attributes.pop("id"))
    student_list = [storage.find_one("Student", id=x["student_id"])["name"] for x in student_list]
    field_attributes["students"] = student_list

def view_activity(field_attributes):
    student_list = storage.find_some("Participation", activity_id = field_attributes.pop("id"))
    student_list = [storage.find_one("Student", id=x["student_id"])["name"] for x in student_list]
    field_attributes["students"] = student_list
    