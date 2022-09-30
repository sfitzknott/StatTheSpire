from typing import Collection
from flask import Flask, jsonify, json
import os
import pymongo
from pymongo import MongoClient, InsertOne

app = Flask(__name__)

client = pymongo.MongoClient('127.0.0.1:27017')
db = client.statTheSpire
characters = {'DEFECT' : db.defect,
              'SILENT': db.silent,
              'IRONCLAD:': db.ironclad,
              'WATCHER': db.watcher}

@app.route("/arun")
def a_run():
    filename = os.path.join(app.static_folder, 'runs', 'DEFECT', '1635940394.run')
    with open(filename) as f:
        run =  json.load(f)
    return run


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

@app.route("/createdb")
def createdb(): 
    client = pymongo.MongoClient('127.0.0.1:27017')
    db = client.statTheSpire
    [populate_collection(v, k) for k,v in characters]
    client.close()
    return "creation succesful"

#Populates mongo with runs currently in runs folder
def populate_collection(collection: Collection, name: str):
    requesting: list[InsertOne] = []
    dir: str = os.path.join(app.static_folder, 'runs', name)
    with os.scandir(dir) as runs:
        for file in runs:
            if file.name.endswith(".run") and file.is_file():
                with open(file) as run:
                    requesting.append(InsertOne(json.load(run)))

    result = collection.bulk_write(requesting)
