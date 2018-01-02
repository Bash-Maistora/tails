from flask import Flask, render_template
import json


app = Flask(__name__)


@app.route('/')
def index():
    data = json.load(open('stores.json'))
    result = data[0]['name']
    return result
