'''
Author: Vinit Patel
Class: CMSC-416 Spring 2021
Date: 04/20/2021
Assignment: Sentiment Analysis
File: sentiment.py

===========
How to run:
===========

$ python3 sentiment.py sentiment-train.txt sentiment-test.txt my-model.txt > my-sentiment-answers.txt


**********
Algorithm:
**********

1. Read in all file from parameters

Training File:
--------------
1. Read in lines from training file
2. Lowercase words, remove whitespaces, and turn into one big string
3. Retrieve all sentiments from the string
4. Remove website links, replace all user @'s with common @user,
	and replace all unnecessary characters and whitespaces
5. Retrieve all contexts (tweets) from the string
6. For each tweet, create a list of all possible n-gram permutations of the tweet
7. Create a dictionary for each ngram that keeps track of all positive and negative
	sentiments.
8. For each ngram, find the log-likelihood, add it to the dictionary, and delete the lower sentiment
9. Return the dictionary

Testing File:
-------------
1. Read in lines from training file
2. Lowercase words, remove whitespaces, and turn into one big string
3. Retrieve all sentiments and instances from the string
4. Remove website links, replace all user @'s with common @user,
	and replace all unnecessary characters and whitespaces
5. Retrieve all contexts (tweets) from the string
6. For each tweet, create a list of all possible n-gram permutations of the tweet
7. Return the list of ngrams and instances

Compare:
--------
1. For each ngram in the testing ngram list
	1. Get the associated sentiment from the training dictionary
	2. Add the log-likelihood to the appropriate sentiment
	3. Append the higher sentiment to the answer list
2. Return the list of answers

Writing Model:
--------------
1. Loop through each word in the training dictionary
2. Print out each ngram and the associated sentiment and log-likelihood
'''

import sys
import re
import math
import queue
import cProfile, pstats

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

	# Return training, testing, and model files
	return training, testing, model


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
	# Create regex for getting sentiment from answer tag
	sensesRegex = re.compile(r'<\s*answer.*?sentiment\s*=\s*"(.*?)".*?>')

	# Return all sentiments from file
	return sensesRegex.findall(lines)


def sub_lines(lines):
	# Remove all website links
	lines = re.sub(r'http[^\s]*', ' ', lines)
	
	# Replace twitter users with generic @user
	lines = re.sub(r'@[^\s]*', '@user', lines)
	
	# Remove unecessary characters
	lines = re.sub(r'[^a-zA-Z0-9\s<>@#/=\']', ' ', lines)
	
	# Remove duplicate whitespaces
	lines = re.sub(r'\s+', ' ', lines)

	# Return cleaned lines
	return lines

def clean_lines(lines):
	# Delete all newlines and trailing spaces and create one big string
	lines = ' '.join([line.strip().lower() for line in lines])
	
	# Return lines with lowercase and escape characters removed
	return lines


def createNgrams(tweet, n):
	# Intialize empty list of ngrams
	ngrams = []

	# Intialize q with size of ngram
	q = queue.Queue(maxsize=n)

	# Loop through tweet
	for idx, word in enumerate(tweet):
		# Check if the queue is 1 element from being full
		if q.qsize() == n - 1:
			# Put current word into queue
			q.put(word)

			# Turn queue into list then into a tuple
			words = tuple(list(q.queue))

			# Append the ngram to the ngram list
			ngrams.append(words)

			# Remove oldest word
			q.get()
		# If the queue is not yet close to full, put word into queue
		else:
			q.put(word)

	# Return ngram list
	return ngrams


def findLikelihood(p, n):
	# If p and n are 0 then return 0 log-likelihood
	if not p and not n:
		return 0
	# If p or n are 0 then return 4 log-likelihood
	elif not p or not n:
		return 4

	# Return the calculated log-likelihood
	return abs(math.log(p / (p + n)) / (n / (p + n)))


def findLikelihoods(training_dict):
	# Loop through all ngrams and their sentiments
	for ngrams, sentiments in training_dict.items():
		# Calculate the log-likelihood for each ngram
		sentiments['log-likelihood'] = findLikelihood(sentiments['positive'], sentiments['negative'])

		# Check if the sentiment is more positive than negative
		if sentiments['positive'] >= sentiments['negative']:
			# Remove negative sentiment if more positive
			del sentiments['negative']
		else:
			# Remove positive sentiment if more negative
			del sentiments['positive']

	# Return finished training dictionary
	return training_dict

