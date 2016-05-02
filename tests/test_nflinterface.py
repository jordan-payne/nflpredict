from context import nflinterface

import pytest
import tempfile


@pytest.fixture
def client(request):
    nflinterface.app.config['TESTING'] = True
    client = nflinterface.app.test_client()
    return client

def test_app():
    assert nflinterface.app != None

def test_home(client):
    response = client.get('/')
    assert b'NFL Predict' in response.data
