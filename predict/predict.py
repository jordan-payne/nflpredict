#!/usr/bin/env python

import json
import generate
import math
import nfldb

db = nfldb.connect()

def normalize(data, game_profile):
    for s in range(1, len(data[0]['home_stats'])):
        stat = [d['home_stats'][s] for d in data]
        stat.extend([d['away_stats'][s] for d in data])
        stat.append(game_profile['home_stats'][s])
        stat.append(game_profile['away_stats'][s])
        stat_max = max(stat)
        stat_min = min(stat)
        for d in data:
            d['home_stats'][s] = (d['home_stats'][s] - stat_min)/(stat_max - float(stat_min))
            d['away_stats'][s] = (d['away_stats'][s] - stat_min)/(stat_max - float(stat_min))
        game_profile['home_stats'][s] = (game_profile['home_stats'][s] - stat_min) / (stat_max - float(stat_min))
        game_profile['away_stats'][s] = (game_profile['away_stats'][s] - stat_min) / (stat_max - float(stat_min))
    return data, game_profile

def open_data():
    f = open('data.json', 'r')
    data = json.load(f)
    f.close()
    return data

def compare_teams(game):
    game_profile = generate.gen_profile(game)
    data = open_data()
    data, game_profile = normalize(data, game_profile)
    limit = 6
    closest = []
    for g in data:
        config1 = sum(
        [calculate_distance(game_profile['home_stats'], g['home_stats']),
        calculate_distance(game_profile['away_stats'], g['away_stats'])]
        )
        config2 = sum(
        [calculate_distance(game_profile['home_stats'], g['away_stats']),
        calculate_distance(game_profile['away_stats'], g['home_stats'])]
        )
        g['distance'] = min(config1, config2)
        if g['distance'] == config1:
            g['distance_config'] = ['home_score', 'away_score']
        else:
            g['distance_config'] = ['away_score', 'home_score']
        closest.append(g)
        closest.sort(cmp=lambda x,y: cmp(x['distance'], y['distance']))
        closest = closest[0:limit]

    return closest

def calculate_distance(game_stats1, game_stats2):
    distance = map(lambda x, y:pow(x-y, 2), game_stats1, game_stats2)
    distance = sum(distance)
    distance = pow(distance, 0.5)
    return round(distance, 5)

def derive_scores(profile):
    try:
        scores = [
        round(math.log10(profile[profile['distance_config'][0]])/profile['distance'], 5),
        round(math.log10(profile[profile['distance_config'][1]])/profile['distance'], 5)]
    except ValueError:
        scores = [0,0]
        if profile[profile['distance_config'][0]] == 0:
            scores[0] = 0
            scores[1] = round(math.log10(profile[profile['distance_config'][1]])/profile['distance'], 5)
        else:
            scores[1] = 0
            scores[0] = round(math.log10(profile[profile['distance_config'][0]])/profile['distance'], 5)
    return scores

def predict_winner(profiles, game):
    scores = [0,0]
    for p in profiles:
        score = derive_scores(p)
        scores[0] += score[0]
        scores[1] += score[1]

    # scores[0] *= home_field_multiplier[game.home_team]
    # scores[1] *= 1 - home_field_multiplier[game.home_team]
    #
    # scores[0] *= 1 - away_field_multiplier[game.away_team]
    # scores[1] *= away_field_multiplier[game.away_team]

    winner = game.home_team if scores[0] > scores[1] else game.away_team
    return winner

def predict_winners(year, season_type):
    q = nfldb.Query(db)
    q.game(season_year=year, season_type=season_type)
    games = q.as_games()
    counter = 0
    print len(games)
    for g in games:
        results = compare_teams(g)
        winner = predict_winner(results, g)
        result = 'Correct' if winner == g.winner else 'Incorrect'
        if winner == g.winner:
            counter += 1
    return counter

home_field_multiplier = {
    'CAR': 0.5250,
    'IND': 0.7375,
    'GB': 0.6875,
    'TEN': 0.5875,
    'NE': 0.8375,
    'NYG': 0.5250,
    'JAC': 0.5750,
    'TB': 0.5250,
    'ATL': 0.6250,
    'NO': 0.5625,
    'SEA': 0.6375,
    'BAL': 0.7625,
    'DET': 0.4000,
    'DEN': 0.6000,
    'ARI': 0.5500,
    'MIN': 0.6000,
    'BUF': 0.4875,
    'MIA': 0.4750,
    'CLE': 0.3875,
    'CHI': 0.6125,
    'STL': 0.4375,
    'OAK': 0.3875,
    'SD': 0.6875,
    'PIT': 0.7342,
    'WAS': 0.4500,
    'PHI': 0.6250,
    'NYJ': 0.5750,
    'CIN': 0.5190,
    'HOU': 0.4875,
    'KC': 0.5625,
    'SF': 0.5500,
    'DAL': 0.6000
}

away_field_multiplier = {
    'PHI': 0.6203,
    'IND': 0.6500,
    'CAR': 0.4625,
    'GB': 0.5500,
    'TEN': 0.4875,
    'NE': 0.7000,
    'NYG': 0.5750,
    'JAC': 0.3750,
    'BUF': 0.3250,
    'DAL': 0.4750,
    'TB': 0.4000,
    'OAK': 0.3125,
    'DET': 0.1875,
    'KC': 0.3625,
    'STL': 0.2625,
    'DEN': 0.4750,
    'BAL': 0.4125,
    'MIN': 0.3625,
    'CIN': 0.3750,
    'HOU': 0.3250,
    'SF': 0.3125,
    'SEA': 0.3750,
    'ATL': 0.4684,
    'NYJ': 0.4250,
    'ARI': 0.2625,
    'PIT': 0.5875,
    'SD': 0.5125,
    'WAS': 0.3625,
    'NO': 0.5625,
    'CLE': 0.3125,
    'CHI': 0.4125,
    'MIA': 0.4000
}
