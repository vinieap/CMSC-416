'''
Author: Vinit Patel
Date: 03/30/2021
Assignment: Word-Sense Disambiguation (Decision List)
File: wsd.py

-------------------------
Word-Sense Disambiguation
-------------------------
Word-sense disambiguation is the open problem involving identifying 
which sense of a word is used in a sentence. Humans rarely have a problem
with this but computers have a much harder time.


===========
How to run:
===========

$ python3 wsd.py line-train.txt line-test.txt my-model.txt > my-line-answers.txt

**********
Algorithm:
**********

1. Read in all files from parameters

Training File:
--------------
1. Read in lines from training file
2. Parse out punctuation, tags, and whitespace from lines
3. Parse all contexts, senses, and locations into lists from lines
4. For each word in each context, transform into Yarowsky feature based on location 
5. Count all occurences of that word into a dictionary specifiying sense and total appearance
6. Create word dictionary
	1. Calculate percentage of word appearing in training file
	2. Calculate log-liklihood for each word
7. Order word dictionary based on log-likehood

Writing Model:
--------------
1. Loop through each word in decision list
2. Print out debugging information to model file

Testing File:
-------------
1. Read in lines from testing file
2. Parse out punctuation, tags, and whitespace from lines
3. Parse all instances, contexts, and location of head tags into lists from lines
4. Loop through each context, instance, and location
	1. Check location of tags for Yarowsky potential features and add them to a list
	2. Loop through each word in the ordered decision list
		1. If feature occurs in the context then assign sense associated with word to context
		2. Break to next context
5. Print out all predictions to file
'''
import sys
import re
import math
import statistics
from collections import OrderedDict

def get_files():
	# Get all parameters
	args = sys.argv

	# Make sure 3 parameters are given else give help and exit
	if len(args) != 4:
		print('3 Arguments Expected')
		print('Expected: $ python3 wsd.py line-train.txt line-test.txt my-model.txt > my-line-answers.txt')
		exit(1)

	# Unpack parameters into individual variables
	training, testing, model = args[1], args[2], args[3]

	# Return answer and key files
	return training, testing, model


def clean_lines(lines):
	# Delete all newlines and trailing spaces and create one big string
	lines = ' '.join([line.strip().lower() for line in lines])

	# Return all lines with unnecessary tags and whitespace removed
	return remove_tags(lines)


def remove_punctuation(lines):
	# Use strings library to remove all punctuations from lines
	return re.sub(r'[.!?,;"\']', '', lines)
	# return lines.translate(str.maketrans('', '', string.punctuation))


def remove_tags(lines):
	# Remove unnecessary tags from lines
	lines = lines.replace('<s>', '')
	lines = lines.replace('</s>', '')
	lines = lines.replace('<@>', '')
	lines = lines.replace('<p>', '')
	lines = lines.replace('</p>', '')
	
	# Remove duplicate whitespaces
	lines = re.sub('\s+', ' ', lines)

	# Return cleaned lines
	return lines


def getSenses(lines):
	# Create regex for getting sense from answer tag
	sensesRegex = re.compile(r'<\s*answer.*?senseid\s*=\s*"(.*?)".*?>')

	# Return all senses from file
	return sensesRegex.findall(lines)


def getContexts(lines):
	# Create regex for getting contexts from file
	contextRegex = re.compile(r'<\s*context\s*>\s*(.*?)\s*<\s*/context\s*>\s*<\s*/\s*instance\s*>')
	
	# Get all contexts from file
	contexts = contextRegex.findall(lines)

	# Return list of all contexts split into list with all punctuations removed
	return [remove_punctuation(context).split(' ') for context in contexts]


def getTestingInstances(lines):
	# Create regex for getting instance information from testing file
	instanceRegex = re.compile(r'<\s*instance\s* id\s*=\s*(.*?)>')
	
	# Return list of all instances
	return instanceRegex.findall(lines)


def createFeatureDict(uniqueSenses):
	# Return new dictionary with all unique senses initialized with a value of 0
	return dict.fromkeys(uniqueSenses, 0)


