'''
Author: Vinit Patel
Class: CMSC-416-001-2021Spring
Date: 03/16/2021

------
Tagger
------

The program reads in a training file of tagged (part of speech) words and uses the most likely
probability tag along with some rules to predict any untagged words.

===========
How to run:
===========

-----------
First step:
-----------

$ python tagger.py pos-train.txt pos-test.txt > pos-test-with-tags.txt

------------
Second step:
------------
$ python scorer.py pos-test-with-tags.txt pos-test-key.txt > pos-tagging-report.txt
===========

Usage:
------
The tagger will take in a training file and a testing file.
The tagger will then generate a most likely probability tag for each word
and use some rules to predict the tags for the test file.
It will then output all the predictions to the output file specified

**********
Algorithm:
**********

1. Read in the file paths for the training and testing files

Training:
---------
1. Read in the training file
2. Preprocess unnecessary things out of the line and split into tokens
3. For each token keep track of how many times the word occurs overall and how many
    times the tag occurs with that specific word
4. Loop over all words in the dictionary and calculate the probability of that tag occuring
    with the word
5. Get the highest probability tag and assign it to that word as the most likely tag


Testing:
--------
1. Read in the training file
2. Preprocess unnecessary things out of the line and split into tokens
3. For each token check if the word occurs in the probability dictionary
    3.1 If the word does occur then use the tag associated with that word
    3.2 If the word does not occur then use the '/NN' tag as default
4. Loop through all predicted tokens again to optimize using rules
5. Check each token with the previous word and next word and update tag if necessary
6. Output predictions using loop
'''

import re
import sys


def process_line(line):
    # Eliminate whitespaces, newlines, and carriage returns
    line = line.strip()

    # Eliminate phrase brackets and return list of each token
    return re.sub(r'[\[\]]', '', line).split()


def add_word_to_wt_dict(word_tag_dict, word, tag):
    # If the word and tag are in the dictionary, add 1 to the count
    if word in word_tag_dict:
        if tag in word_tag_dict[word]:
            word_tag_dict[word][tag] += 1
        # Else if the tag has not been used for that word yet
        # Add the tag to the dictionary and give value of 1
        else:
            word_tag_dict[word][tag] = 1
    # Else if the word does not occur in the dictionary
    # Add the word and the tag to the dictionary and give a value of 1
    else:
        word_tag_dict[word] = {tag: 1}
    
    # Return the modified dictionary
    return word_tag_dict

def add_word_to_dict(dictionary, word):
    # If the word is in the dictionary then add 1 to the word count
    if word in dictionary:
        dictionary[word] += 1
    # Else add word to the dictionary and give value of 1
    else:
        dictionary[word] = 1

    # Return modified dictionary
    return dictionary

def split_tag(word):
    # Get the last occurence of / in the token
    idx = word.rfind('/')

    # Get the base word without escaped '/'
    base = word[0:idx].replace('\/', '/')

    # Get the first associated tag
    tag = word[idx:].split('|')[0]

    # Return word and tag
    return base, tag


def create_probability_dict(wt_dict, word_dict):
    # Used to store probabilities
    prob_dict = {}

    # Loop through all words in the word dictionary
    for k, v in word_dict.items():
        # Dictionary to hold probabilities for current word
        probs = {}

        # For each tag for the word
        # Divide the number of times the tag is used for that word by
        # the number of times the word occurs 
        for tag, count in wt_dict[k].items():
            probs[tag] = count / v

        # Only get the highest probability tag
        highest_tag = max(probs, key=probs.get) if probs else None

        # Assign the highest probability tag to the current word
        prob_dict[k] = highest_tag

    # Return the probability dictionary
    return prob_dict


def get_tags(lines):
    # Used to store how many times a tag appears with each word
    word_tag_dictionary = {}
    # Used to store how many times a word appears in general
    word_dict = {}
    # Used to store list version of each word and tag in read-in sequential order
    to_file = []

    # Loop through all lines
    for line in lines:

        # Eliminate spaces, brackets, and split into list
        line = process_line(line)

        # Loop through all words in the line
        for word in line:

            # Split the token into the word and tag
            word, tag = split_tag(word)

            # Add the word and tag to dictionary
            word_tag_dictionary = add_word_to_wt_dict(word_tag_dictionary, word, tag)

            # Add the word to the dictionary
            word_dict = add_word_to_dict(word_dict, word)

            # Append the curent word and tag to the output list
            to_file.append((word, tag))

    # Return dictionaries and list
    return word_tag_dictionary, word_dict, to_file


# If there are any digits at all within the word
# predict a cardinal number
def rule1(word, prev, after, prediction):
    # print(word)
    if any(c.isdigit() for c in word):
        return '/CD', True
    return prediction, False


