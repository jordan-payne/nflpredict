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
    payload = json.loads(request.data)
    last_name = payload['last_name']
    first_name = payload['first_name']
    team = payload['team']
    stats = nflanalyze.get_player(last_name, first_name, team)
    if stats == None:
        return nflanalyze.to_json({'message': 'not found'})
    return to_json(stats)

@app.route('/get_team_roster', methods=['POST'])
def get_team_roster():
    payload = json.loads(request.data)
    team = payload['team']
    roster = nflanalyze.get_team_roster(team)
    return to_json(roster)

def to_json(obj):
    return json.dumps(to_basic_obj(obj))

def to_basic_obj(obj):
    try:
        collection = {}
        for f in obj.sql_fields():
            if f == 'status' or f == 'position':
                collection[f] = str(getattr(obj, f))
            else:
                collection[f] = getattr(obj, f)
    except AttributeError:
        try:
            collection = {}
            for i in obj:
                if i != 'status':
                    collection[i] = obj[i]
                if i == 'status':
                    collection[i] = str(obj[i])
                if i == 'position':
                    collection[i] = str(obj[i])
        except TypeError:
            collection = []
            for o in obj:
                collection.append(to_basic_obj(o))
    return collection


if __name__ == "__main__":
    app.run()
