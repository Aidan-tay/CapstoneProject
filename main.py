from flask import Flask, render_template, request
import model
import storage
import helper

app = Flask(__name__) 

models = {model.Club.name: model.Club, model.Activity.name: model.Activity}
relationships = {model.Club.name: model.Membership, model.Activity.name: model.Participation}

@app.route("/", methods=['GET'])
def splash():
    return render_template("splash.html")


@app.route("/index", methods=['POST', 'GET'])
def index():
    return render_template("index.html")


@app.route("/add", methods=['POST', 'GET'])
def add():
    return render_template("add.html", entity_list=models.keys())


@app.route("/add/create", methods=['POST', 'GET'])
def add_create():
    #get type of entity from args and its field names and labels
    entity_type = request.args["type"]
    field_labels = models[entity_type].fields_as_dict()

    # Using the field names, get the respective values from request.form
    form = dict(request.form)
    field_inputs = {}
    for key in field_labels.keys():
        if form.get(key) != None:
           field_inputs[key] = form.get(key)
            
    return render_template("add_create.html", entity_type = entity_type, field_labels = field_labels, field_inputs = field_inputs)


@app.route("/add/result", methods=['POST', 'GET'])
def add_result():
    #get type of entity from args
    entity_type = request.args["type"]

    #save the user inputs from request.form
    form = dict(request.form)
    field_inputs = form

    id = None
    error = None

    # find the id of the new entity by incrementing the highest id
    if storage.find_latest_id(entity_type) == None:
        form["id"] = 1
    else:
        form["id"] = storage.find_latest_id(entity_type) + 1

    # validate the inputs using the respective class and catch and save any errors
    try:
        record = models[entity_type].from_dict(form)
        if record.get("name") in storage.find_all(entity_type, field="name"):
            raise NameError(f"{record.get('name')} already exists.")
    except Exception as e:
        error = e

    #if there is no error with the inputs save it into the database
    if error == None:
        id = record.get("id")
        storage.insert(entity_type, record.as_dict())

    return render_template("add_result.html", id = id, field_inputs = field_inputs, error = error, entity_type = entity_type)


@app.route("/view", methods=['POST', 'GET'])
def view():
    return render_template("view.html", entity_names = ["Student", "Class", "Club", "Activity"])


@app.route("/view/select", methods=['POST', 'GET'])
def view_select():
    # get the entity type and find all instances of it in the database
    entity_type = request.args["type"]
    entity_list = storage.find_all(entity_type, field="name")
    entity_list.sort()
    
    return render_template("view_select.html", entity_type = entity_type, entity_list = entity_list)

@app.route("/view/result", methods=['GET', 'POST'])
def view_result():
    # get the entity type and the entity that matches the name selected
    entity_type = request.form["entity_type"]
    field_attributes = storage.find_one(entity_type, name = request.form["name"])

    # replace foreign ids with respective student/class/club/activity names 
    if entity_type == "Student":
        helper.view_student(field_attributes)

    elif entity_type == "Class":
        helper.view_class(field_attributes)

    elif entity_type == "Club":
        helper.view_club(field_attributes)

    elif entity_type == "Activity":
        helper.view_activity(field_attributes)

    return render_template("view_result.html", field_attributes = field_attributes, isinstance = isinstance, list = list)


@app.route("/edit/select/type", methods=['POST', 'GET'])
def edit_select_type():
    return render_template("edit_select_type.html", entity_names=models.keys())


@app.route("/edit/select/name", methods=['POST', 'GET'])
def edit_select_name():
    # get the entity type and names of all the instances of that type
    entity_type = request.args["type"]
    entity_list = storage.find_all(entity_type, field="name")
    entity_list.sort()

    return render_template("edit_select_name.html", entity_type=entity_type, entity_list=entity_list)


@app.route("/edit/select/confirm", methods=['POST', 'GET'])
def edit_select_confirm():
    # get the entity type and the entity that matches the name selected
    entity_type = request.args["type"]
    field_attributes = storage.find_one(entity_type, name = request.form["name"])
    id = field_attributes["id"]

    # replace foreign ids with respective names
    if entity_type == "Club":
        helper.view_club(field_attributes)

    elif entity_type == "Activity":
        helper.view_activity(field_attributes)

    return render_template("edit_select_confirm.html", entity_type=entity_type, field_attributes=field_attributes, id=id, isinstance=isinstance, list=list)


@app.route("/edit", methods=['POST', 'GET'])
def edit():
    # get entity type and id
    entity_type = request.args["type"]
    id = request.args["id"]
    
    return render_template("edit.html", entity_type=entity_type, id=id)


@app.route("/edit/add", methods=['POST', 'GET'])
def edit_add():
    # get entity type, its labels and id
    entity_type = request.args["type"]
    id = request.args["id"]
    field_labels = relationships[entity_type].fields_as_dict()

    # get all student names
    student_list = storage.find_all("Student", field="name")

    # add default values
    field_inputs = {}
    if entity_type == "Club":
        field_inputs["role"] = "Member"
    elif entity_type == "Activity":
        field_inputs["role"] = "Participant"
    
    # get user inputs from request.form
    form = dict(request.form)
    for key in field_labels.keys():
        if form.get(key) != None:
           field_inputs[key] = form.get(key)

    return render_template("edit_add.html", entity_type=entity_type, id=id, field_labels=field_labels, field_inputs=field_inputs, student_list=student_list)


