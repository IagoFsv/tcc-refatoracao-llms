"""Drawing of the gallows in a hangman game, according to the number of misses.

Public entry point: run(misses). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

def print_hangman(guessCount):
    if guessCount == 0:
        print('_________')
        print('|       |')
        print('|')
        print('|')
        print('|')
        print('|')
        print('|')
        print('|')
    elif guessCount == 1:
        print_hangman_base()
        print_hangman_head()
    elif guessCount == 2:
        print_hangman_base()
        print_hangman_head()
        print_hangman_body()
    elif guessCount == 3:
        print_hangman_base()
        print_hangman_head()
        print_hangman_body()
        print_hangman_arm_left()
    elif guessCount == 4:
        print_hangman_base()
        print_hangman_head()
        print_hangman_body()
        print_hangman_arm_left()
        print_hangman_arm_right()
    elif guessCount == 5:
        print_hangman_base()
        print_hangman_head()
        print_hangman_body()
        print_hangman_arm_left()
        print_hangman_arm_right()
        print_hangman_leg_left()
    elif guessCount == 6:
        print_hangman_base()
        print_hangman_head()
        print_hangman_body()
        print_hangman_arm_left()
        print_hangman_arm_right()
        print_hangman_leg_left()
        print_hangman_leg_right()


def print_hangman_base():
    print('_________')


def print_hangman_head():
    print('|       |')
    print('|       O')


def print_hangman_body():
    print('|       |')


def print_hangman_arm_left():
    print('|      /|')


def print_hangman_arm_right():
    print('|      / \\')


def print_hangman_leg_left():
    print('|      /')


def print_hangman_leg_right():
    print('|')


def run(misses):
    """Prints the gallows for the number of misses. Public entry point of this unit."""
    return print_hangman(misses)
