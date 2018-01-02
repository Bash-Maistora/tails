from flask import Flask, render_template
import json


app = Flask(__name__)


@app.route('/')
def index():
    stores = json.load(open('stores.json'))
    ordered = sorted(stores, key=lambda k: k['name'])
    return render_template('index.html', stores=ordered)
