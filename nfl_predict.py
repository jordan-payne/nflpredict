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
week = 17
for i in range(17):
    weeks_data = {}
    # for all 17 weeks, calculate the winning percentage of each team t so far in the season (since week i+1)
    for t in teams:
        q = nfldb.Query(db)
        q.game(season_year=2009, season_type='Regular', winner=t['team_id'], week__le=(i+1))
        wins = len(q.as_games())
        q = nfldb.Query(db)
        q.game(season_year=2009, season_type='Regular', loser=t['team_id'], week__le=(i+1))
        loses = len(q.as_games())
        WP = (wins/float((wins+loses))) * 100
        weeks_data[t['team_id']] = {'winning_per': WP}
    # for all 17 weeks calculate the oponents record so far in the season facing a particular team k
    for k, v in weeks_data.iteritems():
        q = nfldb.Query(db)
        q.game(season_year=2009, season_type='Regular', week=(i+1), home_team=k)
        games = q.as_games()
        if len(games) == 1:
            weeks_data[k]['opponents_record'] = weeks_data[games[0].away_team]['winning_per']
        else:
            q = nfldb.Query(db)
            q.game(season_year=2009, season_type='Regular', week=(i+1), away_team=k)
            games = q.as_games()
            if len(games) == 1:
                weeks_data[k]['opponents_record'] = weeks_data[games[0].home_team]['winning_per']

    # add the weeks data to a list of containing all 17 weeks
    weekly_data[str(i)] = weeks_data

for k, v in weekly_data.iteritems():
    print '\nWEEK %s' % k
    print '-------------------'
    for team, stats in v.iteritems():
        print 'TEAM: %s' % team
        for stat, val in stats.iteritems():
            print '%s: %s%%' %(stat, val)
