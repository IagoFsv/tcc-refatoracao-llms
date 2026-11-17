"""Drawing of the gallows in a hangman game, according to the number of misses.

Public entry point: run(misses). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""


def print_hangman_head(guessCount):
    if guessCount == 0:
        return '_________'
    elif guessCount == 1:
        return '_________'
    elif guessCount == 2:
        return '_________'
    elif guessCount == 3:
        return '_________'
    elif guessCount == 4:
        return '_________'
    elif guessCount == 5:
        return '_________'
    elif guessCount == 6:
        return '_________'
    else:
        raise ValueError("Invalid guessCount")


def print_hangman_body(guessCount):
    if guessCount == 0:
        return '\n|       |\n|'
    elif guessCount == 1:
        return '\n|       |' + '\n|       O'
    elif guessCount == 2:
        return '\n|       |' + '\n|       O' + '\n|'
    elif guessCount == 3:
        return '\n|       |' + '\n|       O' + '\n|       |'
    elif guessCount == 4:
        return '\n|       |' + '\n|       O' + '\n|      /|'
    elif guessCount == 5:
        return '\n|       |' + '\n|       O' + '\n|      /|\\'
    elif guessCount == 6:
        return '\n|       |' + '\n|       O' + '\n|      /|\\' + '\n|      /'
    else:
        raise ValueError("Invalid guessCount")


def print_hangman_foot(guessCount):
    if guessCount == 0:
        return '\n|' + '\n|'
    elif guessCount == 1:
        return '\n|' + '\n|'
    elif guessCount == 2:
        return '\n|' + '\n|'
    elif guessCount == 3:
        return '\n|' + '\n|'
    elif guessCount == 4:
        return '\n|' + '\n|'
    elif guessCount == 5:
        return '\n|' + '\n|'
    elif guessCount == 6:
        return '\n|      / \\'
    else:
        raise ValueError("Invalid guessCount")


def print_hangman(guessCount):
    print(print_hangman_head(guessCount))
    print(print_hangman_body(guessCount))
    print(print_hangman_foot(guessCount))


def run(misses):
    """Prints the gallows for the number of misses. Public entry point of this unit."""
    return print_hangman(misses)
