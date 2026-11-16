def print_head(guessCount):
    print('_________')
    print('|       |')

def print_body(guessCount):
    if guessCount == 1:
        print('|       O')
    elif guessCount == 2:
        print('|       O')
        print('|       |')
    elif guessCount == 3:
        print('|       O')
        print('|      /|')
    elif guessCount == 4:
        print('|       O')
        print('|      /|\\')
    elif guessCount == 5:
        print('|       O')
        print('|      /|\\')
        print('|      /')
    elif guessCount == 6:
        print('|       O')
        print('|      /|\\')
        print('|      / \\')

def print_hangman(guessCount):
    print_head(guessCount)
    print_body(guessCount)
    print('|')
    print('|')
    print('|')
    print('|')
    print('|')
    print('|')

def executar(erros):
    return print_hangman(erros)
