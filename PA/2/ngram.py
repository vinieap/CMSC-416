'''
Author: Vinit Patel
Class: CMSC-416-001-2021Spring
Programming Assignment: Ngram Language Model
Date: 03/02/2021

-------------------------------------------------------------------
An ngram language model that generates a given number of sentences
based on text files given
-------------------------------------------------------------------

Starting the program:
===================================================
$ python3 ngram n m filename1 filename2 ...
        or
$ python ngram n m filename1 filename2 ...

where:
    n - number of previous words to consider
    m - number of sentences to generate
    filename1 filename2 - any number of text files
===================================================

Algorithm:
----------

1. Loop through all files and parse each file
    1. For each line in the file
        1. Strip unnecessary symbols and empty spaces
        2. If there is an ending punctuation split into sentences
2. For all sentences create an n-gram table
    1. Start with a n-tuple of [BEGIN] to indicate begginning of sentences
    2. Loop through all sentences and add current word to the previous
        n-tuple key in dictionary
    3. If the current word is an ending punctuation then add [END]
        to n-gram table
3. For all keys in n-gram table
    1. Calculate probability of next word happening
    2. Replace word count with new probability
4. Generate m number of sentences
    1. Start with n-sized [BEGIN] tuple and random value between 0 and 1
    2. Loop through possible next words and if the probability is
        greater than or equal to the random value, append that to the
        current sentence
    3. Update n-sized tuple previous words and continue
    4. Once [END] is chosen, end current sentence and start new sentence
5. Post-processing sentences
    1. Join words by spaces and correct spacing with punctuations
    2. Print out the sentences
'''

import sys
import re
from random import random


# Print out information about the author and program
def metaInfo():
    print("Author: Vinit Patel")
    print("Class: CMSC-416-001-2021Spring")
    print("Date: 03/02/2021")
    print("N-gram Language Model")
    print("---------------------------------------------------")
    print("This program generates random sentences based on a ngram model")
    print("The words are decided based on the number of previous words to consider")
    print("and the input text files")
    print("---------------------------------------------------")


def getParameters():
    # Get parameters
    args = sys.argv

    # If not enough parameters then print out instructions
    if len(args) < 4:
        print("How to run:")
        print("---------------------------------------------------")
        print("python ngram.py n m filename1 filename2 ...")
        print("---------------------------------------------------")
        print("n - n-gram value")
        print("m - Number of randomly generated ouput sentences")
        print("filename1 filename2... - Any number of filenames")
        print("---------------------------------------------------")

        sys.exit()

    # Assign parameters to proper variables
    nGram = int(args[1])
    numOuputSentences = int(args[2])
    filenames = list()

    # Get all file names inputted
    for x in args[3:]:
        filenames.append(x)

    return nGram, numOuputSentences, filenames

    # Debug Arguments
    # print(f"nGram: {nGram}")
    # print(f"Number of sentences: {numOuputSentences}")
    # print(f"Files: {filenames}")


def updateTable(table, word, previousWords):
    # If the previous words are already a key
    # and the current word is a value
    # Add one to the word count
    if previousWords in table:
        if word in table[previousWords]:
            table[previousWords][word] += 1
        else:
            # If the word is not a value
            # Create an entry with count 1
            table[previousWords][word] = 1
    else:
        # If key not in table
        # Create key with new current word of count 1
        table[previousWords] = {word: 1}

    return table


def updatePreviousWords(previousWords, word):
    # Create new list of previous words
    # Removing first index and adding new word in last index
    newWords = list(previousWords[1:]) + [word]

    # Return the tuple of the previous words
    return tuple(newWords)


def createNgramTable(sentences, nGram):
    # Initialize previous words list
    previousWords = list()

    # Create n-sized list of initial previous words
    for n in range(nGram):
        previousWords.append("[BEGIN]")

    # Turn list into tuple for performance lookup increase
    tuplePreviousWords = tuple(previousWords)

    # Initialize ngram table
    table = {tuplePreviousWords: {}}

    # Loop through each word in each sentence
    for sentence in sentences:
        for word in sentence:
            # Update the current table with new word and previous n words
            table = updateTable(table, word, tuplePreviousWords)

            # Update the pervious n words with current word
            tuplePreviousWords = updatePreviousWords(tuplePreviousWords, word)

        # Update table with previous n words and [END] tag
        # Reinitialize previous n words with starting tags
        table = updateTable(table, '[END]', tuplePreviousWords)
        tuplePreviousWords = tuple(previousWords)

    # print(table)

    # Return ngram table
    return table


def getFreqTable(table):
    # Loop through every key in ngram table
    for _, words in table.items():
        # Initialize counter and pervious word counter
        count = 0
        previous = 0

        # Loop through each key values and update counter with count
        for k in words:
            count += words[k]

        # Loop through each key and update each count with new probability
        for k in words:
            previous += words[k] / count
            words[k] = previous

    # Return frequency table
    return table

# Source: https://stackoverflow.com/questions/15950672/join-split-words-and-punctuation-with-punctuation-in-the-right-place


