from context import nflinterface

import pytest
import tempfile
from flask import json


@pytest.fixture
def client(request):
    nflinterface.app.config['TESTING'] = True
    client = nflinterface.app.test_client()
    return client

def test_app():
    assert nflinterface.app != None

def test_home(client):
    response = client.get('/', follow_redirects=True)
    print response.data
    assert b'NFL Predict' in response.data

def test_get_player(client):
    payload = {
        'last_name':'Brees',
        'first_name':'Drew',
        'team':'NO'}
    response = client.post('/get_player', data=json.dumps(payload))
    json_data = json.loads(response.data)
    assert json_data['position'] == 'QB'
    assert json_data['status'] == 'Active'
    assert json_data['full_name'] == 'Drew Brees'

def test_get_team_roster(client):
    payload = {
        'team': 'NO'
    }
    response = client.post('/get_team_roster', data=json.dumps(payload))
    roster = json.loads(response.data)
    assert roster[0]['team'] == 'NO'
    assert roster[0]['status'] == 'Active'
