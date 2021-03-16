'''
Author: Vinit Patel
Class: CMSC-416-001-2021Spring
Date: 03/16/2021

------
Scorer
------

===========
How to run:
===========

$ python scorer.py pos-test-with-tags.txt pos-test-key.txt > pos-tagging-report.txt

===========

Usage:
------
The scorer will take in the predicted tags and the actual tags and
compare them and give an accuracy and confusion matrix between the two
into the output file specified

**********
Algorithm:
**********

1. Read in the predictions and key file paths
2. Read in the predictions file and turn into a list of (word, tag) tuples
3. Read in the key file and use the tagger.py function get_tags
	to get a list of (word, tag) tuples
4. Simultaneously go through each list and compare their values
	4.1 If they are not equal then add 1 to the incorrect variable
5. Output accuracy using the incorrect and total variables
6. Turn the lists into pandas.Series for confusion matrix
7. Use pandas.crosstab to generate the confusion matrix
8. Output confusion matrix

Baseline (Most Likely):
***********************
Correct: 47,243
Incorrect: 9,581
Total: 56,824

Accuracy: 83.14%

After 5 Rules and Most Likely:
******************************
Correct: 48,500
Incorrect: 8,324
Total: 56,824

Accuracy: 85.35%

=======
Results
=======
+2.21% Increase in accuracy
1,257 More Correct using rules
'''

import sys
import tagger
import pandas as pd




# Information about author and program
def metaInfo():
    print("Author: Vinit Patel")
    print("Class: CMSC-416-001-2021Spring")
    print("Date: 03/16/2021")
    print("Tagger and Scorer")
    print("========================")

def calcAcc(predictions, keys):
	# Store number of inaccuracies and total number of predictions
	incorrect = 0
	total = 0

	# Loop through predictions and keys simultaneously
	for p, k in zip(predictions, keys):

		# If the tags are not the same then add to incorrect variable
		if p[1] != k[1]:
			incorrect += 1

		# Always add to total variable
		total += 1


	# Output Statistics
	print(f"Correct: {total - incorrect}")
	print(f"Incorrect: {incorrect}")
	print(f"-----------------")
	print(f"Total: {total}\n")

	print(f"Accuracy: {format(((total - incorrect) / total * 100), '0.2f')}%")
	print(f"-----------------")
	

def generateConfusionMatrix(predictions, keys):
	# Needed to disable truncation
	pd.set_option('display.expand_frame_repr', False)

	# Get only tags
	pred = [p[1] for p in predictions]
	act = [k[1] for k in keys]

	# List -> Series
	actual = pd.Series(act, name='Actual')
	predicted = pd.Series(pred, name='Predictions')

	# Create the confusion matrix
	confusion_matrix = pd.crosstab(predicted, actual)

	# Output confusion matrix to file
	print(f"Confusion Matrix:")
	print(confusion_matrix)


def parseKeyFile(keyFilePath):

	# Read the keys file
	with open(keyFilePath, 'r') as f:
		lines = f.readlines()

	# Reuse the function in tagger.py to read in key file
	_, _, keys= tagger.get_tags(lines)

	return keys


def getPredictions(predictionsFilePath):

	# Read the predictions file
	with open(predictionsFilePath, 'r') as f:
		lines = f.readlines()

	# Process each line into individual elements into a list
	predictions = [tagger.split_tag(line.strip()) for line in lines]

	return predictions


def parseParameters():
    argv = sys.argv

    # Make sure there are exactly 3 arguments
    if len(argv) != 3:
        print("Run Command Example: python scorer.py pos-test-with-tags.txt pos-test-key.txt > pos-tagging-report.txt")
        sys.exit(1)

     # Returns predictions and keys file paths
    return argv[1], argv[2]


def main():
	# Print information about author and program
	metaInfo()
	
	# Get the file paths for the predictions from the test file and the key
	predictionsFilePath, keyFilePath = parseParameters()

	# Get the predictions and keys from their respective file
	predictions = getPredictions(predictionsFilePath)
	keys = parseKeyFile(keyFilePath)

	# Calculate the accuracy of the predictions using the keys
	calcAcc(predictions, keys)

	# Create the confusion matrix of the key and predictions
	generateConfusionMatrix(predictions, keys)

	# print(wt_dict)

if __name__ == '__main__':
	main()