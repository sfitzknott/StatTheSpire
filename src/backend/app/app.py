from flask import Flask, jsonify, json
import os
import json

app = Flask(__name__)

@app.route("/arun")
def a_run():
    filename = os.path.join(app.static_folder, 'runs', 'DEFECT', '1635940394.run')
    with open(filename) as f:
        run =  json.load(f)
    return run