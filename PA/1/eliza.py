'''
Author: Vinit Patel
Class: CMSC-416-001-2021Spring

Eliza Bot:
----------
A bot that acts as a psychotheraphist and responds to whatever the user says.

What the bot looks for:
______________________________________________________________________________
The bot looks for words that are typically associated with feelings,
such as love, hate, feel, and questions. This allows for a more directed
conversation and a narrower range of responses that the user could input and
improves the bots ability to respond properly.
______________________________________________________________________________

*********************************************************************
*** Proper capitalization, punctuation, and grammar are expected. ***
*********************************************************************
'''

import re
import random
import sys

# Used for Bot name
eliza = "ELIZA>"

# Used for User name usage
name = None

# Reflects personal pronouns for responses
reflections = {
    "i am": "you are",
    "i was": "you were",
    "i": "you",
    "i'm": "you are",
    "i'd": "you would",
    "i've": "you have",
    "i'll": "you will",
    "my": "your",
    "you are": "I am",
    "you were": "I was",
    "you've": "I have",
    "you'll": "I will",
    "your": "my",
    "yours": "mine",
    "you": "me",
    "me": "you",
}

# List of possible responses for bot in regex tuples
answers = (
    (r"You(?:re|'re|\sare) (.*)",
        (
            "Why do you think I'm %1",
            "Why do you say that?",
            "What makes you think I'm %1"
        )
     ),

    (r"How (.*)",
        (
            "That is a question you must answer yourself",
            "Why are you asking that?"
        )
     ),

    (r"(?:I\sam|I'?m) sorry (.*)",
        (
            "Don't be sorry.",
            "What are you sorry for?",
            "Don't apologize {name}."
        )
     ),

    (r"(?:Be)?cause (.*)",
        (
            "Do you truly feel that is valid reasoning?",
            "Is that the true reason why?"
        )
     ),

    (r"Is it (.*)",
        (
            "Do you think it is %1?",
            "Why do you think that?"
        )
     ),

    (r"I(?:\swould|'?d) (.*)",
        (
            "Why would you %1?",
            "Is that something you would really do?",
            "How would you %1?"
        )
     ),

    # Checks for (I will, I'll, I'm gonna, I am gonna, I'm going to, and I am going to)
    (r"I(?:\swill|'?ll|'?m\sgonna|\sam\sgonna|'?m\sgoing\sto|\sam\sgoing\to) (.*)",
        (
            "When are you going to %1?",
            "How are you going to %1?"
        )
     ),

    (r"It is (.*)",
     (
         "Why do you think it is %1?",
         "Is it really?"
     )
     ),

    (r"Are you (.*)",
     (
         "Why are you asking that?",
         "Does it matter if I am %1?",
         "Do you believe I am?"
     )
     ),

    (r"What is (.*)",
        (
            "What do you think %1 is?",
            "Why are you asking %1?"
        )
     ),

    (r"What (.*)",
        (
            "What do you think?",
            "What are your thoughts about that?"
        )
     ),

    (r"I need (.*)",
        (
            "Why is it that you need %1?",
            "Do you really need %1?",
            "How would it benefit you to have %1?",
            "What is stopping you from getting %1?"
        )
     ),

    (r"I want (.*)",
        (
            "Why is it that you want %1?",
            "Why do you want %1?"
        )
     ),

    (r"I love (.*)",
        (
            "Tell me why you love %1.",
            "Why do you love %1?"
        )
     ),

    (r"I hate (.*)",
        (
            "Tell me why you hate %1.",
            "Why do you hate %1?"
        )
     ),

    (r"(?:.*) (family|husband|wife|father|mother|brother|sister|daughter|son|child|grandmother|grandfather|grandpa|grandma|mom|dad)",
     (
         "Tell me more about your %1?",
         "How is your relationship with your %1?",
         "Do you think your relationship with your %1 affected you in anyway?"
     )
     ),

    (r"(?:.*) (school)",
     (
         "Can you expand on how school makes you feel?",
         "Does school stress you out?",
     )
     ),

    (r"(?:.*) (friends?)",
     (
         "How is your relationship with your %1?",
         "Do you like your %1?"
     )
     ),

    (r"I think (.*)",
        (
            "Why do you think that?",
            "What makes you think that?",
            "What reason do you think %1?"
        )
     ),

    # Couldn't think of a more general response without messing up conjugation
    (r"I (\w+)e\b",
        (
            "Is this something you've always %1ed?",
            "Why is that?"
        )

     ),

    (r"(?:I|I'?m) feel(?:ing)? (.*)",
        (
            "Why do you feel %1?",
            "What caused you to feel that way?",
            "Do you feel like that often?",
            "How you deal with feeling like that?"
        )
     ),

    (r"(?:I'?m|I am) (.*)",
        (
            "Why are you %1?",
            "Tell me more about why you are %1."
        )
     ),

    (r"I don(?:'?t) know",
        (
            "Why do you think you don't know?",
            "Can you elborate what you don't know?",
            "How does it make you feel not knowing?",
        )
     ),

    (r"Can I (.*)",
     (
         "Is there a reason you cannot $1?",
         "What is stopping you from doing that?"
     )
     ),

    (r"Why (.*)",
     (
         "What is your thoughts on that?",
         "Why do you think so?"
     )
     ),

    (r"(?:No|Nah|Nope)(.*)",
        (
            "Can you elborate why you said no?",
            "Why not?"
        )
     ),

    (r"(?:Yes|Yeah|Yea|Yep|Of\scourse)(.*)",
        (
            "Can you elborate why you said yes?",
            "Why?"
        )
     ),

    (r"Goodbye(.*)",
        (
            "Goodbye {name}.",
            "See you next time {name}.",
            "Have a nice day {name}."
        )
     ),

    (r"(?:.*) (homework|assignments?|projects?|work)",
     (
         "Have you been keeping up with your %1?",
         "Is your %1 easy or difficult?"
     )
     ),

    # Check for any positive associations
    (r"(good|great|excellent|exceptional|marvelous|satisfying|superb|wonderful|nice|awesome|amazing)",
        (
            "Why do you think it's %1?",
            "Why do you feel positively about that?"
        )
     ),

    # Check for any positive associations
    (r"(bad|horrible|inferior|unsatisfactory|inadequate|nasty|awful|grim|unpleasant|terrible|dreadful)",
        (
            "Why do you think it's %1?",
            "Why do you feel negatively about that?"
        )
     ),

    # Check for any feeling words and expand on that feeling
    (r"(?:.*)(easy|amazed|happy|lucky|overjoyed|thankful|glad|cheerful|elated|courageous|optimistic|impulsive|wonderful|thrilled|calm|peaceful|comfortable|pleased|suprised|content|loved|hated|passionate|sensitive|concerned|affected|fascinated|intrigued|engrossed|curious|eager|anxious|inspired|determined|excited|enthusiastic|brave|challenged|confident|hopeful|insecure|irritated|enraged|insulting|annoyed|upset|hateful|unpleasant|offensive|resentful|infuriated|lousy|disappointed|ashamed|powerless|guilty|dissatisfied|miserable|despicable|disgusting|alone|useless|inferior|pathetic|neutral|stressing|depressed|depressing|stressed|tired|boring|bored|interested|fearful|terrified|nervous|scared|timid|restless|doubtful|wary|grief|anguish|desperate|unhappy|lonely)",
        (
            "Why do you feel %1?",
            "What reasons do you feel %1?",
            "Do you wanna feel this way?"
        )
     ),

    (r"(.*)",
        (
            "Can you elaborate more?",
            "Please tell me more."
        )
     )
)


