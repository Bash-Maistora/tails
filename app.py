from flask import Flask, render_template
import json
import requests


app = Flask(__name__)

API_KEY = 'AIzaSyCV631obrLDLfNHcDJmohRae8aMntavOd4'


@app.route('/', methods=['GET', 'POST'])
def index():
    stores = json.load(open('stores.json'))

    postcodes = [store['postcode'] for store in stores]
    r = requests.post('http://api.postcodes.io/postcodes', data={'postcodes': postcodes})
    results = r.json()

    for entry in results['result']:
        for store in stores:
            if entry['result'] is not None:
                if store['postcode'] == entry['result']['postcode']:
                    store['longitude'] = entry['result']['longitude']
                    store['latitude'] = entry['result']['latitude']

    ordered = sorted(stores, key=lambda k: k['name'])
    store = [entry for entry in results['result'] if entry['result'] is None]

    return render_template('index.html', stores=ordered, API_KEY=API_KEY)
