import re
import sys

def metaInfo():
    print("Author: Vinit Patel")
    print("Class: CMSC-416-001-2021Spring")
    print("Date: 03/16/2021")
    print("Tagger and Scorer")
    print("---------------------------------------------------")


def process_line(line):
    line = line.strip().lower()
    return re.sub(r'[\[\]]', '', line).split()


def add_word_to_wt_dict(word_tag_dict, word, tag):
    if word in word_tag_dict:
        if tag in word_tag_dict[word]:
            word_tag_dict[word][tag] += 1
        else:
            word_tag_dict[word][tag] = 1
    else:
        word_tag_dict[word] = {tag: 1}

    # print(f'Word: {word}, Tag: {tag}, Count: {word_tag_dict[word][tag]}')
    
    return word_tag_dict

def add_word_to_dict(dictionary, word):
    if word in dictionary:
        dictionary[word] += 1
    else:
        dictionary[word] = 1

    return dictionary

def split_tag(word):
    idx = word.rfind('/')
    # print(f"Last Index of /: {idx} for {word}")

    base = word[0:idx].replace('\/', '/')
    tag = word[idx:].split('|')[0]

    return base, tag


def create_probability_dict(wt_dict, word_dict):
    prob_dict = {}

    for k, v in word_dict.items():
        # print(f"[DEBUG] Calculating Probabilities for: {k}")

        probs = {}

        for tag, count in wt_dict[k].items():
            # print(f"[DEBUG] Tag: {tag}")
            # print(f"[DEBUG] Tag Count: {count}")
            probs[tag] = count / v

        highest_tag = max(probs, key=probs.get) if probs else None

        prob_dict[k] = highest_tag

        # print(f"[DEBUG] Word: {k}, Probabilities: {probs}")
        # print(f"[DEBUG] Highest Probability: {highest_tag}")

    return prob_dict

def get_tags(lines):
    word_tag_dictionary = {}
    word_dict = {}
    tag_dict = {}

    for line in lines:
        line = process_line(line)
        for word in line:
            try:
                word, tag = split_tag(word)
            except:
                print(f"Line: {line}")
                print(f"{word.split('/')}")
                exit()
            word_tag_dictionary = add_word_to_wt_dict(word_tag_dictionary, word, tag)
            word_dict = add_word_to_dict(word_dict, word)
            tag_dict = add_word_to_dict(tag_dict, tag)


    return word_tag_dictionary, word_dict, tag_dict
    # print(word_dict)

def predict_tags(lines, prob_dict):
    predictions = {}

    for line in lines:
        line = process_line(line)
        for word in line:
            word = word.replace('\/', '/')
            if word not in prob_dict:
                predictions = add_word_to_wt_dict(predictions, word, '/nn')
            else:
                predictions = add_word_to_wt_dict(predictions, word, prob_dict[word])

    return predictions

def parse_training_tags(trainFilePath):

    with open(trainFilePath, 'r') as f:
        lines = f.readlines()

        return get_tags(lines)

def parse_test_file(testFilePath, prob_dict):

    with open(testFilePath, 'r') as f:
        lines = f.readlines()

    return predict_tags(lines, prob_dict)

# def compare_to_key(keyFilePath, predictions):

#     with open(keyFilePath, 'r'):
#         lines = f.readlines()

#     wt_dict, word_dict, tag_dict = get_tags(lines)

#     print(wt_dict)

def parseParameters():
    argv = sys.argv

    if len(argv) != 3:
        print("Run Command Example: python tagger.py pos-train.txt pos-test.txt > pos-test-with-tags.txt")
        sys.exit(1)

    return argv[1], argv[2]

def main():
    #metaInfo()
    trainFilePath, testFilePath = parseParameters()
    wt_dict, word_dict, tag_dict = parse_training_tags(trainFilePath)
    prob_dict = create_probability_dict(wt_dict, word_dict)
    predictions = parse_test_file(testFilePath, prob_dict)

    print(predictions)


if __name__ == '__main__':
    main()
