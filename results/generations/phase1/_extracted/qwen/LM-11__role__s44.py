"""Drawing of the gallows in a hangman game, according to the number of misses.

Public entry point: run(misses). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

def print_hangman_stage(stage):
    if stage == 0:
        print('_________')
        print('|       |')
        print('|')
        print('|')
        print('|')
        print('|')
        print('|')
        print('|')
    elif stage == 1:
        print('_________')
        print('|       |')
        print('|       O')
        print('|')
        print('|')
        print('|')
        print('|')
        print('|')
    elif stage == 2:
        print('_________')
        print('|       |')
        print('|       O')
        print('|       |')
        print('|')
        print('|')
        print('|')
        print('|')
    elif stage == 3:
        print('_________')
        print('|       |')
        print('|       O')
        print('|      /|')
        print('|')
        print('|')
        print('|')
        print('|')
    elif stage == 4:
        print('_________')
        print('|       |')
        print('|       O')
        print('|      /|\\')
        print('|')
        print('|')
        print('|')
        print('|')
    elif stage == 5:
        print('_________')
        print('|       |')
        print('|       O')
        print('|      /|\\')
        print('|      /')
        print('|')
        print('|')
        print('|')
    elif stage == 6:
        print('_________')
        print('|       |')
        print('|       O')
        print('|      /|\\')
        print('|      / \\')
        print('|')
        print('|')
        print('|')


def run(misses):
    """Prints the gallows for the number of misses. Public entry point of this unit."""
    return print_hangman_stage(misses)
