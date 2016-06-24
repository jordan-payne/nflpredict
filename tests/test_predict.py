from context import predict
from context import generate

def test_open_data():
    data = predict.open_data()
    assert data

def test_compare_teams():
    game = generate.gen_game(2015, 7, 'CAR', 'Regular')
    results = predict.compare_teams(game)
    assert results[0]['distance'] == 0.7259199999999999

def test_derive_score():
    game = generate.gen_game(2015, 7, 'CAR', 'Regular')
    results = predict.compare_teams(game)
    score = predict.derive_scores(results[0])
    assert score[0] == 9.64294
