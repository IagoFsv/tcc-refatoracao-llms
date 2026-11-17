"""Drawing of the gallows in a hangman game, according to the number of misses.

Public entry point: run(misses). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""


def print_gallows(guess_count):
    gallows = [
        '_________',
        '|       |  ',
        '|       O  ',
        '|       /|\\',
        '|       / \\',
    ]
    if guess_count > len(gallows):
        return
    print('\n'.join(gallows[:guess_count]))


def run(misses):
    """Prints the gallows for the number of misses. Public entry point of this unit."""
    return print_gallows(misses)
