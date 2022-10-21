from contextlib import nullcontext
from inspect import _void
from typing import Collection
from flask import Flask, jsonify, json, request
import os
import pymongo
from pymongo import MongoClient, InsertOne
from bson import json_util
from collections.abc import Collection, Mapping

app = Flask(__name__)

client = pymongo.MongoClient('127.0.0.1:27017')
db = client.statTheSpire
characters = {'DEFECT' : db.defect,
              'SILENT': db.silent,
              'IRONCLAD': db.ironclad,
              'WATCHER': db.watcher}

@app.route("/createdb")
def createdb() -> str: 
    client = pymongo.MongoClient('127.0.0.1:27017')
    db = client.statTheSpire
    [populate_collection(v, k) for k,v in characters]
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
def get_runs():
    params = request.form.to_dict()
    print(params)
    params = apply_recursive(convert_if_numeric, params)
    params = apply_recursive(convert_if_bool, params)
    print(params)

    result = []
    if 'character' in params:
        collection = characters[params.pop('character')]
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
    return int(val) if val.isnumeric() else val

def convert_if_bool(val):
    return True if val == "true" else False if val == "false" else val
