#!/usr/bin/env python

import nfldb
import json
import math
import json
import sys

db = nfldb.connect()

def main():

    year = raw_input('Enter a year to predict (2009-2014) or hit "enter" to predict all available years: ')

    try:
        year = int(year)
        if year < 2009 or year > 2014:
            print 'Not a selectable year, exiting...'
            sys.exit()
    except ValueError:
        year = "all"

    teams = get_teams()
    season = 'Regular'

    if year == "all":
        years = range(2009,2015)
    else:
        years = range(year, year+1)
    correct = 0
    for y in years:
        training_data = generate_data(y, teams, season)
        correct += predict(training_data, y, 3)
    print 'Accuracy: %s' %(correct/(len(years)*11.0))

def predict(training_data, year, k):
    q = nfldb.Query(db)
    q.game(season_year=year, season_type='Postseason')
    games = q.as_games()
    correct = 0
    summation = 0
    for g in games:
        summation += 1
        ht_stats = training_data[g.home_team]
        aw_stats = training_data[g.away_team]
        similar_to_home = {'unk': 9999}
        similar_to_away = {'unk': 9999}
        for k,v in training_data.iteritems():
            if k != g.home_team and k != g.away_team:
                distance_to_home_team = math.sqrt(pow(v[0]-ht_stats[0],2) + pow(v[1]-ht_stats[1],2) + pow(v[2]-ht_stats[2],2) + pow(v[3]-ht_stats[3],2))
                if distance_to_home_team < max(similar_to_home.values()) or len(similar_to_home) < k:
                    if len(similar_to_home) == k:
                        largest = max(similar_to_home, key=similar_to_home.get)
                        del similar_to_home[largest]
                    similar_to_home[k]= distance_to_home_team
                distance_to_away_team = math.sqrt(pow(v[0]-aw_stats[0],2) + pow(v[1]-aw_stats[1],2) + pow(v[2]-aw_stats[2],2) + pow(v[3]-aw_stats[3],2))
                if distance_to_away_team < max(similar_to_away.values()) or len(similar_to_away) < k:
                    if len(similar_to_away) == k:
                        largest = max(similar_to_away, key=similar_to_away.get)
                        del similar_to_away[largest]
                    similar_to_away[k] = distance_to_away_team
        games_between_similar = []
        for k_home in similar_to_home:
            for k_away in similar_to_away:
                if k_home != k_away:
                    this_team_played = nfldb.QueryOR(db)
                    this_team_played.game(home_team=k_away)
                    this_team_played.game(away_team=k_away)
                    that_team_played = nfldb.QueryOR(db)
                    that_team_played.game(home_team=k_home)
                    that_team_played.game(away_team=k_home)
                    q = nfldb.Query(db).game(season_year=year, season_type='Regular')
                    q.andalso(this_team_played)
                    q.andalso(that_team_played)
                    games_between = q.as_games()
                    for game_played in games_between:
                        games_between_similar.append(game_played)
        home_score = 0
        away_score = 0
        for game in games_between_similar:
            if game.home_team in similar_to_home and game.away_team in similar_to_away:
                home_score += game.home_score/(similar_to_home[game.home_team] + 1 + similar_to_away[game.away_team])
                away_score += game.away_score/(similar_to_home[game.home_team] + 1 + similar_to_away[game.away_team])
            if game.home_team in similar_to_away and game.away_team in similar_to_home:
                home_score += game.away_score/(similar_to_home[game.away_team] + 1 + similar_to_away[game.home_team])
                away_score += game.home_score/(similar_to_home[game.away_team] + 1 + similar_to_away[game.home_team])
        print '---------------'
        print '%s: %s' %(g.home_team, home_score)
        print '%s: %s' %(g.away_team, away_score)
        if home_score > away_score:
            winner = g.home_team
        elif home_score < away_score:
            winner = g.away_team
        if winner == g.winner:
            correct += 1
            print 'CORRECT'
        else:
            print 'INCORRECT'
        print '---------------'

    return correct


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

