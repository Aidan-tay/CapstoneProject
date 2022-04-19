from flask import Flask, render_template, request
import model
import storage

app = Flask(__name__)
models = {str(model.Club): model.Club, str(model.Activity): model.Activity}
relationships = {str(model.Club): model.Membership, str(model.Activity): model.Participation}

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
    form = dict(request.form)
    
    entity_type = form["entity_type"]
    field_labels = models[entity_type].fields_as_dict()
    field_inputs = {}
    for key in field_labels.keys():
        if form.get(key) != None:
           field_inputs[key] = form.get(key)
        
    return render_template("add_create.html", entity_type=entity_type, field_labels = field_labels, field_inputs = field_inputs)

@app.route("/add/result", methods=['POST', 'GET'])
def add_result():
    form = dict(request.form)
    
    entity_type = form.pop("entity_type")
    error = None
    field_inputs = form
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
    entity_type = request.form["entity_type"]
    entity_list = storage.find_all(entity_type, field="name")
    
    return render_template("view_select.html", entity_type = entity_type, entity_list = entity_list)

@app.route("/view/result", methods=['GET'])
def view_result():
    return render_template("view_result.html", field_attributes = storage.find_one(request.form["entity_type"], name = request.form["name"]))

@app.route("/edit/select/type", methods=['POST', 'GET'])
def edit_select_type():
    return render_template("edit_select_type.html", entity_names=models.keys())

@app.route("/edit/select/name", methods=['POST', 'GET'])
def edit_select_name():
    entity_type = request.form["entity_type"]
    entity_list = storage.find_all(entity_type, field="name")

    return render_template("edit_select_name.html", entity_type=entity_type, entity_list=entity_list)

@app.route("/edit/select/confirm", methods=['POST', 'GET'])
def edit_select_confirm():
    entity_type = request.form["entity_type"]
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
    
    form["student_id"] = storage.find_one("Student", name=name)["id"]
    form[f"{entity_type.lower()}_id"] = id

    error = None
    try:
        record = relationships[entity_type].from_dict(form)
    except Exception as e:
        error = e

    if error == None:
        storage.insert(str(relationships[entity_type]), record.as_dict())
        
    return render_template("edit_add_result.html", entity_type=entity_type, id=id, error = error, field_inputs=field_inputs)

@app.route("/edit/student", methods=['POST', 'GET'])
def edit_student():
    entity_type = request.args["type"]
    id = request.args["id"]
    student_list = storage.find_all("Student", field="name")
    
    return render_template("edit_student.html", entity_type=entity_type, id=id, student_list=student_list)

@app.route("/edit/relationship", methods=['POST', 'GET'])
def edit_relationship():
    entity_type = request.args["type"]
    id = request.args["id"]
    name = request.form["name"]
    field_labels = relationships[entity_type].fields_as_dict()
    
    student_id = storage.find_one("Student", name=name)["id"]
    data = storage.findone(str(relationships[entity_type]), **{"student_id":student_id, f"{entity_type.lower()}_id":id})

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
            storage.update(str(relationships[entity_type]), record.as_dict(), **{"student_id":student_id, f"{entity_type.lower()}_id":id})

    elif action == "Delete":
        storage.delete(str(relationships[entity_type]), **{"student_id":student_id, f"{entity_type.lower()}_id":id})
    
    return render_template("edit_result.html", entity_type=entity_type, id=id, name=name)
