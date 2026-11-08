def print_head():
    print('_________')
    print('|       |')

def print_body(guessCount):
    if guessCount == 0:
        print('|')
    elif guessCount == 1:
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
    print_head()
    print('|       |')
    print_body(guessCount)
    print('|')
    print('|')
    print('|')
    print('|')

def executar(erros):
    """Imprime a forca para o numero de erros. Ponto de entrada publico desta unidade."""
    return print_hangman(erros)
