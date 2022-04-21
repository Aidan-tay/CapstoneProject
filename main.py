from flask import Flask, render_template, request
import model
import storage

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
    entity_type = request.args["type"]
    form = dict(request.form)

    field_labels = models[entity_type].fields_as_dict()
    field_inputs = {}
    for key in field_labels.keys():
        if form.get(key) != None:
           field_inputs[key] = form.get(key)
            
    return render_template("add_create.html", entity_type = entity_type, field_labels = field_labels, field_inputs = field_inputs)

@app.route("/add/result", methods=['POST', 'GET'])
def add_result():
    entity_type = request.args["type"]
    form = dict(request.form)

    id = None
    error = None
    field_inputs = form
    if storage.find_lastest_id(entity_type) == None:
        form["id"] = 0
    else:
        form["id"] = storage.find_lastest_id(entity_type) + 1

    try:
        record = models[entity_type].from_dict(form)
    except Exception as e:
        error = e

    if error == None:
        id = record.get("id")
        storage.insert(entity_type, record.as_dict())

    return render_template("add_result.html", id = id, field_inputs = field_inputs, error = error, entity_type = entity_type)

@app.route("/view", methods=['POST', 'GET'])
def view():
    return render_template("view.html", entity_names = ["Student", "Class", "Club", "Activity"])

@app.route("/view/select", methods=['POST', 'GET'])
def view_select():
    entity_type = request.args["type"]
    entity_list = storage.find_all(entity_type, field="name")
    
    return render_template("view_select.html", entity_type = entity_type, entity_list = entity_list)

@app.route("/view/result", methods=['GET'])
def view_result():
    entity_type = request.args["type"]
    field_attributes = storage.find_one(entity_type, name = request.form["name"])

    if entity_type == "Student":
        field_attributes["class"] = storage.find_one("Class", id=field_attributes.pop("class_id"))
        
        subject_list = storage.find_some("Student-Subject", student_id = field_attributes.pop("id"))
        subject_list = [storage.find_one("Subject", id=x["subject_id"])["name"] for x in subject_list]
        field_attributes["subjects"] = subject_list

    elif entity_type == "Class":
        student_list = storage.find_some("Student", class_id = field_attributes.pop("id"))
        student_list = [x["name"] for x in student_list]
        field_attributes["students"] = student_list

    elif entity_type == "Club":
        student_list = storage.find_some("Membership", student_id = field_attributes.pop("id"))
        student_list = [storage.find_one("Student", id=x["student_id"])["name"] for x in student_list]
        field_attributes["students"] = student_list

    elif entity_type == "Activity":
        student_list = storage.find_some("Participation", student_id = field_attributes.pop("id"))
        student_list = [storage.find_one("Student", id=x["student_id"])["name"] for x in student_list]
        field_attributes["students"] = student_list
        
    return render_template("view_result.html", field_attributes = field_attributes)

@app.route("/edit/select/type", methods=['POST', 'GET'])
def edit_select_type():
    return render_template("edit_select_type.html", entity_names=models.keys())

@app.route("/edit/select/name", methods=['POST', 'GET'])
def edit_select_name():
    entity_type = request.args["type"]
    entity_list = storage.find_all(entity_type, field="name")

    return render_template("edit_select_name.html", entity_type=entity_type, entity_list=entity_list)

@app.route("/edit/select/confirm", methods=['POST', 'GET'])
def edit_select_confirm():
    entity_type = request.args["type"]
    field_attributes = storage.find_one(entity_type, name = request.form["name"])
    id = field_attributes.pop("id")

    return render_template("edit_select_name.html", entity_type=entity_type, field_attributes=field_attributes, id=id)

@app.route("/edit", methods=['POST', 'GET'])
def edit():
    entity_type = request.args["type"]
    id = request.args["id"]
    
    return render_template("edit.html", entity_type=entity_type, id=id)

@app.route("/edit/add", methods=['POST', 'GET'])
def edit_add():
    entity_type = request.args["type"]
    id = request.args["id"]
    student_list = storage.find_all("Student", field="name")
    field_labels = relationships[entity_type].fields_as_dict()

    form = dict(request.form)
    field_inputs = {}
    for key in field_labels.keys():
        if form.get(key) != None:
           field_inputs[key] = form.get(key)

    return render_template("edit_add.html", entity_type=entity_type, id=id, field_labels=field_labels, field_inputs=field_inputs, student_list=student_list)

@app.route("/edit/add/result", methods=['POST', 'GET'])
def edit_add_result():
    entity_type = request.args["type"]
    id = request.args["id"]

    form = dict(request.form)
    name = form.pop("name")
    field_inputs = form

    student_id_list = storage.find_some(relationships[entity_type].name, **{f"{entity_type.lower()}_id":id})
    student_id_list = [x["student_id"] for x in student_id_list]
    
    form["student_id"] = storage.find_one("Student", name=name)["id"]
    form[f"{entity_type.lower()}_id"] = id

    error = None
    try:
        if form["student_id"] in student_id_list:
            raise TypeError(f"{name} is already in {entity_type}.")
        record = relationships[entity_type].from_dict(form)
    except Exception as e:
        error = e

    if error == None:
        storage.insert(relationships[entity_type].name, record.as_dict())
        
    return render_template("edit_add_result.html", entity_type=entity_type, id=id, error = error, field_inputs=field_inputs)

@app.route("/edit/student", methods=['POST', 'GET'])
def edit_student():
    entity_type = request.args["type"]
    id = request.args["id"]
    
    student_id_list = storage.find_some(relationships[entity_type].name, **{f"{entity_type.lower()}_id":id})
    student_id_list = [x["student_id"] for x in student_id_list]
    
    student_list = []
    for student_id in student_id_list:
        student_list.append(storage.find_one("Student", id=student_id)["name"])
    
    return render_template("edit_student.html", entity_type=entity_type, id=id, student_list=student_list)

@app.route("/edit/relationship", methods=['POST', 'GET'])
def edit_relationship():
    entity_type = request.args["type"]
    id = request.args["id"]
    name = request.form["name"]
    field_labels = relationships[entity_type].fields_as_dict()
    
    student_id = storage.find_one("Student", name=name)["id"]
    data = storage.findone(relationships[entity_type].name, **{"student_id":student_id, f"{entity_type.lower()}_id":id})

    field_inputs = {}
    for key in field_labels.keys():
        field_inputs[key] = data.get(key)
    
    return render_template("edit_relationship.html", entity_type=entity_type, id=id, name=name, field_labels=field_labels, field_inputs=field_inputs)

@app.route("/edit/result", methods=['POST', 'GET'])
def edit_result():
    entity_type = request.args["type"]
    id = request.args["id"]
    form = dict(request.form)
    name = form.pop("name")
    action = form.pop("action")
    student_id = storage.find_one("Student", name=name)["id"]

    error = None
    if action == "Edit":
        form["student_id"] = student_id
        form[f"{entity_type.lower()}_id"] = id
        
        try:
            record = relationships[entity_type].from_dict(form)
        except Exception as e:
            error = e

        if error == None:
            storage.update(relationships[entity_type].name, record.as_dict(), **{"student_id":student_id, f"{entity_type.lower()}_id":id})

    elif action == "Delete":
        storage.delete(relationships[entity_type].name, **{"student_id":student_id, f"{entity_type.lower()}_id":id})
    
    return render_template("edit_result.html", entity_type=entity_type, id=id, name=name)




########FRONTPRAWN RANDOM SHIT JS IGNORE IF I FORGOT DELETE BEFORE MERGE######    

app.run("0.0.0.0")