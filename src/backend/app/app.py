from contextlib import nullcontext
from inspect import _void
from typing import Collection
from flask import Flask, jsonify, json, request
import os
import pymongo
from pymongo import MongoClient, InsertOne
from bson import json_util
from collections.abc import Collection, Mapping
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
#app.config['CORS_HEADERS'] = 'Content-Type'

client = pymongo.MongoClient('127.0.0.1:27017')
db = client.statTheSpire
characters = {'DEFECT' : db.defect,
              'SILENT': db.silent,
              'IRONCLAD': db.ironclad,
              'WATCHER': db.watcher}

@app.route("/createdb")
def createdb() -> str: 
    client = pymongo.MongoClient('127.0.0.1:27017')
    client.drop_database('statTheSpire')
    db = client.statTheSpire
    for k,v in characters.items():
        populate_collection(v, k)
    client.close()
    return "creation succesful"

#Populates mongo with runs currently in runs folder
def populate_collection(collection: Collection, name: str) -> None:
    requesting: list[InsertOne] = []
    dir: str = os.path.join(app.static_folder, 'runs', name)
    with os.scandir(dir) as runs:
        for file in runs:
            if file.name.endswith(".run") and file.is_file():
                with open(file) as run:
                    requesting.append(InsertOne(json.load(run)))

    result = collection.bulk_write(requesting)

#reading a run
@app.route("/arun")
def a_run():
    filename = os.path.join(app.static_folder, 'runs', 'DEFECT', '1635940394.run')
    with open(filename) as f:
        run =  json.load(f)
    return run

#inserting
@app.route("/ins")
def ins(): 
    collection = db.defect
    requesting = []

    filename = os.path.join(app.static_folder, 'runs', 'DEFECT', '1635940394.run')
    with open(filename) as f:
            myDict = json.load(f)
            requesting.append(InsertOne(myDict))

    result = collection.bulk_write(requesting)
    client.close()
    return {}

#by ascension

#by victory

#by character

@app.route("/runs", methods=['POST'])
@cross_origin()
def get_runs():
    #params = request.form.to_dict()
    params = request.get_json()
    print(params)
    params = apply_recursive(convert_if_numeric, params)
    #params = apply_recursive(convert_if_bool, params)

    result = []
    if 'character' in params:
        collection = characters[params.pop('character')]
        print(params)
        result =  get_query(collection, params)
    else:
        for char in list(characters.values()):
            result += (get_query(char, params))
    print(len(result))
    return result

def get_query(col, params):
    result = col.find(params)
    json_with_backslash = json_util.dumps(result)
    formatted_json = json.loads(json_with_backslash)
    return formatted_json

#apply func recursively to object dict
def apply_recursive(func, obj):
    if isinstance(obj, dict):  # if dict, apply to each key
        print("in dict")
        return {k: apply_recursive(func, v) for k, v in obj.items()}
    elif isinstance(obj, list):  # if list, apply to each element
        print("in_list")
        return [apply_recursive(func, elem) for elem in obj]
    else:
        print("at leaf: " + str(obj) +" of type: " + str(type(obj)) + "/" + str(type(func(obj))))
        return func(obj)

def convert_if_numeric(val):
    if isinstance(val, int) or isinstance(val, float):
        return val
    #attempting to catch floats, may have to revise
    elif val.replace('.', '').isdigit():
        return float(val)
    elif val.isdigit():
        return int(val)
    return val

def convert_if_bool(val):
    return True if val == "true" else False if val == "false" else val
