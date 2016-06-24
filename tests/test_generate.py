from context import generate

def test_get_teams():
    teams = generate.get_teams()
    assert len(teams) == 32

def test_gen_game():
    game = generate.gen_game(2015, 7, 'CAR', 'Regular')
    assert game.away_team == 'PHI'
    assert game.home_team == 'CAR'
    assert game.away_score == 16
    assert game.home_score == 27

def test_gen_win_percentage():
    game = generate.gen_game(2015, 7, 'CAR', 'Regular')
    profile = generate.gen_profile(game)
    wp = generate.gen_win_percentage(game, profile['away_team'])
    assert wp == 0.429

def test_gen_profile():
    game = generate.gen_game(2015, 7, 'CAR', 'Regular')
    profile = generate.gen_profile(game)
    assert profile['home_score'] == 27
    assert len(profile['home_stats']) == 4
    assert profile['away_stats'][0] == 0.429
    game = generate.gen_game(2015, 17, 'CLE', 'Regular')
    profile = generate.gen_profile(game)
    assert profile['home_stats'][0] == 0.188

def test_gen_all_win_percentages():
    teams = generate.get_teams()
    wps = generate.gen_all_win_percentages(teams, 2015, 17, 'Regular')
    assert wps['CLE'] == 0.188
    wps = generate.gen_all_win_percentages(teams, 2015, 1, 'Regular')
    assert wps['NE'] == 1.0

def test_gen_opponents_win_percentage():
    game = generate.gen_game(2015, 7, 'CAR', 'Regular')
    owp = generate.gen_opponents_win_percentage(game, 'CAR')
    assert owp == 0.428

def test_gen_opponents_opponents_win_percentage():
    game = generate.gen_game(2015, 7, 'CAR', 'Regular')
    oowp = generate.gen_opponents_opponents_win_percentage(game, 'CAR')
    assert oowp == 0.541

def test_gen_rating_percentage_index():
    game = generate.gen_game(2015, 7, 'CAR', 'Regular')
    rpi = generate.gen_rating_percentage_index(game, 'CAR')
    assert rpi == 1.099
    game = generate.gen_game(2015, 7, 'CLE', 'Regular')
    rpi = generate.gen_rating_percentage_index(game, 'CLE')
    assert rpi == 0.909
    game = generate.gen_game(2015, 7, 'NE', 'Regular')
    rpi = generate.gen_rating_percentage_index(game, 'NE')
    assert rpi == 1.15

def test_gen_pythagorean_wins():
    game = generate.gen_game(2015, 7, 'CAR', 'Regular')
    pyth_wins = generate.gen_pythagorean_wins(game, 'CAR')
    assert pyth_wins == 0.715
    game = generate.gen_game(2015, 8, 'NE', 'Regular')
    pyth_wins = generate.gen_pythagorean_wins(game, 'NE')
    assert pyth_wins == 0.816

def test_gen_offensive_strategy():
    game = generate.gen_game(2015, 7, 'CAR', 'Regular')
    offensive_strategy = generate.gen_offensive_strategy(game, 'CAR')
    assert offensive_strategy == 0.919
    game = generate.gen_game(2015, 7, 'NO', 'Regular')
    offensive_strategy = generate.gen_offensive_strategy(game, 'NO')
    assert offensive_strategy == 1.578

def test_gen_turnover_differential():
    game = generate.gen_game(2015, 17, 'CAR', 'Regular')
    turnover_differential = generate.gen_turnover_differential(game, 'CAR')
    assert turnover_differential == 18
    game = generate.gen_game(2015, 17, 'KC', 'Regular')
    turnover_differential = generate.gen_turnover_differential(game, 'KC')
    assert turnover_differential == 16

def test_gen_profiles():
    profiles = generate.gen_profiles(2015, 'Regular')
    assert len(profiles) == 256

def test_gen_stats():
    game = generate.gen_game(2015, 7, 'CAR', 'Regular')
    stats = generate.gen_stats(game, game.home_team)
    assert stats[0] == 1.0

def test_gen_games():
    games = generate.gen_games(2015, 7, 'Regular')
    assert len(games) == 14
