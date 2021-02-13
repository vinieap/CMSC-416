import re

eliza = "ELIZA>"

name = None

interrogative_words = ['what', 'when', 'why',
                       'which', 'who', 'how', 'whose', 'whom', 'where']

reflections = {
    "i": "you",
    "you": "me",
    "am": "are",
    "are": "am",
    "i'd": "you would",
    "i'll": "you will",
    "you'll": "I will",
    "you've": "I have",
    "i've": "you have",
    "was": "were",
    "my": "your",
    "your": "my",
    "yours": "mine",
    "me": "you"
}


def remove_punctuation(query):
    return re.sub(r'[^\w\s]', '', query)


def intro():
    global name

    intro = input(
        f"{eliza} Hi, I'm a psychotheraphist. What is your name?\nUSER> ").split(' ')
    r = re.compile('[A-Z]')
    name = re.sub(r'[^\w\s]', '', list(filter(r.match, intro))[-1])


def parse_answer(query):
    query = remove_punctuation(query).lower().split()

    print(query)


def main():
    intro()

    query = input(f"{eliza} Hi {name}, How can I help you today?\n{name}> ")

    parse_answer(query)

#    while True:
#       parse_answer(query)


if __name__ == '__main__':
    main()
