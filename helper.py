import storage

def view_student(field_attributes):
    '''
    Converts class_id to class name and id to a list of subject names, club names and activity names
    '''
    field_attributes["class"] = storage.find_one("Class", id=field_attributes.pop("class_id"))["name"]

    _id = field_attributes.pop("id")
    subject_list = storage.find_some("Student-Subject", student_id = _id)
    subject_list = [storage.find_one("Subject", id=x["subject_id"])["name"] for x in subject_list]
    field_attributes["Subjects"] = subject_list

    club_list = storage.find_some("Membership", student_id = _id)
    club_list = [storage.find_one("Club", id=x["club_id"])["name"] for x in club_list]
    field_attributes["Clubs"] = club_list

    activity_list = storage.find_some("Participation", student_id = _id)
    activity_list = [storage.find_one("Activity", id=x["activity_id"])["name"] for x in activity_list]
    field_attributes["Activities"] = activity_list
    
def view_class(field_attributes):
    '''
    Converts id to a list of student names in the class
    '''
    student_list = storage.find_some("Student", class_id = field_attributes.pop("id"))
    student_list = [x["name"] for x in student_list]
    field_attributes["students"] = student_list

def view_club(field_attributes):
    '''
    Converts id to a list of student names in the club
    '''
    student_list = storage.find_some("Membership", club_id = field_attributes.pop("id"))
    student_list = [storage.find_one("Student", id=x["student_id"])["name"] for x in student_list]
    field_attributes["students"] = student_list

def view_activity(field_attributes):
    '''
    Converts id to a list of student names in the activity
    '''
    student_list = storage.find_some("Participation", activity_id = field_attributes.pop("id"))
    student_list = [storage.find_one("Student", id=x["student_id"])["name"] for x in student_list]
    field_attributes["students"] = student_list
    