# If the previous word was a determiner and the next word is a singular noun
# the current word is more likely to be a adjective
def rule2(word, prev, after, prediction):
    if after == '/NN' and prev == 'DT':
        return '/JJ', True
    return prediction, False


# If the word ends in 'ly' then predict an adverb
def rule3(word, prev, after, prediction):
    if len(word) > 2 and word[-2:] == 'ly':
        return '/RB', True
    return prediction, False


# If the word ends in 'ing' then predict a gerund verb
def rule4(word, prev, after, prediction):
    if len(word) > 3 and word[-3:] == 'ing':
        return '/VBG', True
    return prediction, False


# If the previous word was 'to' and the prediction is a singular noun or mass,
# Then predict a base form verb instead because it occurs more often than a singlar noun
def rule5(word, prev, after, prediction):
    if prev == '/TO' and prediction == '/NN':
        return '/VB', True
    return prediction, False

def processRules(word, prev, after, prediction):
    # Process all the rules with the current word, previous word,
    # next word, and the current prediction

    # Use rule 1
    tag, result = rule1(word, prev, after, prediction)

    # If the rule is used then return new tag
    if result:
        return tag

    # Use rule 2
    tag, result = rule2(word, prev, after, prediction)

    # If the rule is used then return new tag
    if result:
        return tag

    # Use rule 3
    tag, result = rule3(word, prev, after, prediction)

    # If the rule is used then return new tag
    if result:
        return tag

    # Use rule 4
    tag, result = rule4(word, prev, after, prediction)

    # If the rule is used then return new tag
    if result:
        return tag

    # Use rule 5
    tag, result = rule5(word, prev, after, prediction)

    # If the rule is used then return new tag
    if result:
        return tag

    # If no rules could be used then stick with old prediction
    return tag


def postProcess(predictions):
    # Used for the very beginning of the file
    prev = '[START]'
    # Get the second tag in our predictions
    after = predictions[1][1]

    # List used to store final predictions
    postList = []

    # Loop through all the predictions
    for idx, (word, prediction) in enumerate(predictions):
        # Try to use rules for a better prediction
        newPrediction = processRules(word, prev, after, prediction)
        
        # Assign current word to previous word
        prev = newPrediction

        # If we are at the last element then use [END] tag for after
        if idx == len(predictions) - 1:
            after = '[END]'
        else:
            # Else we can just use the next tag in our predictions
            after = predictions[idx + 1][1]

        # Append new prediction to final list
        postList.append((word, newPrediction))

    # Return final predictions
    return postList


def predict_tags(lines, prob_dict):
    to_file = []
    words = []

    # Loop through each line
    for line in lines:
        # Eliminate spaces, brackets, and split into list
        line = process_line(line)

        # Loop through each word in the line
        for word in line:
            # Replace any escaped forward slashes for clarity
            word = word.replace('\/', '/')

            # Append to words list
            words.append(word)

    # Loop through words list
    for word in words:
        # If the word is in our training set then use it
        if word in prob_dict:
            # Get the most likely tag for that word from the probability dictionary
            prediction = prob_dict[word]
        else:
            # If the word is not in our training set then default to the tag /NN
            prediction = '/NN'

        # Append to the output list
        to_file.append((word, prediction))

    # Process all the words again but with additional rules
    to_file = postProcess(to_file)

    # Return prediction list
    return to_file

def parse_training_tags(trainFilePath):

    # Read in training file
    with open(trainFilePath, 'r') as f:
        lines = f.readlines()

    # Generate word and tag dictionary with training data 
    return get_tags(lines)

def parse_test_file(testFilePath, prob_dict):

    # Read in test file
    with open(testFilePath, 'r') as f:
        lines = f.readlines()

    # Predict tags using probability dictionary
    return predict_tags(lines, prob_dict)


def parseParameters():
    argv = sys.argv

    # Make sure we have exactly 3 arguments
    if len(argv) != 3:
        print("Run Command Example: python tagger.py pos-train.txt pos-test.txt > pos-test-with-tags.txt")
        sys.exit(1)

    # Return training and testing file paths
    return argv[1], argv[2]

def main():
    # Get the file path for the training and test dataset
    trainFilePath, testFilePath = parseParameters()

    # Parse the training file and generate the dictionary of words and tags
    wt_dict, word_dict, to_file = parse_training_tags(trainFilePath)

    # Calculate the most likely tags
    prob_dict = create_probability_dict(wt_dict, word_dict)

    # Parse and predict the test file
    to_file = parse_test_file(testFilePath, prob_dict)

    # Output the predictions
    for prediction in to_file:
        print(f'{prediction[0]}{prediction[1]}')

if __name__ == '__main__':
    main()
