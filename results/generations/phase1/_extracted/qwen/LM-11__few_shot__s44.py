"""Drawing of the gallows in a hangman game, according to the number of misses.

Public entry point: run(misses). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""


def _print_hangman_segment(segment):
    print(segment)


def _print_horizontal_line():
    _print_hangman_segment('_________')


def _print_vertical_line():
    _print_hangman_segment('|')


def _print_head():
    _print_hangman_segment('|       O')


def _print_left_arm():
    _print_hangman_segment('|      /|')


def _print_right_arm():
    _print_hangman_segment('|      / \\')


def _print_body():
    _print_hangman_segment('|')


def _print_left_leg():
    _print_hangman_segment('|      /')


def _print_right_leg():
    _print_hangman_segment('|')


def _print_hangman(guessCount):
    _print_horizontal_line()
    _print_vertical_line()
    _print_vertical_line()
    _print_vertical_line()
    _print_vertical_line()
    _print_vertical_line()
    _print_vertical_line()
    _print_vertical_line()

    if guessCount == 1:
        _print_head()
    elif guessCount == 2:
        _print_head()
        _print_left_arm()
    elif guessCount == 3:
        _print_head()
        _print_left_arm()
        _print_right_arm()
    elif guessCount == 4:
        _print_head()
        _print_left_arm()
        _print_right_arm()
        _print_body()
    elif guessCount == 5:
        _print_head()
        _print_left_arm()
        _print_right_arm()
        _print_body()
        _print_left_leg()
    elif guessCount == 6:
        _print_head()
        _print_left_arm()
        _print_right_arm()
        _print_body()
        _print_left_leg()
        _print_right_leg()


def run(misses):
    """Prints the gallows for the number of misses. Public entry point of this unit."""
    _print_hangman(misses)
