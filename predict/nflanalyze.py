# ANALYSIS MODULE FOR NFL PREDICT

import nfldb, nfldbc
import json

dbc = nfldbc.dbc

def get_team(team_name):
    with nfldb.Tx(dbc) as cursor:
        cursor.execute('SELECT * FROM team WHERE team_id = %s', [team_name,])
        return cursor.fetchone()

def get_all_teams():
    with nfldb.Tx(dbc) as cursor:
        cursor.execute('SELECT * FROM team;')
        return cursor.fetchall()

def get_stats_categories():
    return nfldb.stat_categories

def get_player(last_name, first_name, team):
    with nfldb.Tx(dbc) as cursor:
        cursor.execute(
            '''SELECT * FROM player WHERE last_name = %s AND first_name = %s AND team = %s''',
            [last_name,first_name, team])
        return cursor.fetchone()

def get_player_all_time_stats(last_name, first_name, team):
    player = get_player(last_name, first_name, team)
    q = nfldb.Query(dbc)
    q.play_player(player_id=player['player_id'])
    return q.limit(1).as_aggregate()[0]

def to_json(obj):
    dictionary = {}
    try:
        for f in obj.fields:
            dictionary[f] = getattr(obj, f)
    except AttributeError:
        dictionary = dict(obj)
        for i in obj:
            if i != 'status':
                dictionary[i] = obj[i]
            if i == 'status':
                dictionary[i] = str(obj[i])
            if i == 'position':
                dictionary[i] = str(obj[i])
    return json.dumps(dictionary)
