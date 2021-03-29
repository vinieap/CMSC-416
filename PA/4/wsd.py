'''
Author: Vinit Patel
Date: 03/30/2021
Assignment: Word Sense Disambiguation (Decision List)
'''
import sys
import re


def get_files():
	args = sys.argv

	if len(args) != 4:
		print('3 Arguments Expected')
		print('Expected: $ python3 wsd.py line-train.txt line-test.txt my-model.txt > my-line-answers.txt')
		exit(1)

	training, testing, model = args[1], args[2], args[3]

	return training, testing, model


def strip_line(line):
	return line.strip()


def remove_tags(lines):
	lines = lines.replace('<s>', '')
	lines = lines.replace('</s>', '')
	lines = lines.replace('<@>', '')
	lines = lines.replace('<p>', '')
	lines = lines.replace('</p>', '')
	lines = re.sub('\s+', ' ', lines)

	return lines


def parse_training_file(training_file):

	with open(training_file, 'r') as f:
		lines = f.readlines()

	lines = ' '.join([strip_line(line) for line in lines])

	lines = remove_tags(lines)

	contexts, answers, = [], []

	

	print(lines)

def main():
	training, testing, model = get_files()
	parse_training_file(training)


if __name__ == '__main__':
	main()