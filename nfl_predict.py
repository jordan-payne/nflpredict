#!/usr/bin/env python

import nfldb
import json

db = nfldb.connect()

def main():

    teams = get_teams()
    season = 'Regular'

    #Training data range of years 2009-2013
    training_data_years = range(2009,2014)

    #Test data range of years 2014-2015
    test_data_years = range(2014,2016)

    #Standard regular season of 17 weeks
    weeks = range(1,18)
    training_data = generate_data(training_data_years, teams, weeks, season)
    test_data = generate_data(test_data_years, teams, weeks, season)
    f = open('data.json', 'w')
    data = {'training_data': training_data, 'test_data': test_data}
    f.write(json.dumps(data))

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

def generate_data(years, teams, weeks, season):
    data = []
    for year in years:
        for week in weeks:
            for t in teams:
                profile = {}
                q = nfldb.Query(db)
                q.game(season_year=year, season_type=season, week=week, team=t)
                games = q.as_games()
                this_weeks_game = None if len(games) == 0 else games[0]

                if this_weeks_game:
                    opponent = this_weeks_game.home_team if this_weeks_game.away_team == t else this_weeks_game.away_team
                    home_team = True if this_weeks_game.home_team == t else False
                    winner = this_weeks_game.winner
                    home_score = this_weeks_game.home_score
                    away_score = this_weeks_game.away_score
                else:
                    opponent = 'BYE'
                    home_score = 'BYE'
                    away_score = 'BYE'
                    winner = 'BYE'
                    home_team = 'BYE'

                profile = {
                    'stats': [], 'other_stats': {},
                    'name': t, 'week': week,
                    'year': year, 'opponent': opponent,
                    'home_team': home_team, 'winner': winner,
                    'home_score': home_score, 'away_score': away_score}

                q = nfldb.Query(db)
                this_team_played = nfldb.QueryOR(db).game(home_team=t).game(away_team=t)
                q.game(season_year=year, season_type=season, week__lt=week)
                all_previous_games = q.andalso(this_team_played).as_games()
                wins = len([g for g in all_previous_games if g.winner == t])
                loses = len([g for g in all_previous_games if g.loser == t])
                try:
                    WP = (wins/float((wins+loses)))
                except ZeroDivisionError:
                    WP = 0.0
                profile['other_stats']['wp'] = WP

                opponents = [g.away_team if g.home_team == t else g.home_team for g in all_previous_games]
                profile['opponents'] = opponents
                opponents_records = []
                for o in opponents:
                    q = nfldb.Query(db)
                    opponent_played = nfldb.QueryOR(db).game(home_team=o).game(away_team=o)
                    q.game(season_year=year, season_type=season, week__lt=week, home_team__ne=t, away_team__ne=t)
                    all_opponents_previous_games = q.andalso(opponent_played).as_games()
                    wins = len([g for g in all_opponents_previous_games if g.winner == o])
                    loses = len([g for g in all_opponents_previous_games if g.loser == o])
                    try:
                        record = (wins/float((wins+loses)))
                    except ZeroDivisionError:
                        record = 0.0
                    opponents_records.append(record)
                try:
                    OWP = sum(opponents_records)/float(len(opponents))
                except ZeroDivisionError:
                    OWP = 0.0
                profile['other_stats']['owp'] = OWP

                oowps = [o['other_stats']['owp'] for o in data if o['year'] == year and o['week'] < week and o['opponent'] == t]
                try:
                    OOWP = sum(oowps)/float(len(oowps))
                except ZeroDivisionError:
                    OOWP = 0.0
                profile['other_stats']['oowp'] = OOWP
                profile['stats'].append(0.25 * WP + 0.5 + OWP * 0.5 + 0.25 * OOWP)

                points_for = sum([g.home_score if g.home_team == t else g.away_score for g in all_previous_games])
                points_against = sum([g.away_score if g.home_team == t else g.home_score for g in all_previous_games])
                try:
                    pyth_wins = pow(points_for, 2.37)/(pow(points_for, 2.37) + pow(points_against, 2.37))
                except ZeroDivisionError:
                    pyth_wins = 0
                profile['stats'].append(pyth_wins)


                q = nfldb.Query(db)
                q.game(season_year=year, season_type=season, week__lt=week, team=t)
                passing_attempts = 0
                rushing_attempts = 0
                for pp in q.drive(pos_team=t).as_aggregate():
                    passing_attempts = passing_attempts + pp.passing_att
                    rushing_attempts = rushing_attempts + pp.rushing_att
                try:
                    offensive_strategy = passing_attempts/float(rushing_attempts)
                except ZeroDivisionError:
                    offensive_strategy = 0.0
                profile['stats'].append(offensive_strategy)


                q = nfldb.Query(db)
                q.game(season_year=year, season_type=season, week__lt=week, team=t)
                interceptions = 0
                fumbles_recovered = 0
                for pp in q.drive(pos_team__ne=t).as_aggregate():
                    interceptions = interceptions + pp.defense_int
                    fumbles_recovered = fumbles_recovered + pp.defense_frec

                q = nfldb.Query(db)
                q.game(season_year=year, season_type=season, week__lt=week, team=t)
                interceptions_lost = 0
                fumbles_lost = 0
                for pp in q.drive(pos_team=t).as_aggregate():
                    interceptions_lost = interceptions_lost + pp.passing_int
                    fumbles_lost = fumbles_lost + pp.fumbles_lost

                takeaways = interceptions + fumbles_recovered
                giveaways = interceptions_lost + fumbles_lost

                try:
                    turnover_differential = takeaways/float(giveaways)
                except ZeroDivisionError:
                    turnover_differential = 0.0
                profile['stats'].append(turnover_differential)

                data.append(profile)
    return data

if __name__ == "__main__":
    main()
