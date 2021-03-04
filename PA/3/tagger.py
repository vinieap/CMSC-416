import re


def metaInfo():
    print("Author: Vinit Patel")
    print("Class: CMSC-416-001-2021Spring")
    print("Date: 03/16/2021")
    print("Tagger and Scorer")
    print("---------------------------------------------------")


def remove_brackets(line):
    return re.sub(r'[\[\]]', '', line)


def add_word_to_dict(tag_dict, word, tag):


    if word in tag_dict:
        if tag in tag_dict[word]:
            tag_dict[word][tag] += 1
        else:
            tag_dict[word][tag] = 1
    else:
        tag_dict[word] = {tag: 1}

    print(f'Word: {word}, Tag: {tag}, Count: {tag_dict[word][tag]}')
    
    return tag_dict

def split_tag(word):
    splitted = word.split('/')

    # TODO
    # Fix weird 1\\/2/cd tagging

    for idx, w in enumerate(splitted):
        if w[-1] == '\\':
            splitted[idx] = splitted[idx].replace('\\', '/')
            splitted[idx : idx + 1] = [''.join(splitted[idx : idx + 1])]
            print(splitted)
            return splitted

    return splitted
            

def get_tags(lines):
    tag_dictionary = {}

    for line in lines:
        line = remove_brackets(line.strip().lower()).split()
        for word in line:
            try:
                word, tag = split_tag(word)
            except:
                print(f"Line: {line}")
                print(f"{word.split('/')}")
                exit()
            add_word_to_dict(tag_dictionary, word, tag)


def parse_tags():

    with open('PA3/pos-train.txt', 'r') as f:
        lines = f.readlines()

        get_tags(lines)


def main():
    metaInfo()

    parse_tags()


if __name__ == '__main__':
    main()
