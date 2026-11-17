"""Drawing of the gallows in a hangman game, according to the number of misses.

Public entry point: run(misses). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

def print_base():
    print('_________')
    print('|       |')

def print_head():
    print('|       O')

def print_body():
    print('|')

def print_left_arm():
    print('|       |')

def print_right_arm():
    print('|      /|')

def print_left_leg():
    print('|      /')

def print_right_leg():
    print('|      / \\')

def print_hangman(guessCount):
    print_base()
    if guessCount >= 1:
        print_head()
    if guessCount >= 2:
        print_body()
    if guessCount >= 3:
        print_left_arm()
    if guessCount >= 4:
        print_right_arm()
    if guessCount >= 5:
        print_left_leg()
    if guessCount >= 6:
        print_right_leg()

def run(misses):
    """Prints the gallows for the number of misses. Public entry point of this unit."""
    return print_hangman(misses)
