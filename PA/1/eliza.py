'''
Author: Vinit Patel
Class: CMSC-416-001-2021Spring
PA: Eliza Bot
Date: 02/16/2021

------------------------------------------------------------------------------
A chat bot that acts as a psychotheraphist and attempts to respond to whatever
the user says.

What the bot looks for:
------------------------------------------------------------------------------
The bot looks for words that are typically associated with feelings,
such as love, hate, feel, and questions. This allows for a more directed
conversation and a narrower range of responses that the user could input and
improves the bots ability to respond properly.
------------------------------------------------------------------------------



*********************************************************************
*** Proper capitalization, punctuation, and grammar are expected. ***
*********************************************************************

Starting the program:
=====================
$ python3 eliza.py
        or
$ python eliza.py
=====================

Example input:
---------------
Introduction:
=============
ELIZA> What is your name?

Optional ways to answer:
~~~~~~~~~~~~~~~~~~~~~~~~
1. USER> My name is Name.
2. USER> Name.
3. USER> Name is my name.
4. USER> I'm Name.
~~~~~~~~~~~~~~~~~~~~~~~~

Sample Conversation:
====================
ELIZA> Hi Name. How can I help you today?

Optional ways to answer:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. Name> I want to be happy.
2. Name> I need to do my homework.
3. Name> Me and my friend got in an argument.
4. Name> What is the meaning of life?
5. Name> How can I stop procrastinating?
and more...
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ending Conversation:
====================
1. Name> Goodbye.
2. Name> bye
3. Name> bye bye Eliza



Algorithm:
----------
 - Store a large tuple of possible responses the user might input
   - Each tuple element is a pair of (regex , (response 1, response 2, ...))

 - Store a dictionary of reflections where the response turns from
   the POV of the user to the POV of the bot for better immersion

 - Loop endlessly until the user says some form of bye
   - Take input from the user
   - Loop over the regex tuple for possible pattern matches
   - If match is found then pick random response
   - Replace any captured patterns, names, and reflections
   - Return the chat bot's respose
 - End loop

'''

import re
import random
import sys

# Used for Bot name
eliza = "ELIZA>"

# Used for User name usage
name = None