# Compile all regex responeses
responses = [(re.compile(a, re.I), b) for (a, b) in answers]


# Remove ending punctuation because responses are already punctuated
def remove_punctuation(query):
    return query.rstrip('?!.')


# Transform personal pronouns to POV of the bot
def reflective_transformation(query):
    # Loop over query and replace all personal pronouns with their reflection
    for idx, word in enumerate(query):
        if word in reflections:
            query[idx] = reflections[word]
    # Return a string instead of a list
    return ' '.join(query)


# Introduce bot and get user's name
def intro():
    global name

    # Introduce bot
    print(f"{eliza} Hello my name is Eliza and I'm a psychotheraphist bot.")
    print(f"{eliza} Whenever you feel tired of the conversation, please say 'Goodbye'.")
    print(f"{eliza} What is your name?")

    # Split user's response into list of strings
    intro = input("USER> ").split(' ')

    # Get only words with capital letters
    r = re.compile('[A-Z]')

    # Typically the name is the last capital word in an introduction
    name = remove_punctuation(list(filter(r.match, intro))[-1])


# Parse through possible responses and generate a response
def parse_answer(query):
    # Remove ending punctuation
    query = remove_punctuation(query)

    # Compile exiting statement
    goodbye = re.compile(r'goodbye', re.I)

    # Loop through all possible responses and get first response with match
    for (response, answer) in responses:
        if match := response.match(query):
            # Transform all personal pronouns to POV of bot
            reflected_match = reflective_transformation(
                match.group(1).lower().split(' '))

            # Choose a random response from possible responses
            ans = random.choice(answer)

            # Replace response with captured information
            ans = re.sub(r"\%1", reflected_match, ans)

            # Replace name with User's name
            ans = re.sub(r"\{name\}", name, ans)

            # If response is goodbye then exit
            if goodbye.search(query):
                print(f'ELIZA> {ans}')
                sys.exit()

            # Return bot's response
            return ans


# Main loop where bot keeps responding until User wants to exit
def main():
    # Introduce bot and get user's name
    intro()

    # Initiate conversation
    query = input(f"{eliza} Hi {name}. How can I help you today?\n{name}> ")

    # Converse and respond until user exits
    while True:
        ans = parse_answer(query)
        print(f"ELIZA> {ans}")
        query = input(f"{name}> ")


if __name__ == '__main__':
    main()
