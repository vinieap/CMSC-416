import sys
import re


def metaInfo():
    print("Author: Vinit Patel")
    print("N-gram Language Model")
    print("----------------------")


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

    print(sentences)


if __name__ == '__main__':
    main()
