#!/usr/bin/env python

import nfldb

db = nfldb.connect()

# Get a list of the teams in the NFL and place it in teams list
teams = []
unknown = 'UNK'
with nfldb.Tx(db) as cursor:
    cursor.execute('''
        SELECT %s FROM team WHERE city != %%s
        ''' % '*', (unknown,))
    for row in cursor.fetchall():
        teams.append(row)

weekly_data = {}
for week in range(1,18):
    weeks_data = {}
    # for all 17 weeks, calculate the winning percentage of each team t so far in the season (since week i+1)
    for t in teams:
        team = t['team_id']
        q = nfldb.Query(db)
        this_team_played = nfldb.QueryOR(db).game(home_team=team).game(away_team=team)
        q.game(season_year=2009, season_type='Regular', week__lt=week)
        all_previous_games = q.andalso(this_team_played).as_games()
        wins = len([g for g in all_previous_games if g.winner == team])
        loses = len([g for g in all_previous_games if g.loser == team])
        try:
            WP = (wins/float((wins+loses)))
        except ZeroDivisionError:
            WP = 0.0
        weeks_data[team] = {'wp': WP}


        opponents = [g.away_team if g.home_team == team else g.home_team for g in all_previous_games]
        opponents_records = []
        for o in opponents:
            q = nfldb.Query(db)
            opponent_played = nfldb.QueryOR(db).game(home_team=o).game(away_team=o)
            q.game(season_year=2009, season_type='Regular', week__lt=week, home_team__ne=team, away_team__ne=team)
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
        weeks_data[team]['owp'] = OWP

        opponents_by_week = dict([(g.week, g.away_team) if g.home_team == team else (g.week, g.home_team) for g in all_previous_games])
        owps = []
        for k,v in opponents_by_week.iteritems():
            owps.append(weekly_data[str(k)][v]['owp'])
        try:
            OOWP = sum(owps)/float(len(opponents_by_week))
        except ZeroDivisionError:
            OOWP = 0.0
        weeks_data[team]['oowp'] = OOWP
        weeks_data[team]['rpi'] = 0.25 * WP + 0.5 + OWP * 0.5 + 0.25 * OOWP

        points_for = sum([g.home_score if g.home_team == team else g.away_score for g in all_previous_games])
        points_against = sum([g.away_score if g.home_team == team else g.home_score for g in all_previous_games])
        try:
            pyth_wins = pow(points_for, 2.37)/(pow(points_for, 2.37) + pow(points_against, 2.37))
        except ZeroDivisionError:
            pyth_wins = 0
        weeks_data[team]['pyth_wins'] = pyth_wins

        q = nfldb.Query(db)
        q.game(season_year=2015, season_type='Regular', week__lt=week, team=team)
        passing_attempts = 0
        rushing_attempts = 0
        for pp in q.drive(pos_team=team).as_aggregate():
            passing_attempts = passing_attempts + pp.passing_att
            rushing_attempts = rushing_attempts + pp.rushing_att
        try:
            offensive_strategy = passing_attempts/float(rushing_attempts)
        except ZeroDivisionError:
            offensive_strategy = 0.0
        weeks_data[team]['offensive_strategy'] = offensive_strategy

        q = nfldb.Query(db)
        q.game(season_year=2009, season_type='Regular', week__lt=week, team=team)
        interceptions = 0
        fumbles_recovered = 0
        for pp in q.drive(pos_team__ne=team).as_aggregate():
            interceptions = interceptions + pp.defense_int
            fumbles_recovered = fumbles_recovered + pp.defense_frec

        q = nfldb.Query(db)
        q.game(season_year=2009, season_type='Regular', week__lt=week, team=team)
        interceptions_lost = 0
        fumbles_lost = 0
        for pp in q.drive(pos_team=team).as_aggregate():
            interceptions_lost = interceptions_lost + pp.passing_int
            fumbles_lost = fumbles_lost + pp.fumbles_lost

        takeaways = interceptions + fumbles_recovered
        giveaways = interceptions_lost + fumbles_lost

        try:
            turnover_differential = takeaways/float(giveaways)
        except ZeroDivisionError:
            turnover_differential = 0.0
        weeks_data[team]['turnover_differential'] = turnover_differential

    weekly_data[str(week)] = weeks_data


for k, v in weekly_data.iteritems():
    print '\nWEEK %s' % k
    print '-------------------'
    for team, stats in v.iteritems():
        print 'TEAM: %s' % team
        for stat, val in stats.iteritems():
            print '%s: %s' %(stat, val)
