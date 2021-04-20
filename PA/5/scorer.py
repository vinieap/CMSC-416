'''
Author: Vinit Patel
Class: CMSC-416 Spring 2021
Date: 04/20/2021
Assignment: Sentiment Analysis
File: scorer.py

===========
How to run:
===========

$ python3 scorer.py my-sentiment-answers.txt sentiment-test-key.txt

**********
Algorithm:
**********

1. Read in all files from parameters
2. Parse each file and get the instances and sentiments for both
3. Loop through keys and check if key matches prediction
	1. If match then add 1 to correct
4. Create Pandas Series for predictions and keys
5. Use pandas.crosstab to create confusion matrix
6. Print out information and confusion matrix

-------------------
Results (Accuracy):
-------------------
72.41% w/ 1-gram [BEST]
71.55% w/ 2-gram
66.38% w/ 3-gram [WORST]
68.53% w/ 4-gram
68.97% w/ 5-gram
68.53% w/ 6-gram
69.83% w/ 7-gram
69.83% w/ 8-gram
69.40% w/ 9-gram
'''
import sys
from sentiment import getSentiments
import pandas as pd
import re


def getAnswerInstances(lines):
	# Create regex for getting instance information from key files
	instanceRegex = re.compile(r'<answer instance="(.*?)" sentiment=".*?"/>')
	
	# Return list of all instances
	return instanceRegex.findall(lines)

def get_files():
	# Get all parameters
	args = sys.argv

	# Make sure 2 parameters are given else give help and exit
	if len(args) != 3:
		print('2 Arguments Expected')
		print('Expected: $ python3 scorer.py my-sentiment-answers.txt sentiment-test-key.txt')
		exit(1)

	# Unpack parameters into individual variables
	answers, key = args[1], args[2]

	# Return answer and key files
	return answers, key


def getAnswers(file):
	# Get all lines from file
	with open(file, 'r') as f:
		lines = f.readlines()

	# Delete all newlines and trailing spaces and create one big string
	lines = ' '.join([line.strip() for line in lines])

	# Call getSentiments and getInstances from wsd.py on file lines
	sentiments = getSentiments(lines)
	instances = getAnswerInstances(lines)

	# Return dictionary of instances and sentiments with instances as key and sentiments as values
	return dict(zip(instances, sentiments))


def compare(answers, keys):
	# Initialize correct answers to 0
	correct = 0

	# Loop through keys
	for key in keys:
		# If the instance in the predictions is equal to the key then add 1 to correct
		if keys[key] == answers[key]:
			correct += 1

	# Print information
	print(f'Correct: {correct}')
	print(f'Total: {len(keys)}')
	print(f'Accuracy: {100 * correct/len(keys): 0.2f}%')
	print(f'-----------------')

	# Create Pandas Series for both predictions and answers
	predictions = pd.Series(answers, name='Predictions')
	actual = pd.Series(keys, name='Actual')

	# Create confusion matrix using predictions and answers series
	confusion_matrix = pd.crosstab(predictions, actual, margins=True)

	# Print confusion matrix
	print(f'Confusion Matrix:')
	print(f'-----------------')
	print(confusion_matrix)

def main():
	# Get files
	answer_file, key_file = get_files()
	
	# Get answer file sentiments
	answers = getAnswers(answer_file)
	
	# Get key file answers
	keys = getAnswers(key_file)
	
	# Compare answers and key
	compare(answers, keys)

# Run file
if __name__ == '__main__':
	main()