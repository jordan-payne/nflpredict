import nfldb

db = nfldb.connect()

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
    for t in teams:
        q = nfldb.Query(db)
        q.game(season_year=2009, season_type='Regular', winner=t['team_id'], week__le=(i+1))
        wins = len(q.as_games())
        q2 = nfldb.Query(db)
        q2.game(season_year=2009, season_type='Regular', loser=t['team_id'], week__le=(i+1))
        loses = len(q2.as_games())
        WP = (wins/float((wins+loses))) * 100
        # print 'Winning Percentage for %s: %s%% (Wins:%s, Loses:%s)' % (t['team_id'],WP, wins, loses)
        weeks_data[t['team_id']] = {'winning_per': WP}
    for k, v in weeks_data.iteritems():
        query = nfldb.Query(db)
        query.game(season_year=2009, season_type='Regular', week=(i+1), home_team=k)
        games = query.as_games()
        if len(games) == 1:
            weeks_data[k]['opponents_record'] = weeks_data[games[0].away_team]['winning_per']
        else:
            query = nfldb.Query(db)
            query.game(season_year=2009, season_type='Regular', week=(i+1), away_team=k)
            games = query.as_games()
            if len(games) == 1:
                weeks_data[k]['opponents_record'] = weeks_data[games[0].home_team]['winning_per']
    weekly_data[str(i)] = weeks_data

for k, v in weekly_data.iteritems():
    print '\nWEEK %s' % k
    print '-------------------'
    for team, stats in v.iteritems():
        print 'TEAM: %s' % team
        for stat, val in stats.iteritems():
            print '%s: %s%%' %(stat, val)
