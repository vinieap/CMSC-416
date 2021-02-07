import re

name = None

interrogative_words = ['what', 'when', 'why', 'which', 'who', 'how', 'whose', 'Whom', 'where']

def intro():
    global name

    intro = input(
        "Hi, I'm a psychotheraphist. What is your name?\n").split(' ')
    r = re.compile('[A-Z]')
    name = re.sub(r'[^\w\s]', '', list(filter(r.match, intro))[-1])

def parse_question(question):
    print(f'That is a question')

def parse_answer(query):
    query = query.lower().split(' ')

    if query[0] in interrogative_words or query[-1][-1] == '?':
        parse_question(query)

def main():
    intro()

    query = input(f"Hi {name}, How can I help you today?\n")

    while True:
        parse_answer(query)

if __name__ == '__main__':
    main()
