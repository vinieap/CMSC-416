import sys
import re
import json
import tagger


def calcAcc(predictions, key):
	incorrect = 0
	total = 0

	biggest_inaccs = {}

	for word, prediction in predictions.items():
		for tag, count in prediction.items():
			total += count
			correctTag = tag

		for tag, count in key[word].items():
			if tag != correctTag:
				if count > 50:
					biggest_inaccs[word] = key[word]
				incorrect += count

	print(f"Incorrect: {incorrect}, Total: {total}")
	print(f"Accuracy: {format(((total - incorrect) / total * 100), '0.2f')}%")
	print(f"Biggest Inaccuracies:")
	print(json.dumps(biggest_inaccs, indent=2))


def parseKeyFile(keyFilePath):
	with open(keyFilePath, 'r') as f:
		lines = f.readlines()

	wt_dict, word_dict, tag_dict = tagger.get_tags(lines)

	return wt_dict


def getPredictions(predictionsFilePath):
	with open(predictionsFilePath, 'r') as f:
		predictions = f.read()

	return eval(predictions)


def parseParameters():
    argv = sys.argv

    if len(argv) != 3:
        print("Run Command Example: python scorer.py pos-test-with-tags.txt pos-test-key.txt > pos-tagging-report.txt")
        sys.exit(1)

    return argv[1], argv[2]


def main():
	predictionsFilePath, keyFilePath = parseParameters()
	predictions = getPredictions(predictionsFilePath)
	wt_dict = parseKeyFile(keyFilePath)

	calcAcc(predictions, wt_dict)

	# print(wt_dict)

if __name__ == '__main__':
	main()