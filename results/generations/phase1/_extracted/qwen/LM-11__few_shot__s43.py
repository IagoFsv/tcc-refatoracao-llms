"""Drawing of the gallows in a hangman game, according to the number of misses.

Public entry point: run(misses). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

def print_hangman(guessCount):
    gallows = [
        ('_________', '|       |', '|', '|', '|', '|', '|', '|'),
        ('_________', '|       |', '|       O', '|', '|', '|', '|', '|'),
        ('_________', '|       |', '|       O', '|       |', '|', '|', '|'),
        ('_________', '|       |', '|       O', '|      /|', '|', '|', '|', '|'),
        ('_________', '|       |', '|       O', '|      /|\\', '|', '|', '|', '|'),
        ('_________', '|       |', '|       O', '|      /|\\', '|      /', '|', '|', '|'),
        ('_________', '|       |', '|       O', '|      /|\\', '|      / \\', '|', '|', '|')
    ]
    print(gallows[guessCount])


def run(misses):
    """Prints the gallows for the number of misses. Public entry point of this unit."""
    return print_hangman(misses)
