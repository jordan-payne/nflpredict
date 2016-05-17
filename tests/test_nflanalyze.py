from context import nflanalyze
import json

def test_get_team():
    team = nflanalyze.get_team('ARI')
    assert team['team_id'] == 'ARI'
    assert team['city'] == 'Arizona'
    assert team['name'] == 'Cardinals'

def test_get_stats_categories():
    assert len(nflanalyze.get_stats_categories()) == 109

def test_get_all_teams():
    assert len(nflanalyze.get_all_teams()) == 33

def test_fuzzy_search():
    (player, dist) = nflanalyze.fuzzy_search('eli manni')
    assert player.first_name == 'Eli'
    assert player.last_name == 'Manning'

def test_get_player():
    first_name = 'Peyton'
    last_name = 'Manning'
    team = 'UNK'
    player = nflanalyze.get_player(last_name, first_name, team)
    assert player['first_name'] == first_name
    assert player['last_name'] == last_name
    assert player['team'] == team

def test_get_player_all_time_stats():
    first_name = 'Peyton'
    last_name = 'Manning'
    team = 'UNK'
    stats = nflanalyze.get_player_all_time_stats(last_name, first_name, team)
    assert stats.passing_att == 4082
    assert stats.rushing_att == 131
    assert stats.passing_yds == 31097

def test_get_team_roster():
    team = 'NO'
    players = nflanalyze.get_team_roster(team)
    assert players[0].team == 'NO'
    assert str(players[0].status) == 'Active'
