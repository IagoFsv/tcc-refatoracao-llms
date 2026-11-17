"""Drawing of the gallows in a hangman game, according to the number of misses.

Public entry point: run(misses). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

def _print_hangman_base():
    print('_________')
    print('|       |')
    print('|')

def _print_hangman_head():
    print('|       O')

def _print_hangman_body():
    print('|')

def _print_hangman_left_arm():
    print('|      /|')

def _print_hangman_right_arm():
    print('|      /|\\')

def _print_hangman_left_leg():
    print('|      /')

def _print_hangman_right_leg():
    print('|      / \\')

def print_hangman(guessCount):
    _print_hangman_base()
    if guessCount >= 1:
        _print_hangman_head()
    if guessCount >= 2:
        _print_hangman_body()
    if guessCount >= 3:
        _print_hangman_left_arm()
    if guessCount >= 4:
        _print_hangman_right_arm()
    if guessCount >= 5:
        _print_hangman_left_leg()
    if guessCount >= 6:
        _print_hangman_right_leg()


def run(misses):
    """Prints the gallows for the number of misses. Public entry point of this unit."""
    return print_hangman(misses)
