from context import predict
from context import generate

import pytest

slow = pytest.mark.skipif(
    not pytest.config.getoption('--runslow'),
    reason='need --runslow option to run'
)

def test_open_data():
    data = predict.open_data()
    assert data

def test_compare_teams():
    game = generate.gen_game(2015, 7, 'CAR', 'Regular')
    results = predict.compare_teams(game)
    assert results[0]['distance'] == 0.13239

def test_derive_score():
    game = generate.gen_game(2015, 7, 'CAR', 'Regular')
    results = predict.compare_teams(game)
    score = predict.derive_scores(results[0])
    assert score[0] == 11.15735

def test_predict_winner():
    game = generate.gen_game(2015, 10, 'NE', 'Regular')
    results = predict.compare_teams(game)
    winner = predict.predict_winner(results, game)
    assert winner == 'NE'

@slow
def test_predict_winners():
    correct = predict.predict_winners(2015, 'Regular')
    assert correct == 186

def test_normalize():
    game = generate.gen_game(2015, 10, 'NE', 'Regular')
    game_profile = generate.gen_profile(game)
    data = predict.open_data()
    data, game_profile = predict.normalize(data, game_profile)
    assert data[0]['away_stats'][2] == 0.3012275731822474
