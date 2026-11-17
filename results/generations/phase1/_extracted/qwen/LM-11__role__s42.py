"""Drawing of the gallows in a hangman game, according to the number of misses.

Public entry point: run(misses). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

def print_hangman_part(misses, part):
    print('_________')
    print('|       |')
    print(f'|       {"O" if misses >= 1 else ""}')
    print(f'|      /{"|\\ " if misses >= 2 else ""}')
    print(f'|      /{" " if misses == 3 else "\\ "}')
    print('|')
    print('|')
    print('|')

def print_hangman(misses):
    """Prints the gallows for the number of misses. Public entry point of this unit."""
    if misses == 0:
        print_hangman_part(misses, 0)
    elif misses == 1:
        print_hangman_part(misses, 1)
    elif misses == 2:
        print_hangman_part(misses, 2)
    elif misses == 3:
        print_hangman_part(misses, 3)
    elif misses == 4:
        print_hangman_part(misses, 4)
    elif misses == 5:
        print_hangman_part(misses, 5)
    elif misses == 6:
        print_hangman_part(misses, 6)


def run(misses):
    """Prints the gallows for the number of misses. Public entry point of this unit."""
    return print_hangman(misses)
