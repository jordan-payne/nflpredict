#!/usr/bin/env python

import nflanalyze

from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
from flask import json

app = Flask(__name__)



@app.route('/')
def index():
    return redirect(url_for('static', filename='index.html'))

@app.route('/get_player', methods=['POST'])
def get_player():
    print type(request.data)
    payload = json.loads(request.data)
    print payload
    last_name = payload['last_name']

    first_name = payload['first_name']
    team = payload['team']
    stats = nflanalyze.get_player(last_name, first_name, team)
    return nflanalyze.to_json(stats)

if __name__ == "__main__":
    app.run()
