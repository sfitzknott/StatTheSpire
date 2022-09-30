from flask import Flask, jsonify, json
import os
import pymongo
from pymongo import MongoClient, InsertOne

app = Flask(__name__)

@app.route("/arun")
def a_run():
    filename = os.path.join(app.static_folder, 'runs', 'DEFECT', '1635940394.run')
    with open(filename) as f:
        run =  json.load(f)
    return run


@app.route("/ins")
def ins(): 
    client = pymongo.MongoClient('127.0.0.1:27017')
    db = client.statTheSpire
    collection = db.defect
    requesting = []

    filename = os.path.join(app.static_folder, 'runs', 'DEFECT', '1635940394.run')
    with open(filename) as f:
            myDict = json.load(f)
            requesting.append(InsertOne(myDict))

    result = collection.bulk_write(requesting)
    client.close()
    return {}