def addToSenseDict(senseDict, word, sense):
	# If the sense is not yet in the dictionary, add it to the dictionary
	if sense not in senseDict:
		senseDict[sense] = {}
	# If the feature is not yet associated with that sense, add it
	if word not in senseDict[sense]:
		senseDict[sense][word] = 0
	# Add 1 to the count of the feature with that sense
	senseDict[sense][word] += 1

	return senseDict


def addToCountDict(countDict, word):
	# If the word is not in dictionary, add it
	if word not in countDict:
		countDict[word] = 0
	# Add 1 to the total count of that word
	countDict[word] += 1

	return countDict


def oneLeft(word):
	# Create 1 left word feature
	return 'L:' + word


def twoLeft(words):
	# Create 2 left words feature
	return '2L:' + ' '.join(words)

def oneRight(word):
	# Create 1 right word feature
	return 'R:' + word


def twoRight(words):
	# Create 2 right words feature
	return '2R:' + ' '.join(words)


def adjacent(words):
	# Create 1 left and 1 right words feature
	return 'LR:' + ' '.join(words)


def window(words, senseRegex, k):
	# Create k-left and k-right words feature
	words = [w for w in words if not re.match(senseRegex, w)]
	return str(k) + 'W:' + ' '.join(words)


def parseTraining(training, k):
	# Get all lines from training file
	with open(training, 'r') as f:
		lines = f.readlines()

	# Clean up all lines from training file
	lines = clean_lines(lines)

	# Get all senses and contexts
	senses = getSenses(lines)
	contexts = [list(filter(None, line)) for line in getContexts(lines)]
	# Get most used sense in training file
	defaultSense = statistics.mode(senses)
	# Create regex to find location of head tag in contexts
	senseRegex = re.compile(r'<head>line[s]?</head>')
	# Create all unique senses in training file
	uniqueSenses = set(senses)
	# Get location of all <head>line(s)</head> in context list
	locations = [i for context in contexts for i, c in enumerate(context) if re.search(senseRegex, c)]

	# Create sense-feature and feature dictionaries
	senseDict = {}
	countDict = {}

	# Loop through all senses, contexts, and locations
	for sense, context, location in zip(senses, contexts, locations):
		
		# Word immediately to the right
		if location + 1 < len(context):
			addToSenseDict(senseDict, oneRight(context[location + 1]), sense)
			addToCountDict(countDict, oneRight(context[location + 1]))
		# Word immediately to the left
		if location - 1 >= 0:
			addToSenseDict(senseDict, oneLeft(context[location - 1]), sense)
			addToCountDict(countDict, oneLeft(context[location - 1]))

		# 2 Words to the right
		if location + 2 < len(context):
			addToSenseDict(senseDict, twoRight(context[location + 1: location + 3]), sense)
			addToCountDict(countDict, twoRight(context[location + 1: location + 3]))

		# 2 Words to the left
		if location - 2 >= 0:
			addToSenseDict(senseDict, twoLeft(context[location - 2: location]), sense)
			addToCountDict(countDict, twoLeft(context[location - 2: location]))

		# Adjacent Words
		if location - 1 >= 0 and location + 1 < len(context):
			addToSenseDict(senseDict, adjacent(context[location - 1: location + 2 : 2]), sense)
			addToCountDict(countDict, adjacent(context[location - 1: location + 2 : 2]))

		# k-Word window
		if location - k >= 0 and location + k < len(context):
			addToSenseDict(senseDict, window(context[location - k: location + k + 1], senseRegex, k), sense)
			addToCountDict(countDict, window(context[location - k: location + k + 1], senseRegex, k))

	
	# Calculate Probabilities
	# Get all unique features and total number of features found
	numUniqueFeatures = len(countDict)
	numTotalFeatures = sum(countDict.values())
	
	# Loop through all senses
	for sense in senseDict:
		# Loop through all features
		for word in countDict:
			# Initial probability
			probability = 0

			# If the feature is associated with that sense then use it for probability
			if word in senseDict[sense]:
				probability = senseDict[sense][word] / countDict[word]
			# Else just use a very small number
			else:
				probability = 1 / (numUniqueFeatures + numTotalFeatures)

			# Assign the probability to that feature-sense
			senseDict[sense][word] = probability

	
	# Calculate Log-Likelihood
	# Create decision dictionary
	rankedDict = {}

	# Loop through all features
	for word in countDict:
		# Initial prediction, highest probability, and probabilities
		predictedSense = None
		highestProbability = 0
		probabilities = []

		# Loop through all senses
		for sense in uniqueSenses:
			# Add probability of feature with sense to list
			probability = senseDict[sense][word]
			probabilities.append(probability)

			# If the probability is higher than already found, replace with new one
			if probability > highestProbability:
				highestProbability = probability
				predictedSense = sense

		# Calculate log-likelihood and add it to the decision dictionary
		loglikelihood = abs(math.log(probabilities[0] / probabilities[1]))
		rankedDict[word + '|' + predictedSense] = loglikelihood

	# Create ordered dictionary with highest log-likelihoods at the beginning
	orderedRankedList = OrderedDict(sorted(rankedDict.items(), key=lambda x: x[1], reverse=True))

	# Return decision dictioary and default sense
	return orderedRankedList, defaultSense

