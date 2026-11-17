"""Drawing of the gallows in a hangman game, according to the number of misses.

Public entry point: run(misses). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""


def print_head():
    print('_________')
    print('|       |')

def print_body():
    print('|')

def print_arm1():
    print('|       O')

def print_arm2():
    print('|       O')
    print('|       |')

def print_leg1():
    print('|      /|')

def print_leg2():
    print('|      /|\\')

def print_hangman(guessCount):
    if guessCount == 0:
        print_head()
        print_body()
        print_body()
        print_body()
        print_body()
        print_body()
    elif guessCount == 1:
        print_head()
        print_body()
        print_arm1()
        print_body()
        print_body()
        print_body()
        print_body()
    elif guessCount == 2:
        print_head()
        print_arm1()
        print_body()
        print_body()
        print_body()
        print_body()
    elif guessCount == 3:
        print_head()
        print_arm1()
        print_arm2()
        print_body()
        print_body()
    elif guessCount == 4:
        print_head()
        print_arm1()
        print_arm2()
        print_leg1()
        print_body()
    elif guessCount == 5:
        print_head()
        print_arm1()
        print_arm2()
        print_leg1()
        print_leg2()
    elif guessCount == 6:
        print_head()
        print_arm1()
        print_arm2()
        print_leg1()
        print_leg2()

def run(misses):
    """Prints the gallows for the number of misses. Public entry point of this unit."""
    return print_hangman(misses)
