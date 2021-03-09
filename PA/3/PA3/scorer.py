import sys
import re
import json


def getPredictions(predictionsFilePath):
	with open(predictionsFilePath, 'r') as f:
		predictions = f.read()

	return json.loads(predictions)

def parseParameters():
    argv = sys.argv

    if len(argv) != 3:
        print("Run Command Example: python scorer.py pos-test-with-tags.txt pos-test-key.txt > pos-tagging-report.txt")
        sys.exit(1)

    return argv[1], argv[2]



def main():
	predictionsFilePath, keyFilePath = parseParameters()
	predictions = getPredictions(predictionsFilePath)


	print(predictions)

if __name__ == '__main__':
	main()