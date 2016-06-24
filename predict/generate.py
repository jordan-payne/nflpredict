#!/usr/bin/env python

import nfldb
import json

db = nfldb.connect()

def gen_game(year, week, team, season_type):
    q = nfldb.Query(db)
    q.game(season_year=year, season_type=season_type, week=week, team=team).limit(1)
    game = q.as_games()
    if len(game) == 1:
        return game[0]
    else:
        return None

def gen_games(year, week, season_type):
    q = nfldb.Query(db)
    q.game(season_year=year, season_type=season_type, week=week)
    games = q.as_games()
    return games

def gen_win_percentage(game, team):
    q = nfldb.Query(db)
    q.game(season_year=game.season_year, season_type=game.season_type, week__le=game.week, team=team)
    games = q.as_games()
    wins = len([g for g in games if g.winner == team])
    loses = len([g for g in games if g.loser == team])
    try:
        wp = (wins/float((wins+loses)))
    except ZeroDivisionError:
        wp = 0.0
    return round(wp, 3)

def gen_all_win_percentages(teams, year, week, season_type):
    wps = {}
    for t in teams:
        game = gen_game(year, week, t, season_type)
        if game:
            wps[t] = gen_win_percentage(game, t)
    return wps

def gen_opponents_win_percentage(game, team):
    q = nfldb.Query(db)
    q.game(season_year=game.season_year, season_type=game.season_type, week__le=game.week, team=team)
    games = q.as_games()
    opponents = [g.away_team if g.home_team == team else g.home_team for g in games]
    wps = []
    for o in opponents:
        wps.append(gen_win_percentage_without_team(game, o, team))
    return round(sum(wps)/len(wps), 3)

def gen_win_percentage_without_team(game, team, other_team):
    q = nfldb.Query(db)
    q.game(season_year=game.season_year, season_type=game.season_type, week__le=game.week, team=team)
    games = q.as_games()
    wins = len([g for g in games if g.winner == team and g.loser != other_team])
    loses = len([g for g in games if g.loser == team and g.winner != other_team])
    try:
        wp = (wins/float((wins+loses)))
    except ZeroDivisionError:
        wp = 0.0
    return round(wp, 3)

def gen_opponents_opponents_win_percentage(game, team):
    q = nfldb.Query(db)
    q.game(season_year=game.season_year, season_type=game.season_type, week__le=game.week, team=team)
    games = q.as_games()
    opponents = [g.away_team if g.home_team == team else g.home_team for g in games]
    owps = []
    for o in opponents:
        owps.append(gen_opponents_win_percentage(game, o))
    return sum(owps)/len(owps)

def gen_rating_percentage_index(game, team):
    wp = gen_win_percentage(game, team)
    owp = gen_opponents_win_percentage(game, team)
    oowp = gen_opponents_opponents_win_percentage(game, team)
    rpi = 0.25 * wp + 0.5 + owp * 0.5 + 0.25 * oowp
    return round(rpi, 3)

def gen_pythagorean_wins(game, team):
    q = nfldb.Query(db)
    q.game(season_year=game.season_year, season_type=game.season_type, week__le=game.week, team=team)
    games = q.as_games()
    points_for = sum([g.home_score if g.home_team == team else g.away_score for g in games])
    points_against = sum([g.away_score if g.home_team == team else g.home_score for g in games])
    exp = 2.37
    try:
        pyth_wins = pow(points_for, exp)/(pow(points_for, exp) + pow(points_against, exp))
    except ZeroDivisionError:
        pyth_wins = 0
    return round(pyth_wins, 3)

def gen_offensive_strategy(game, team):
    q = nfldb.Query(db)
    q.game(season_year=game.season_year, season_type=game.season_type, week__le=game.week, team=team)
    passing_attempts = 0
    rushing_attempts = 0
    stats_query = nfldb.QueryOR(db).play_player(rushing_att__gt=0, passing_att__gt=0)
    team_query = nfldb.Query(db).play_player(team=team)
    q.andalso(stats_query).andalso(team_query)
    for pp in q.as_aggregate():
        passing_attempts = passing_attempts + pp.passing_att
        rushing_attempts = rushing_attempts + pp.rushing_att
    try:
        offensive_strategy = passing_attempts/float(rushing_attempts)
    except ZeroDivisionError:
        offensive_strategy = 0.0
    return round(offensive_strategy, 3)

def gen_turnover_differential(game, team):
    q = nfldb.Query(db)
    q.game(season_year=game.season_year, season_type=game.season_type, week__le=game.week, team=team)
    interceptions = 0
    fumbles_recovered = 0
    stats_query = nfldb.QueryOR(db).play_player(defense_int__gt=0, defense_frec__gt=0)
    team_query = nfldb.Query(db).drive(pos_team__ne=team)
    q.andalso(stats_query).andalso(team_query)
    for pp in q.as_aggregate():
        interceptions = interceptions + pp.defense_int
        fumbles_recovered = fumbles_recovered + pp.defense_frec

    q = nfldb.Query(db)
    q.game(season_year=game.season_year, season_type=game.season_type, week__le=game.week, team=team)
    interceptions_lost = 0
    fumbles_lost = 0
    stats_query = nfldb.QueryOR(db).play_player(fumbles_lost__gt=0, passing_int__gt=0)
    team_query = nfldb.Query(db).drive(pos_team=team)
    q.andalso(stats_query).andalso(team_query)
    for pp in q.as_aggregate():
        interceptions_lost = interceptions_lost + pp.passing_int
        fumbles_lost = fumbles_lost + pp.fumbles_lost
    takeaways = interceptions + fumbles_recovered
    giveaways = interceptions_lost + fumbles_lost

    return takeaways - giveaways

def gen_profiles(year, season_type):
    profiles = []
    if season_type == 'Regular':
        for w in range(1, 18):
            games = gen_games(year, w, season_type)
            for g in games:
                profiles.append(gen_profile(g))
    return profiles

def gen_stats(game, team):
    return [
    gen_win_percentage(game, team),
    gen_pythagorean_wins(game, team),
    gen_offensive_strategy(game, team),
    gen_turnover_differential(game, team)
    ]

def gen_profile(game):
    profile = {}

    home_team = game.home_team
    away_team = game.away_team
    winner = game.winner
    home_score = game.home_score
    away_score = game.away_score
    home_stats = gen_stats(game, game.home_team)
    away_stats = gen_stats(game, game.away_team)

    profile = {
        'week': game.week,
        'year': game.season_year, 'winner': winner,
        'home_score': home_score, 'away_score': away_score,
        'home_team': home_team, 'away_team': away_team,
        'home_stats': home_stats, 'away_stats': away_stats}
    return profile

def get_teams():
    teams = []
    unknown = 'UNK'
    with nfldb.Tx(db) as cursor:
        cursor.execute('''
            SELECT %s FROM team WHERE city != %%s
            ''' % 'team_id', (unknown,))
        for row in cursor.fetchall():
            teams.append(row)
    return [t['team_id'] for t in teams]

def main():
    profiles = []
    f = open('data.json', 'w')
    for y in range(2009,2014):
        profiles.extend(gen_profiles(y, 'Regular'))
    json.dump(profiles, f)
    f.close()

if __name__ == "__main__":
    main()
