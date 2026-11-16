def print_hangman_head():
    print('_________')
    print('|       |')
    print('|       O')
    print('|')

def print_hangman_body():
    print('|       |')
    print('|      /|\\')
    print('|')

def print_hangman_legs():
    print('|      / \\')
    print('|')

def print_hangman(guessCount):
    print('_________')
    print('|       |')
    if guessCount >= 1:
        print_hangman_head()
    if guessCount >= 2:
        print_hangman_body()
    if guessCount >= 3:
        print_hangman_legs()

def executar(erros):
    """Imprime a forca para o numero de erros. Ponto de entrada publico desta unidade."""
    return print_hangman(erros)