# All possible reflections for User POV to Bot POV
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
    # Check for generic negative question
    (r"(Why not)",
        (
            "That is something you should be answering.",
            "I cannot answer that for you, that is something you need to answer yourself."
        )
     ),

    # Check bot focused statement
    (r"You(?:re|'re|\sare) (.*)",
        (
            "Why do you think I'm %1?",
            "Why do you say that?",
            "What makes you think I'm %1?"
        )
     ),

    # Check bot focused statement
    (r"You (.*)",
        (
            "Let's talk about you not me.",
            "Why do you think that?",
            "Why do you feel that way?"
        )
     ),

    # Check generic 'how' question
    (r"How (.*)",
        (
            "That is a question you must answer yourself.",
            "Why are you asking that?"
        )
     ),

    # Check apologies
    (r"(?:I\sam|I'?m) sorry (.*)",
        (
            "Don't be sorry.",
            "What are you sorry for?",
            "Don't apologize {name}."
        )
     ),

    # Check reasoning
    (r"(?:Be)?cause (.*)",
        (
            "Do you truly feel that is valid reasoning?",
            "Is that the true reason why?"
        )
     ),

    # Check generic question
    (r"Is it (.*)",
        (
            "Do you think it is %1?",
            "Why do you think that?"
        )
     ),

    # Check present or future statements
    (r"I(?:\swould|'?d) (.*)",
        (
            "Why would you %1?",
            "Is that something you would really do?",
            "How would you %1?"
        )
     ),

    # Check future promises
    # Checks for (I will, I'll, I'm gonna, I am gonna, I'm going to, and I am going to)
    (r"I(?:\swill|'?ll|'?m\sgonna|\sam\sgonna|'?m\sgoing\sto|\sam\sgoing\to) (.*)",
        (
            "When are you going to %1?",
            "How are you going to %1?"
        )
     ),

    # Check statement
    (r"(?:It\sis|It's) (.*)",
     (
         "Why do you think it is %1?",
         "Is it really?"
     )
     ),

    # Check bot focused statement
    (r"Are you (.*)",
     (
         "Why are you asking that?",
         "Does it matter if I am %1?",
         "Do you believe I am?"
     )
     ),

    # Check targeted question
    (r"What is (.*)",
        (
            "What do you think %1 is?",
            "Why are you asking %1?"
        )
     ),

    # Check generic question
    (r"What (.*)",
        (
            "What do you think?",
            "What are your thoughts about that?"
        )
     ),

    # Check necessities
    (r"I need (.*)",
        (
            "Why is it that you need %1?",
            "Do you really need %1?",
            "How would it benefit you to have %1?",
            "What is stopping you from getting %1?"
        )
     ),

    # Check desires
    (r"I (?:want|wanna) (.*)",
        (
            "Why is it that you want %1?",
            "Why do you want %1?"
        )
     ),

    # Check positive statement
    (r"I love (.*)",
        (
            "Tell me why you love %1.",
            "Why do you love %1?"
        )
     ),

    # Check negative statement
    (r"I hate (.*)",
        (
            "Tell me why you hate %1.",
            "Why do you hate %1?"
        )
     ),

    # Check family related statement
    (r"(?:.*) (family|husband|wife|father|mother|brother|sister|daughter|son|child|grandmother|grandfather|grandpa|grandma|mom|dad)",
     (
         "Tell me more about your %1?",
         "How is your relationship with your %1?",
         "Do you think your relationship with your %1 affected you in anyway?"
     )
     ),

    # Check school statement
    (r"(?:.*) (school)",
     (
         "Can you expand on how school makes you feel?",
         "Does school stress you out?",
     )
     ),

    # Check friendship related statement
    (r"(?:.*) (friends?)",
     (
         "How is your relationship with your %1?",
         "Do you like your %1?"
     )
     ),

    # Check opinionated statement
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

    # Check feeling statement
    (r"(?:I|I'?m) feel(?:ing)? (.*)",
        (
            "Why do you feel %1?",
            "What caused you to feel that way?",
            "Do you feel like that often?",
            "How you deal with feeling like that?"
        )
     ),

    # Check self describing statement
    (r"(?:I'?m|I am) (.*)",
        (
            "Why are you %1?",
            "Tell me more about why you are %1."
        )
     ),

    # Check unsure answer
    (r"I don(?:'?t) know",
        (
            "Why do you think you don't know?",
            "Can you elborate what you don't know?",
            "How does it make you feel not knowing?",
        )
     ),

    # Check generic self question
    (r"Can I (.*)",
     (
         "Is there a reason you cannot $1?",
         "What is stopping you from doing that?"
     )
     ),

    # Check generic question
    (r"Why (.*)",
     (
         "What is your thoughts on that?",
         "Why do you think so?"
     )
     ),

    # Check for exit key word
    (r"(?:Good)?bye(.*)",
        (
            "Goodbye {name}.",
            "See you next time {name}.",
            "Have a nice day {name}."
        )
     ),

    # Check for school related response
    (r"(?:.*) (homework|assignments?|projects?|work)",
     (
         "Have you been keeping up with your %1?",
         "Is your %1 easy or difficult?"
     )
     ),

    # Check for any positive associations
    (r"(?:.*)(good|great|excellent|exceptional|marvelous|satisfying|superb|wonderful|nice|awesome|amazing)",
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

    # Check generic negative response
    (r"(?:No|Nah|Nope)(.*)",
        (
            "Can you elborate why you said no?",
            "Why not?"
        )
     ),

    # Check generic positive response
    (r"(?:Yes|Yeah|Yea|Yep|Of\scourse)(.*)",
        (
            "Can you elborate why you said yes?",
            "Why?"
        )
     ),

    # Default to this
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

    # Get only words with capital letters
    r = re.compile('[A-Z]')
    
    # Introduce bot
    print(f"{eliza} Hello my name is Eliza and I'm a psychotheraphist bot.")
    print(f"{eliza} Whenever you feel tired of the conversation, please say 'Goodbye'.")
    print(f"{eliza} What is your name? (Name needs to be captial)")

    # NAME HAS TO BE CAPTIAL

    # Split user's response into list of strings
    while True:
        intro = input("USER> ")
        if any(letter.isupper() for letter in intro):
            break
        print("Please capitalize your name")

    intro = intro.split(' ')

    # Typically the name is the last capital word in an introduction
    name = remove_punctuation(list(filter(r.match, intro))[-1])


# Parse through possible responses and generate a response
def parse_answer(query):
    # Remove ending punctuation
    query = remove_punctuation(query)

    # Compile exiting statement
    goodbye = re.compile(r'(?:good)?bye', re.I)

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


# Start program and run main loop
if __name__ == '__main__':
    main()
