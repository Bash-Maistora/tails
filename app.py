from flask import Flask, render_template, request

import json
import requests


app = Flask(__name__)

API_KEY = 'AIzaSyCV631obrLDLfNHcDJmohRae8aMntavOd4'


@app.route('/', methods=['GET', 'POST'])
def index():
    '''Returns list of stores from json on GET
       Returns nearby stores for postcode on POST '''
    stores = json.load(open('stores.json'))
    postcodes = [store['postcode'] for store in stores]

    for store in stores:
        store['name'] = store['name'].replace('_', ' ')

    r = requests.post('http://api.postcodes.io/postcodes', data={'postcodes': postcodes})
    results = r.json()

    for entry in results['result']:
        for store in stores:
            if entry['result'] is not None:
                if store['postcode'] == entry['result']['postcode']:
                    store['longitude'] = entry['result']['longitude']
                    store['latitude'] = entry['result']['latitude']

    ordered = sorted(stores, key=lambda k: k['name'])

    if request.method == 'POST':
        postcode = request.form['postcode']
        outcode = postcode.split()[0]
        r = requests.get('http://api.postcodes.io/outcodes/{}/nearest'.format(outcode))

        if r.json()['status'] == 404:
            error = 'Invalid Postcode!'
            return render_template('index.html', stores=ordered,
                                   API_KEY=API_KEY, error=error)

        results = {entry['outcode']: entry['distance'] for entry in r.json()['result']}

        nearby = []
        for store in stores:
            if store['postcode'].split()[0] in results:
                store['distance'] = results[store['postcode'].split()[0]]
                nearby.append(store)

        ordered = sorted(nearby, key=lambda k: k['distance'])
        return render_template('index.html', stores=ordered, API_KEY=API_KEY)

    return render_template('index.html', stores=ordered, API_KEY=API_KEY)


if __name__ == "__main__":
    app.run()
