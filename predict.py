import json
import os
import math
from pprint import pprint

location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

fileIn = 'data\\2014\\week11-2014.json'
fileOut = 'out\\2014-2\\out-week11-2014.json'

with open(os.path.join(location, fileIn)) as file:
	data = json.load(file)

testData = data['test_data']

trainData = data['training_data']
normallizeScale = { 0 : {'min' : 0, 'max' : 150}, 1 : {'min' : 0, 'max' : 100}, 2 :{'min' : 0, 'max' : 50}, 3 : {'min' : 0, 'max' : 50}}

maxRPITrain = max([y[0] for y in [z['stats'] for z in trainData]])
minRPITrain = min([y[0] for y in [z['stats'] for z in trainData]])

maxRPITest = max([y[0] for y in [z['stats'] for z in testData]])
minRPITest = min([y[0] for y in [z['stats'] for z in testData]])

maxRPI = max(maxRPITest, maxRPITrain)
minRPI = min(minRPITrain, minRPITest)
#---------------------------------------
maxPWTrain = max([y[1] for y in [z['stats'] for z in trainData]])
minPWTrain = min([y[1] for y in [z['stats'] for z in trainData]])

maxPWTest = max([y[1] for y in [z['stats'] for z in testData]])
minPWTest = min([y[1] for y in [z['stats'] for z in testData]])

maxPW = max(maxPWTest, maxPWTrain)
minPW = min(minPWTrain, minPWTest)
#----------------------------------------
maxOSTrain = max([y[2] for y in [z['stats'] for z in trainData]])
minOSTrain = min([y[2] for y in [z['stats'] for z in trainData]])

maxOSTest = max([y[2] for y in [z['stats'] for z in testData]])
minOSTest = min([y[2] for y in [z['stats'] for z in testData]])

maxOS = max(maxOSTest, maxOSTrain)
minOS = min(minOSTrain, minOSTest)
#-----------------------------------------
maxTDTrain = max([y[3] for y in [z['stats'] for z in trainData]])
minTDTrain = min([y[3] for y in [z['stats'] for z in trainData]])

maxTDTest = max([y[3] for y in [z['stats'] for z in testData]])
minTDTest = min([y[3] for y in [z['stats'] for z in testData]])

maxTD = max(maxTDTest, maxTDTrain)
minTD = min(minTDTrain, minTDTest)

oldScale = { 0 : {'min' : minRPI, 'max': maxRPI}, 1 :{'min' : minPW, 'max': maxPW}, 2:{'min' : minOS, 'max': maxOS}, 3:{'min' : minTD, 'max': maxTD}}

maxDistance = 2
		
def main():
	
	for testteam in testData:
		testteam['stats'] = normallize(testteam['stats'])

	for trainteam in trainData:
		trainteam['stats'] = normallize(trainteam['stats'])
		
	
	for teamRecord in testData:
		if teamRecord['home_score'] == 'BYE':
			continue
			
		if teamRecord.has_key('predict'):
			continue
		
		teamName = teamRecord['name']
		teamOppo = getOpponent(teamRecord['opponent'], teamRecord['week'], teamRecord['year'])
		
		#biweek - no games 
		if not teamOppo:
			continue
		
		similarTeam = getSimilartTeams(teamRecord)
		#pprint(similarTeam)

		similarOpp = getSimilartTeams(teamOppo)
		#pprint(similarOpp)
		
		resultPoints = [0.0, 0.0]
		
		calculatePoints(similarTeam, similarOpp, resultPoints)
		
		#what if they are equal?
		
		#print resultPoints
		
		if resultPoints[0] > resultPoints[1] :
			teamRecord['predict'] = 'win'
			teamOppo['predict'] = 'lose'
		elif resultPoints[0] < resultPoints[1] :
			teamRecord['predict'] = 'lose'
			teamOppo['predict'] = 'win'
		else :
			if sum(teamRecord['stats']) > sum(teamOppo['stats']) :
				teamRecord['predict'] = 'win'
				teamOppo['predict'] = 'lose'
			else:
				teamRecord['predict'] = 'lose'
				teamOppo['predict'] = 'win'
		
		#pprint(teamRecord)
		#pprint(teamOppo)
	#pprint(testData)
	f = open(os.path.join(location, fileOut), 'w')
	f.write(json.dumps(testData))
	f.close()
	
		
def normallize(points):
	for index in range(len(points)):
		value = points[index]
		newScale = normallizeScale[index]
		scale = oldScale[index]
		points[index] = (((value - scale['min'])*(newScale['max'] - newScale['min'])) / ( scale['max'] - scale['min'])) + newScale['min']
		
	return points
		
def distance(team1Points, team2Points):
	distance = 0
	for index in range(len(team1Points)):
		distance = math.pow(team1Points[index] -  team2Points[index], 2)
	
	distance = math.sqrt(distance)
	#print distance
	return distance
	
def getOpponent(name, week, year):
	for team in testData :
		if team['name'] == name and team['week'] == week and team['year'] == year:
			return team
			
	return False
			
def getSimilartTeams(curTeam):
	similarTeams = {}
	points = curTeam['stats']
	
	for team in trainData :
		teamStat = team['stats']
		distanceValue = distance(points, teamStat)
		#print distanceValue
		if distanceValue < maxDistance :
			similarTeam = { 'distance' : distanceValue , 'team': team }
			similarTeams[team['name']+str(team['week'])+str(team['year'])] = similarTeam
	
	return similarTeams
	
def calculatePoints(team1List, team2List, result) :
	for trainteam in trainData :
		
		week = trainteam['week']
		year = trainteam['year']
		name = trainteam['name']
		opponent = trainteam['opponent'] 
		winner = trainteam['winner'] 
		stats = trainteam['stats'] 
		for key, similarTeam in team1List.iteritems():
			team = similarTeam['team']
			teamDistance = similarTeam['distance']
			
			teamWeek = team['week']
			teamYear = team['year']
			teamName = team['name']
			teamOpp = team['opponent']
			teamStats = team['stats']
			
			if year != teamYear:
				continue
			
			for oppKey, similarOpp in team2List.iteritems() :
				opp = similarOpp['team']
				oppDistance = similarOpp['distance']
				#print oppDistance
				oppWeek = opp['week']
				oppYear = opp['year']
				if oppYear != teamYear:
					continue
				
				oppName = opp['name']
				
				if oppName == teamName:
					continue
				
				oppOpp = opp['opponent']
				oppStats = opp['stats']
				#print 'team Distance: {0} opp Distance: {1}' .format(teamDistance, oppDistance)
				distances = teamDistance + oppDistance + 1.0
				if name == teamName and opponent == oppName :
					result[0] += (float(trainteam['home_score']) / distances)	
					result[1] += (float(trainteam['away_score']) / distances)
					#print 'home score: {0} away score: {1} result[0]: {2} result[1]: {3}' .format(trainteam['home_score'], trainteam['away_score'], result[0], result[1])
					continue
				elif name == oppName and opponent == teamName :
					result[0] += (float(trainteam['away_score'])/ distances)
					result[1] += (float(trainteam['home_score'])/ distances)
					#print result
					continue
				
			
if __name__ == '__main__':
   main()
	