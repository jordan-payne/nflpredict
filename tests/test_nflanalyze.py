from context import nflanalyze

def test_get_team():
    team = nflanalyze.get_team('ARI')
    assert team['team_id'] == 'ARI'
    assert team['city'] == 'Arizona'
    assert team['name'] == 'Cardinals'

def test_get_stats_categories():
    assert len(nflanalyze.get_stats_categories()) == 109

def test_get_all_teams():
    assert len(nflanalyze.get_all_teams()) == 33

def test_get_player():
    first_name = 'Drew'
    last_name = 'Brees'
    team = 'NO'
    player = nflanalyze.get_player(last_name, first_name, team)
    assert player['first_name'] == first_name
    assert player['last_name'] == last_name
    assert player['team'] == team

def test_get_player_all_time_stats():
    first_name = 'Peyton'
    last_name = 'Manning'
    team = 'DEN'
    stats = nflanalyze.get_player_all_time_stats(last_name, first_name, team)
    assert stats.passing_att == 4059
    assert stats.rushing_att == 131
    assert stats.passing_yds == 30956