def parseTesting(decision_list, testing, defaultSense, k):
	# Get all lines from training file
	with open(testing, 'r') as f:
		lines = f.readlines()

	# Clean up all lines from training file
	lines = clean_lines(lines)

	# Get all instances, locations, and contexts
	# Create regex for getting head tag locations
	instances = list(filter(None, getTestingInstances(lines)))
	contexts = [list(filter(None, line)) for line in getContexts(lines)]
	senseRegex = re.compile(r'<head>line[s]?</head>')
	locations = [i for context in contexts for i, c in enumerate(context) if re.search(senseRegex, c)]

	# Loop through all contexts, locations, and instances
	for instance, context, location in zip(instances, contexts, locations):
		# Holds all possible features to check against decision list
		possibleFeatures = []

		# Word immediately to the right
		if location + 1 < len(context):
			possibleFeatures.append(oneRight(context[location + 1]))
		# Word immediately to the left
		if location - 1 >= 0:
			possibleFeatures.append(oneLeft(context[location - 1]))

		# 2 Words to the right
		if location + 2 < len(context):
			possibleFeatures.append(twoRight(context[location + 1: location + 3]))

		# 2 Words to the left
		if location - 2 >= 0:
			possibleFeatures.append(twoLeft(context[location - 2: location]))

		# Adjacent Words
		if location - 1 >= 0 and location + 1 < len(context):
			possibleFeatures.append(adjacent(context[location - 1: location + 2 : 2]))

		# k-Word window
		if location - k >= 0 and location + k < len(context):
			possibleFeatures.append(window(context[location - k: location + k + 1], senseRegex, k))

		# Initial prediction
		predicted = ''

		# Loop through decision list with highest log-likelihood at the beginning
		for key in decision_list:
			# Split key into feature and sense
			feature, sense = key.split('|')
			
			# If the feature exists within the possible features we got, use the associated sense
			# Continue onto next context
			if feature in possibleFeatures:
				predicted = sense
				break

		# If prediction is empty, use most common sense from training file
		if predicted == '':
			predicted = defaultSense

		# Print answers to file
		print(f'<answer instance={instance} senseid="{predicted}"/>')


def writeModel(decision_list, model):
	# Write decision-list model to file
	with open(model, 'w') as f:
		f.write('Log File for wsd.py\n\n')
		f.write('------------------------------------------\n')
		f.write('Feature Words and Their Log-Likelihoods\n')
		f.write('------------------------------------------\n\n')

		# Loop through all features and output word, sense, and log-likelihood
		for word in decision_list:
			feature, sense = word.split('|')
			loglikelihood = decision_list[word]

			f.write(f'[FEATURE WORD]: {feature}\n')
			f.write(f'[LOG-LIKELIHOOD]: {loglikelihood}\n')
			f.write(f'[PREDICTED SENSE]: {sense}\n\n')

			f.write('------------------------------------------\n\n')

def main():
	# Initialize k for k-window size
	k = 2

	# Get files
	training, testing, model = get_files()

	# Generate decision list and default sense
	decision_list, defaultSense = parseTraining(training, k)

	# Write model to file
	writeModel(decision_list, model)

	# Write prediction to file using decision list
	parseTesting(decision_list, testing, defaultSense, k)


# Run file
if __name__ == '__main__':
	main()