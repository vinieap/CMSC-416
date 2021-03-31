'''
Author: Vinit Patel
Date: 03/30/2021
Assignment: Word Sense Disambiguation (Decision List)
File: wsd.py

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
3. Parse all contexts and senses into lists from lines
4. For each word in each context count all occurences of that word into a dictionary specifiying sense
5. Create word dictionary
	1. Loop through count dictionary and calculate most likely sense for each word
	2. Calculate log-liklihood for each word
	3. Calculate percentage of word appearing in training file
6. Order word dictionary based on log-likehood and then number of occurences after

Writing Model:
--------------
1. Loop through each word in decision list
2. Print out debugging information to model file

Testing File:
-------------
1. Read in lines from testing file
2. Parse out punctuation, tags, and whitespace from lines
3. Parse all instances and contexts into lists from lines
4. Loop through each context
	1. Loop through each word in the ordered decision list
		1. If word occurs in the context then assign sense associated with word to context
		2. Break to next context
5. Print out all predictions to file
'''
import sys
import re
import string
from collections import OrderedDict
import math


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


def remove_punctuation(lines):
	# Use strings library to remove all punctuations from lines
	return lines.translate(str.maketrans('', '', string.punctuation))


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


def createCountDict(lines, senses, contexts):
	# Initialize count dictionary
	countDict = {}
	# Get all unique senses
	uniqueSenses = set(senses)

	# Loop through all senses and their contexts
	for sense, context in zip(senses, contexts):
		# Loop through all words in the context
		for word in context:
			# If the word is not in the dictionary add it to the dictionary
			if word not in countDict:
				# Create entry for word in dictionary
				countDict[word] = createFeatureDict(uniqueSenses)
			
			# Add 1 to sense for that word in the dictionary
			countDict[word][sense] += 1

	# Return dictionary
	return countDict


def createWordDict(countDict):
	# Initialize word dictionary
	wordDict = {}

	# Loop through all words in count dictionary
	for word in countDict:
		# Loop through all senses and their counts for that word
		for sense, count in countDict[word].items():
			# If the word is not in the dictionary then create entry for word
			if word not in wordDict:
				# Create entry
				wordDict[word] = {}
				# Set keys to default values for word
				wordDict[word]['total'] = 0
				wordDict[word]['maxSense'] = sense
				wordDict[word]['maxSenseCount'] = count
			# Else if the current sense count is higher than the highest sense count
			# then replace word in the dictionary
			elif count > wordDict[word]['maxSenseCount']:
				# Replace sense and max count
				wordDict[word]['maxSense'] = sense
				wordDict[word]['maxSenseCount'] = count
			
			# Add count to total of word count
			wordDict[word]['total'] += count

	# Loop through all words in the dictionary
	for word in wordDict:
		# Create entry for each word for percentage of times word occurred in file
		wordDict[word]['percentageSense'] = wordDict[word]['maxSenseCount']/ wordDict[word]['total']
		# If the word only appeared with a certain sense then set log-likelihood to 1
		# Else calculate the log-likelihood for the word
		if wordDict[word]['percentageSense'] != 1.0:
			wordDict[word]['log-likelihood'] = abs(math.log(wordDict[word]['maxSenseCount'] / (wordDict[word]['total'] - wordDict[word]['maxSenseCount'])))
		else:
			wordDict[word]['log-likelihood'] = 1

	# Return word dictionary
	return wordDict


def clean_lines(lines):
	# Delete all newlines and trailing spaces and create one big string
	lines = ' '.join([line.strip().lower() for line in lines])

	# Return all lines with unnecessary tags and whitespace removed
	return remove_tags(lines)


def parse_training_file(training_file):

	# Get all lines from training file
	with open(training_file, 'r') as f:
		lines = f.readlines()

	# Clean up all lines from training file
	lines = clean_lines(lines)

	# Get all senses and contexts
	senses = getSenses(lines)
	contexts = [list(filter(None, line)) for line in getContexts(lines)]

	# Count words in context
	# Create dictionary with most likely sense and highest likelihoods
	countDict = createCountDict(lines, senses, contexts)
	wordDict = createWordDict(countDict)

	# Sort by accuracy, then frequency into new dictionary (highest -> lowest)
	orderedWords = OrderedDict(sorted(wordDict.items(), key=lambda x: (x[1]['log-likelihood'], x[1]['maxSenseCount']), reverse=True))

	# Return ordered decision list of words
	return orderedWords


def parse_testing_file(testing_file, orderedWords):

	# Get all lines from testing file
	with open(testing_file, 'r') as f:
		lines = f.readlines()

	# Clean up all lines from testing file
	lines = clean_lines(lines)

	# Get all instances and contexts from testing file
	instances = list(filter(None, getTestingInstances(lines)))
	contexts = [list(filter(None, line)) for line in getContexts(lines)]
	
	# Initialize predictions list
	predictions = []

	# Loop through every context in file
	for context in contexts:
		# Loop through every word in decision list
		for word in orderedWords:
			# If the word in decision list appears in context then apped the predicted sense
			# for that word to the predictions list
			# Then go onto next context
			if word in context:
				predictions.append(orderedWords[word]['maxSense'])
				break

	# Loop through all predictions and output answers to file
	for prediction, instance in zip(predictions, instances):
		print(f'<answer instance={instance} senseid="{prediction}"/>')


def write_model(model, orderedWords):
	# Write out information for decision list to file
	# Information Outputted:
	# --------------------------
	# Word
	# How many times word occurs in sense context
	# How many times word occurs overall in file
	# The log-likelihood of the word
	# The predicted sense for that word
	with open(model, 'w') as f:
		f.write('Log File for wsd.py\n\n')
		f.write('------------------------------------------\n')
		f.write('Feature Words and Their Log-Likelihoods\n')
		f.write('------------------------------------------\n\n')

		for word in orderedWords:
			f.write(f'[FEATURE WORD]: {word}\n')
			f.write(f'[SENSE OCCURENCES]: {orderedWords[word]["maxSenseCount"]}\n')
			f.write(f'[TOTAL OCCURENCES]: {orderedWords[word]["total"]}\n')

			log = 1

			if orderedWords[word]['total'] != orderedWords[word]['maxSenseCount']:
				log = abs(math.log(orderedWords[word]['maxSenseCount'] / (orderedWords[word]['total'] - orderedWords[word]['maxSenseCount'])))

			f.write(f'[LOG-LIKELIHOOD]: {log}\n')
			f.write(f'[PREDICTED SENSE]: {orderedWords[word]["maxSense"]}\n\n')

			f.write('------------------------------------------\n\n')

def main():
	# Get files
	training, testing, model = get_files()

	# Parse training file and create decision list
	orderedWords = parse_training_file(training)

	# Output model to file
	write_model(model, orderedWords)

	# Predict senses on test file
	parse_testing_file(testing, orderedWords)


# Run file
if __name__ == '__main__':
	main()