@app.route("/edit/add/result", methods=['POST', 'GET'])
def edit_add_result():
    # get entity type and id
    entity_type = request.args["type"]
    id = request.args["id"]

    # get the name and user inputs
    form = dict(request.form)
    name = form.pop("name")
    field_inputs = form

    # get a list of student ids that are in the club/activity
    student_id_list = storage.find_some(relationships[entity_type].name, **{f"{entity_type.lower()}_id":id})
    student_id_list = [x["student_id"] for x in student_id_list]

    # store the id of the club/activity and the id of student selected
    form["student_id"] = storage.find_one("Student", name=name)["id"]
    form[f"{entity_type.lower()}_id"] = id

    error = None
    try:
        # give an error if student is already in club/activity
        if form["student_id"] in student_id_list:
            raise TypeError(f"{name} is already in {entity_type}.")

        # validate the data through the class
        record = relationships[entity_type].from_dict(form)
    except Exception as e:
        error = e

    # if there is no error store it in database
    if error == None:
        storage.insert(relationships[entity_type].name, record.as_dict())
        
    return render_template("edit_add_result.html", entity_type=entity_type, id=id, error = error, field_inputs=field_inputs)


@app.route("/edit/student", methods=['POST', 'GET'])
def edit_student():
    # get entity type and id
    entity_type = request.args["type"]
    id = request.args["id"]

    # get a list of student ids that are in the club/activity
    student_id_list = storage.find_some(relationships[entity_type].name, **{f"{entity_type.lower()}_id":id})
    student_id_list = [x["student_id"] for x in student_id_list]

    #convert the list to a list of student names
    student_list = []
    for student_id in student_id_list:
        student_list.append(storage.find_one("Student", id=student_id)["name"])
    
    return render_template("edit_student.html", entity_type=entity_type, id=id, student_list=student_list)


@app.route("/edit/relationship", methods=['POST', 'GET'])
def edit_relationship():
    # get entity type and id
    entity_type = request.args["type"]
    id = request.args["id"]

    # get student name and label
    name = request.form["name"]
    field_labels = relationships[entity_type].fields_as_dict()

    # get student id and find its relationship record in the database
    student_id = storage.find_one("Student", name=name)["id"]
    data = storage.find_one(relationships[entity_type].name, **{"student_id":student_id, f"{entity_type.lower()}_id":id})

    #get field inputs from request.form
    field_inputs = {}
    for key in field_labels.keys():
        field_inputs[key] = data.get(key)
    
    return render_template("edit_relationship.html", entity_type=entity_type, id=id, name=name, field_labels=field_labels, field_inputs=field_inputs)


@app.route("/edit/result", methods=['POST', 'GET'])
def edit_result():
    # get entity type and id
    entity_type = request.args["type"]
    id = request.args["id"]

    # get student name, action, field_inputs and student id
    form = dict(request.form)
    name = form.pop("name")
    action = form.pop("action")
    field_inputs = form
    student_id = storage.find_one("Student", name=name)["id"]

    error = None
    if action == "Edit":
        #validate any inputs and catch any errors
        form["student_id"] = student_id
        form[f"{entity_type.lower()}_id"] = id
        
        try:
            record = relationships[entity_type].from_dict(form)
        except Exception as e:
            error = e

        # if there are no errors, update the database
        if error == None:
            storage.update(relationships[entity_type].name, record.as_dict(), **{"student_id":student_id, f"{entity_type.lower()}_id":id})

    elif action == "Delete":
        # delete the specified record
        storage.delete(relationships[entity_type].name, **{"student_id":student_id, f"{entity_type.lower()}_id":id})

    return render_template("edit_result.html", entity_type=entity_type, id=id, name=name, field_inputs=field_inputs, error=error)


@app.route("/delete", methods=['POST', 'GET'])
def delete():
    return render_template("delete.html", entity_list=models.keys())


@app.route("/delete/select", methods=['POST', 'GET'])
def delete_select():
    # get the entity type and find all instances of it in the database
    entity_type = request.args["type"]
    entity_list = storage.find_all(entity_type, field="name")
    entity_list.sort()
    
    return render_template("delete_select.html", entity_type=entity_type, entity_list=entity_list)


@app.route("/delete/result", methods=['POST', 'GET'])
def delete_result():
    # get the entity type and name
    name = request.form["name"]
    entity_type = request.form["entity_type"]

    #delete the entity and its relationships
    storage.delete(relationships[entity_type].name, **{f"{entity_type.lower()}_id": storage.find_one(entity_type, name=name)["id"]})
    storage.delete(entity_type, name=name)

    return render_template("delete_result.html")

app.run("0.0.0.0")