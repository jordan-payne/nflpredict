import json
import os

location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

fileIn = 'output.json'

with open(os.path.join(location,fileIn)) as file:
	data = json.load(file)
	
correctCount = 0
biweekCount = 0

for game in data:
	if not game.has_key('predict'):
		biweekCount += 1
		continue
	elif game['predict'] == 'win' and game['winner'] == game['name']:
		correctCount += 1
	elif game['predict'] == 'lose' and game['winner'] == game['opponent']:
		correctCount += 1

totalGame = len(data) - biweekCount
print 'Accuracy: %s' %(correctCount/float(totalGame)) 		