'''
Vinit Patel
CMSC-416 Spring 2021
04/20/2021
Sentiment Analysis
'''

import sys
import re
import math


def get_files():
	# Get all parameters
	args = sys.argv

	# Make sure 3 parameters are given else give help and exit
	if len(args) != 4:
		print('3 Arguments Expected')
		print('Expected: $ python3 sentiment.py sentiment-train.txt sentiment-test.txt my-model.txt > my-sentiment-answers.txt')
		exit(1)

	# Unpack parameters into individual variables
	training, testing, model = args[1], args[2], args[3]

	# Return answer and key files
	return training, testing, model


def remove_punctuation(lines):
	# Use strings library to remove all punctuations from lines
	return re.sub(r'[.!?,;"\']', '', lines)


def getContexts(lines):
	# Create regex for getting contexts from file
	contextRegex = re.compile(r'<\s*context\s*>\s*(.*?)\s*<\s*/context\s*>\s*<\s*/\s*instance\s*>')
	
	# Get all contexts from file
	contexts = contextRegex.findall(lines)

	# Return list of all contexts split into list with all punctuations removed
	return [context.split(' ') for context in contexts]


def getTestingInstances(lines):
	# Create regex for getting instance information from testing file
	instanceRegex = re.compile(r'<\s*instance\s* id\s*=\s*(.*?)>')
	
	# Return list of all instances
	return instanceRegex.findall(lines)


def getSentiments(lines):
	# Create regex for getting sense from answer tag
	sensesRegex = re.compile(r'<\s*answer.*?sentiment\s*=\s*"(.*?)".*?>')

	# Return all senses from file
	return sensesRegex.findall(lines)


def sub_lines(lines):
	lines = re.sub(r'http[^\s]*', ' ', lines)
	lines = re.sub(r'@[^\s]*', '@user', lines)
	lines = re.sub(r'[^a-zA-Z0-9\s<>@#/=\']', ' ', lines)
	lines = re.sub(r'\s+', ' ', lines)

	return lines

def clean_lines(lines):
	# Delete all newlines and trailing spaces and create one big string
	lines = ' '.join([line.strip().lower() for line in lines])
	
	# Return all lines with unnecessary tags and whitespace removed
	return lines


def createBigrams(tweet):
	bigrams = []
	previous_word = ''
	midpoint = (len(tweet) + 1) // 2

	for idx, word in enumerate(tweet):
		if previous_word != '':
			if idx <= midpoint:
				bigrams.append((previous_word, word + ' START'))
				previous_word = word + ' START'
			else:
				bigrams.append((previous_word, word + ' END'))
				previous_word = word + ' END'
		else:
			previous_word = word + ' START'

	return bigrams


def findCertainty(p, n):
	if not p and not n:
		return 0
	elif not p or not n:
		return 4
	return abs(math.log(p / (p + n)) / (n / (p + n)))


def findCertainties(training_dict):
	for bigram, sentiments in training_dict.items():
		sentiments['certainty'] = findCertainty(sentiments['positive'], sentiments['negative'])

		if sentiments['positive'] >= sentiments['negative']:
			del sentiments['negative']
		else:
			del sentiments['positive']

	return training_dict

def createDict(bigram_list, sentiments):
	training_dict = {}

	for bigrams, sentiment in zip(bigram_list, sentiments):
		for bigram in bigrams:
			if bigram not in training_dict:
				training_dict[bigram] = {'positive': 0,
										 'negative': 0
										}
			training_dict[bigram][sentiment] += 1

	return training_dict


def parseTraining(training_file):

	with open(training_file, 'r') as f:
		lines = f.readlines()

	lines = clean_lines(lines)

	instances = getTestingInstances(lines)
	sentiments = getSentiments(lines)

	lines = sub_lines(lines)

	contexts = getContexts(lines)

	bigram_list = [createBigrams(tweet) for tweet in contexts]

	# print(bigrams)

	training_dict = createDict(bigram_list, sentiments)

	findCertainties(training_dict)

	print(training_dict)


def main():
	training_file, testing_file, model_file = get_files()
	parseTraining(training_file)

if __name__ == '__main__':
	main()