"""Drawing of the gallows in a hangman game, according to the number of misses.

Public entry point: run(misses). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""


def print_hangman_head():
    print('_________')
    print('|       |')

def print_hangman_body(misses):
    if misses == 1:
        print('|       O')
    elif misses == 2:
        print('|       O')
        print('|       |')
    elif misses == 3:
        print('|       O')
        print('|      /|')
    elif misses == 4:
        print('|       O')
        print('|      /|\\')
    elif misses == 5:
        print('|       O')
        print('|      /|\\')
        print('|      /')

def print_hangman_foot():
    print('|      / \\')
    print('|')

def print_hangman(guessCount):
    if guessCount == 0:
        print_hangman_head()
        print_hangman_body(0)
        print_hangman_foot()
    elif guessCount == 1:
        print_hangman_head()
        print_hangman_body(1)
        print_hangman_foot()
    elif guessCount == 2:
        print_hangman_head()
        print_hangman_body(2)
        print_hangman_foot()
    elif guessCount == 3:
        print_hangman_head()
        print_hangman_body(3)
        print_hangman_foot()
    elif guessCount == 4:
        print_hangman_head()
        print_hangman_body(4)
        print_hangman_foot()
    elif guessCount == 5:
        print_hangman_head()
        print_hangman_body(5)
        print_hangman_foot()
    elif guessCount == 6:
        print_hangman_head()
        print_hangman_body(6)
        print_hangman_foot()

def run(misses):
    """Prints the gallows for the number of misses. Public entry point of this unit."""
    return print_hangman(misses)
