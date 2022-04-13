from flask import Flask, render_template, request
import model
import storage

app = Flask(__name__)
models = {str(model.Club): model.Club, str(model.Activity): model.Activity}

@app.route("/")
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