def createDict(ngram_list, sentiments):
	# Initialize training dictionary
	training_dict = {}

	# Loop through all ngrams and sentiments
	for ngrams, sentiment in zip(ngram_list, sentiments):
		# Loop through each ngram from ngram list
		for ngram in ngrams:
			# Check if the ngram does not exists in the dictionary
			if ngram not in training_dict:
				# Create new entry for ngram
				training_dict[ngram] = {'positive': 0,
										 'negative': 0
										}
			# Add 1 to the sentiment for the ngram in dictionary
			training_dict[ngram][sentiment] += 1

	# Return the training dictionary
	return training_dict


def parseFile(file, n, is_training):
	# Get all lines from file
	with open(file, 'r') as f:
		lines = f.readlines()

	# Remove all escape characters and lower words
	lines = clean_lines(lines)

	# Get all sentiments and instances from file
	sentiments = getSentiments(lines)
	instances = getTestingInstances(lines)

	# Clean up tweets
	lines = sub_lines(lines)

	# Get all tweets
	contexts = getContexts(lines)

	# Loop through each tweet and create ngram list for each tweet
	ngram_list = [createNgrams(tweet, n) for tweet in contexts]

	# Check if the file is the training file
	if is_training:
		# Create training dictionary with list of ngrams and sentiments
		training_dict = createDict(ngram_list, sentiments)

		# Calculate all likelihoods from training dictionary
		findLikelihoods(training_dict)

		# Return training dictionary
		return training_dict

	# If this is a testing file, then return the ngram list and all instances
	return ngram_list, instances


def compare(training_dict, testing_ngrams):
	# Initialize empty list of answers
	answers = []

	# Loop through each tweet
	for ngrams in testing_ngrams:
		# Reset sum of positive and negative sentiments
		pos_sum = 0.0
		neg_sum = 0.0

		# Loop through each ngram from tweet
		for ngram in ngrams:
			# Check if the ngram is in the training dictionary
			if ngram in training_dict:
				# Check if the log-likelihood is not 0 and the sentiment is positive
				if 'positive' in training_dict[ngram] and training_dict[ngram]['log-likelihood'] != 0:
					# Add the log-likelihood to the positive sum
					pos_sum += training_dict[ngram]['log-likelihood']
				# Else if the negative log-likelihood is not 0
				elif training_dict[ngram]['log-likelihood'] != 0:
					# Add the log-likelihood to the negative sum
					neg_sum += training_dict[ngram]['log-likelihood']

		# Check if the sentiment is more positive than negative
		if pos_sum >= neg_sum:
			# Append the answer of positive to the answer list
			answers.append('positive')
		else:
			# Append the answer of negative to the answer list
			answers.append('negative')

	# Return the list of predictions
	return answers


def printModel(model_file, training_dict, n):
	# Print out model information
	with open(model_file, 'w') as f:
		# Print out n-gram Title
		f.write(f'{n}-gram Model\n')
		f.write(f'-------------------------\n')
		for ngram, sentiments in training_dict.items():
			# Print out feature with associated sentiment and log-likelihood
			f.write(f'Feature: {ngram}\n')

			for sentiment in sentiments.keys():
				f.write(f'{sentiment.capitalize()}: {training_dict[ngram][sentiment]}\n')

			f.write('\n')


def createOutputLines(instances, answers):
	# For each prediction, output the predictions to file
	for instance, answer in zip(instances, answers):
		print(f'<answer instance={instance} sentiment="{answer}"/>')


def main():
	# Ngram value
	n = 9

	# Get files
	training_file, testing_file, model_file = get_files()

	# Get training dictionary
	training_dict = parseFile(training_file, n, True)

	# Get ngrams from testing file and instances
	testing_ngrams, instances = parseFile(testing_file, n, False)

	# Get predictions
	answers = compare(training_dict, testing_ngrams)

	# Output predictions
	createOutputLines(instances, answers)

	# Print out model to file
	printModel(model_file, training_dict, n)

# Run file
if __name__ == '__main__':
	main()