def generate_data(year, teams, season):
    data = []
    WP = {}
    for t in teams:
        q = nfldb.Query(db)
        q.game(season_year=year, season_type=season, winner=t)
        games = q.as_games()
        wins = 0
        for g in games:
            wins += 1
        q = nfldb.Query(db)
        q.game(season_year=year, season_type=season,loser=t)
        games = q.as_games()
        loses = 0
        for g in games:
            loses += 1
        WP[t] = float(wins)/(loses + wins)

    OWP = {}
    for t in teams:
        this_team_played = nfldb.QueryOR(db)
        this_team_played.game(home_team=t)
        this_team_played.game(away_team=t)
        q = nfldb.Query(db).game(season_year=year, season_type=season)
        q.andalso(this_team_played)
        opponents = []
        games = q.as_games()
        for g in games:
            if g.home_team != t:
                opponents.append(g.home_team)
            else:
                opponents.append(g.away_team)
        summation = 0
        for o in opponents:
            summation += WP[o]
        OWP[t] = summation/len(opponents)

    OOWP = {}
    for t in teams:
        this_team_played = nfldb.QueryOR(db)
        this_team_played.game(home_team=t)
        this_team_played.game(away_team=t)
        q = nfldb.Query(db).game(season_year=year, season_type=season)
        q.andalso(this_team_played)
        opponents = []
        games = q.as_games()
        for g in games:
            if g.home_team != t:
                opponents.append(g.home_team)
            else:
                opponents.append(g.away_team)
        summation = 0
        for o in opponents:
            summation += OWP[o]
        OOWP[t] = summation/len(opponents)

    RPI = {}
    for t in teams:
        RPI[t] = 0.25*WP[t]*100 + OWP[t]*0.5*100 + OOWP[t]*0.25*100

    PYTH_WINS = {}
    for t in teams:
        this_team_played = nfldb.QueryOR(db)
        this_team_played.game(home_team=t)
        this_team_played.game(away_team=t)
        q = nfldb.Query(db).game(season_year=year, season_type=season)
        q.andalso(this_team_played)
        points_for = 0
        points_against = 0
        games = q.as_games()
        for g in games:
            if g.home_team != t:
                points_for += g.away_score
                points_against += g.home_score
            else:
                points_for += g.home_score
                points_against += g.away_score
        PYTH_WINS[t] = pow(points_for, 2.37)/(pow(points_for, 2.37) + pow(points_against, 2.37))

    OFFENSIVE_STRATEGY = {}
    for t in teams:
        this_team_played = nfldb.QueryOR(db)
        this_team_played.game(home_team=t)
        this_team_played.game(away_team=t)
        q = nfldb.Query(db).game(season_year=year, season_type=season)
        q.andalso(this_team_played)
        passing_attempts = 0
        rushing_attempts = 0
        for pp in q.drive(pos_team=t).as_aggregate():
            passing_attempts = passing_attempts + pp.passing_att
            rushing_attempts = rushing_attempts + pp.rushing_att
        try:
            offensive_strategy = passing_attempts/float(rushing_attempts)
        except ZeroDivisionError:
            offensive_strategy = 0.0
        OFFENSIVE_STRATEGY[t] = offensive_strategy


    TURNOVER_DIFFERENTIAL = {}
    for t in teams:
        this_team_played = nfldb.QueryOR(db)
        this_team_played.game(home_team=t)
        this_team_played.game(away_team=t)
        q = nfldb.Query(db).game(season_year=year, season_type=season)
        q.andalso(this_team_played)
        interceptions = 0
        fumbles_recovered = 0
        for pp in q.drive(pos_team__ne=t).as_aggregate():
            interceptions = interceptions + pp.defense_int
            fumbles_recovered = fumbles_recovered + pp.defense_frec

        this_team_played = nfldb.QueryOR(db)
        this_team_played.game(home_team=t)
        this_team_played.game(away_team=t)
        q = nfldb.Query(db).game(season_year=year, season_type=season)
        q.andalso(this_team_played)
        interceptions_lost = 0
        fumbles_lost = 0
        for pp in q.drive(pos_team=t).as_aggregate():
            interceptions_lost = interceptions_lost + pp.passing_int
            fumbles_lost = fumbles_lost + pp.fumbles_lost

        takeaways = interceptions + fumbles_recovered
        giveaways = interceptions_lost + fumbles_lost

        try:
            turnover_differential = takeaways - giveaways
        except ZeroDivisionError:
            turnover_differential = 0.0
        TURNOVER_DIFFERENTIAL[t] = turnover_differential

    RPI = normalize(RPI, 150, 0)
    PYTH_WINS = normalize(PYTH_WINS, 0, 100)
    OFFENSIVE_STRATEGY = normalize(OFFENSIVE_STRATEGY, 0, 50)
    TURNOVER_DIFFERENTIAL = normalize(TURNOVER_DIFFERENTIAL, 0, 50)
    stats = {}
    for t in teams:
        stats[t] = [RPI[t], PYTH_WINS[t], OFFENSIVE_STRATEGY[t], TURNOVER_DIFFERENTIAL[t]]
    return stats

def normalize(values, new_max, new_min):
    max_value = values[max(values, key=values.get)]
    min_value = values[min(values, key=values.get)]
    old_range = max_value - min_value
    new_range = new_max - new_min
    for k,v in values.iteritems():
        values[k] = (((v - min_value) * new_range) / old_range) + new_min
    return values

if __name__ == "__main__":
    main()
