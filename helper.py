import storage

def view_student(field_attributes):
    '''
    Cleans up the field_attributes to be more user friendly as well as converting any foreign keys to their respective names / list of names
    '''
    # class_id to class name
    field_attributes["Class"] = storage.find_one("Class", id=field_attributes.pop("class_id"))["name"]

    # id to subjects
    _id = field_attributes.pop("id")
    subject_list = storage.find_some("Student-Subject", student_id = _id)
    subject_list = [storage.find_one("Subject", id=x["subject_id"])["name"] for x in subject_list]
    field_attributes["Subjects"] = subject_list

    # id to clubs
    club_list = storage.find_some("Membership", student_id = _id)
    club_list = [storage.find_one("Club", id=x["club_id"])["name"] for x in club_list]
    field_attributes["Clubs"] = club_list

    # id to activities
    activity_list = storage.find_some("Participation", student_id = _id)
    activity_list = [storage.find_one("Activity", id=x["activity_id"])["name"] for x in activity_list]
    field_attributes["Activities"] = activity_list

    # change the fields into its label
    field_label = {"name": "Name", "age": "Age", "year_enrolled": "Year Enrolled", "graduating_year": "Graduating Year"}
    for field, label in field_label.items():
        field_attributes[label] = field_attributes.pop(field)
    
def view_class(field_attributes):
    '''
    Cleans up the field_attributes to be more user friendly as well as converting any foreign keys to their respective names / list of names
    '''
    # id to students
    student_list = storage.find_some("Student", class_id = field_attributes.pop("id"))
    student_list = [x["name"] for x in student_list]
    field_attributes["Students"] = student_list

    # change the fields into its label
    field_label = {"name": "Name", "level": "Level"}
    for field, label in field_label.items():
        field_attributes[label] = field_attributes.pop(field)

def view_club(field_attributes):
    '''
    Cleans up the field_attributes to be more user friendly as well as converting any foreign keys to their respective names / list of names
    '''
    # id to students
    club_id = field_attributes.pop("id")
    student_list = storage.find_some("Membership", club_id = club_id)
    student_list = [storage.find_one("Student", id=x["student_id"])["name"] + " " + f"({storage.find_one('Membership', student_id=x['student_id'], club_id = club_id)['role']})" for x in student_list]
    field_attributes["Students"] = student_list

    # change the fields into its label
    field_label = {"name": "Name"}
    for field, label in field_label.items():
        field_attributes[label] = field_attributes.pop(field)

def view_activity(field_attributes):
    '''
    Cleans up the field_attributes to be more user friendly as well as converting any foreign keys to their respective names / list of names
    '''
    # id to students
    activity_id = field_attributes.pop("id")
    student_list = storage.find_some("Participation", activity_id = activity_id)
    student_list = [storage.find_one("Student", id=x["student_id"])["name"] + " " + f"({storage.find_one('Participation', student_id=x['student_id'], activity_id=activity_id)['role']})" for x in student_list]
    field_attributes["Students"] = student_list

    # change the fields into its label
    field_label = {"name": "Name", "start_date": "Start Date", "end_date": "End Date", "description": "Description"}
    for field, label in field_label.items():
        field_attributes[label] = field_attributes.pop(field)
    