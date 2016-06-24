#!/usr/bin/env python

import json
import generate

def open_data():
    f = open('data.json', 'r')
    data = json.load(f)
    f.close()
    return data

def compare_teams(game):
    game_profile = generate.gen_profile(game)
    data = open_data()
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

    print profile[profile['distance_config'][0]], profile[profile['distance_config'][1]], profile['distance']

    return [
    round(profile[profile['distance_config'][0]]/profile['distance'], 5),
    round(profile[profile['distance_config'][1]]/profile['distance'], 5)]
