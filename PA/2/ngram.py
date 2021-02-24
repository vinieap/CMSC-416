'''
Author: Vinit Patel
Class: CMSC-416-001-2021Spring
Programming Assignment: Ngram Language Model
Date: 03/02/2021

-------------------------------------------------------------------
An ngram language model that generates a given number of sentences
based on text files given in
-------------------------------------------------------------------

Starting the program:
=============================================
$ python3 ngram n m
        or
$ python ngram n m

where:
    n - number of previous words to consider
    m - number of sentences to generate
=============================================
'''

import sys
import re


def metaInfo():
    print("Author: Vinit Patel")
    print("Class: CMSC-416-001-2021Spring")
    print("Date: 03/02/2021")
    print("N-gram Language Model")
    print("----------------------------")


def getParameters():
    args = sys.argv

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

    nGram = int(args[1])
    numOuputSentences = int(args[2])
    filenames = list()

    for x in args[3:]:
        filenames.append(x)

    return nGram, numOuputSentences, filenames

    # Debug Arguments
    # print(f"nGram: {nGram}")
    # print(f"Number of sentences: {numOuputSentences}")
    # print(f"Files: {filenames}")


def updateTable(table, word, previousWords):
    if previousWords in table:
        if word in table[previousWords]:
            table[previousWords][word] += 1
        else:
            table[previousWords][word] = 1
    else:
        table[previousWords] = {word: 1}

    return table


def updatePreviousWords(previousWords, word):
    newWords = list(previousWords[1:]) + [word]

    return tuple(newWords)


def createNgramTable(sentences, nGram):
    previousWords = list()

    for n in range(nGram):
        previousWords.append("[BEGIN]")

    tuplePreviousWords = tuple(previousWords)

    table = {tuplePreviousWords: {}}

    for sentence in sentences:
        for word in sentence:

            table = updateTable(table, word, tuplePreviousWords)

            tuplePreviousWords = updatePreviousWords(tuplePreviousWords, word)

        table = updateTable(table, '[END]', tuplePreviousWords)
        tuplePreviousWords = tuple(previousWords)

    # print(table)

    return table


def getFreqTable(table):
    for _, words in table.items():
        count = 0
        previous = 0

        for k in words:
            count += words[k]

        for k in words:
            previous += words[k] / count
            words[k] = previous

    return table


def parseLine(word):
    partialList = re.split('(\W+?)', word.lower())
    emptyList = ['', ' ']

    processedList = [x for x in partialList if x not in emptyList][:-1]

    if processedList:
        return processedList


def findSentences(lines, nGram):
    sentences = list()
    sentence = list()

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
    parsedLines = list()

    with open(filename, 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()
        for line in lines:
            parsedLine = parseLine(line)
            if not parsedLine:
                continue
            parsedLines.append(parsedLine)

    return findSentences(parsedLines, nGram)


def main():
    metaInfo()
    nGram, numOuputSentences, filenames = getParameters()

    sentences = list()

    for filename in filenames:
        sentences.extend(parseFile(filename, nGram))

    table = getFreqTable(createNgramTable(sentences, nGram))

    print(table)


if __name__ == '__main__':
    main()