def correct_punctuation(sentence):
    # Create set of symbols for correcting spacing
    punctuations = set('.?!,;\'"()[]{}:')

    # Create iterable for sentence
    sentence = iter(sentence)

    # Get next word in sentence
    currWord = next(sentence)

    # For each word in sentence
    # If next word is a symbol in the set, add word to current word
    # Else just assign new word to current word
    for word in sentence:
        if word in punctuations:
            currWord += word
        else:
            yield currWord
            currWord = word

    # Return ending word (punctuation)
    yield currWord


def generate_sentences(table, nGram, numOfSentences):
    # Initialize lists for tracking sentences and previous words
    allSentences, currSentence, previousWords = list(), list(), list()

    # Initialize starting tag list
    for n in range(nGram):
        previousWords.append("[BEGIN]")

    # Declare initial tuple key and current n previous word tuple
    initialTuple, tuplePreviousWords = tuple(
        previousWords), tuple(previousWords)

    # Tracks if word is found
    foundWord = False

    # Track sentence count
    sentenceCount = 0

    # Loop for m number of sentences
    while sentenceCount < numOfSentences:
        # Choose random number between 0 and 1
        random_value = random()

        # Declare found word to false
        foundWord = False

        # Loop through the values of key of previous words
        for k, v in table[tuplePreviousWords].items():
            # Check if the probability is greater than the random value
            if random_value <= v and not foundWord:

                # Check if current previous words is not just starting tags
                if initialTuple != tuplePreviousWords:
                    # If word is i, replace with capital
                    if tuplePreviousWords[-1] == 'i':
                        currSentence.append('I')
                    # Else just add word to current sentence
                    else:
                        currSentence.append(tuplePreviousWords[-1])

                # Update previous words with current word
                tuplePreviousWords = updatePreviousWords(tuplePreviousWords, k)

                # Check if current word was ending word
                if tuplePreviousWords[-1] == '[END]':
                    # Add sentence to all sentence list
                    allSentences.append(currSentence)

                    # Reinitialize previous words with starting tags
                    tuplePreviousWords = initialTuple

                    # Add one to sentence count
                    sentenceCount += 1

                    # Reinitialize current sentence to empty list
                    currSentence = list()

                # Choose another random number
                random_value = random()

                # Declare word is found
                foundWord = True

    # Split sentences with correct spacing
    split_sentences = [' '.join(correct_punctuation(sentence))
                       for sentence in allSentences]

    print(f"{numOfSentences} Randomly Generated Sentences")
    print("---------------------------------------------------")

    # Print out each generated sentence
    for idx, sentence in enumerate(split_sentences):
        print(f"{idx + 1}. {sentence.capitalize()}")


def parseLine(word):
    # Replace unncessary symbols with empty string
    word = re.sub(r"[^a-zA-Z0-9\s?!.,;]", "", word)

    # Split line into individual words
    partialList = re.split('(\W+?)', word.lower())

    # Used for eliminating duplicate spaces
    emptyList = ['', ' ']

    # Eliminate duplicate spaces
    processedList = [x for x in partialList if x not in emptyList][:-1]

    # If line is not None return list, else return None
    if processedList:
        return processedList


def findSentences(lines, nGram):
    # Initialize all sentences and current sentence
    sentences, sentence = list(), list()

    # Loop through each word in each line and append to
    # current sentence until ending punctuation
    # Then append sentence to list of sentences and
    # create empty current sentence
    for line in lines:
        for word in line:
            if (word == '.' or word == '?' or word == '!') and sentence:
                sentence.append(word)
                if len(sentence) >= nGram:
                    sentences.append(sentence)
                sentence = list()
                continue
            sentence.append(word)

    return sentences


def parseFile(filename, nGram):
    # Initialize lines list
    parsedLines = list()

    # Loop through file and parse line by line
    with open(filename, 'r', encoding='utf-8-sig') as f:
        # Read in all lines
        lines = f.readlines()

        # Loop through each line and parse the line
        for line in lines:
            parsedLine = parseLine(line)

            # If line was empty then move to next line
            if not parsedLine:
                continue

            # Append line to parsed lines list
            parsedLines.append(parsedLine)

    # Find all sentences from lines list
    return findSentences(parsedLines, nGram)


def main():
    # Print all meta information
    metaInfo()

    # Get parameters
    nGram, numOuputSentences, filenames = getParameters()

    # Initialze sentences list
    sentences = list()

    # Loop through each file and parse file and get all sentences
    for filename in filenames:
        sentences.extend(parseFile(filename, nGram))

    # DEBUGGING
    # Initialize token count
    token_total = 0

    # Loop through each sentence and get token count and add to counter
    for sentence in sentences:
        token_total += len(sentence)

    # Create ngram and frequency table
    table = getFreqTable(createNgramTable(sentences, nGram))

    # Generate m sentences
    generate_sentences(table, nGram, numOuputSentences)

    # DEBUG
    # print(table)

    # print(f"[DEBUG] # of Tokens: {token_total}")
    # print(f"[DEBUG] # of Sentences: {len(sentences)}")
    # print(f"[DEBUG] Table Length: {len(table)}")


# Start program
if __name__ == '__main__':
    main()
