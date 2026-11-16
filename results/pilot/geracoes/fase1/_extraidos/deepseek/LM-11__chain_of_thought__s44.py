def print_hangman(guessCount):
    if guessCount == 0:
        print_hangman_body()
        print('|')
        print('|')
        print('|')
        print('|')
        print('|')
        print('|')
        print('|')
    elif guessCount == 1:
        print_hangman_body()
        print('|       O')
        print('|')
        print('|')
        print('|')
        print('|')
        print('|')
    elif guessCount == 2:
        print_hangman_body()
        print('|       O')
        print('|       |  ')
        print('|')
        print('|')
        print('|')
        print('|')
    elif guessCount == 3:
        print_hangman_body()
        print('|       O')
        print('|       /|')
        print('|')
        print('|')
        print('|')
        print('|')
    elif guessCount == 4:
        print_hangman_body()
        print('|       O')
        print('|       /|\\')
        print('|')
        print('|')
        print('|')
        print('|')
    elif guessCount == 5:
        print_hangman_body()
        print('|       O')
        print('|       /|\\')
        print('|       /  ')
        print('|')
        print('|')
        print('|')
    elif guessCount == 6:
        print_hangman_body()
        print('|       O')
        print('|       /|\\')
        print('|       / \\')
        print('|')
        print('|')
        print('|')

def print_hangman_body(guessCount):
    print('_________')
    print('|       |  ')

def executar(erros):
    """Imprime a forca para o numero de erros. Ponto de entrada publico desta unidade."""
    return print_hangman(erros)
