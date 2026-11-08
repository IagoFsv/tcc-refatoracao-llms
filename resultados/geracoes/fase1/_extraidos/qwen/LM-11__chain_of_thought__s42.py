def print_hangman_0():
    print('_________')
    print('|       |')
    print('|')
    print('|')
    print('|')
    print('|')
    print('|')
    print('|')

def print_hangman_1():
    print('_________')
    print('|       |')
    print('|       O')
    print('|')
    print('|')
    print('|')
    print('|')
    print('|')

def print_hangman_2():
    print('_________')
    print('|       |')
    print('|       O')
    print('|       |')
    print('|')
    print('|')
    print('|')
    print('|')

def print_hangman_3():
    print('_________')
    print('|       |')
    print('|       O')
    print('|      /|')
    print('|')
    print('|')
    print('|')
    print('|')

def print_hangman_4():
    print('_________')
    print('|       |')
    print('|       O')
    print('|      /|\\')
    print('|')
    print('|')
    print('|')
    print('|')

def print_hangman_5():
    print('_________')
    print('|       |')
    print('|       O')
    print('|      /|\\')
    print('|      /')
    print('|')
    print('|')
    print('|')

def print_hangman_6():
    print('_________')
    print('|       |')
    print('|       O')
    print('|      /|\\')
    print('|      / \\')
    print('|')
    print('|')
    print('|')

def print_hangman(guessCount):
    hangman_functions = {
        0: print_hangman_0,
        1: print_hangman_1,
        2: print_hangman_2,
        3: print_hangman_3,
        4: print_hangman_4,
        5: print_hangman_5,
        6: print_hangman_6
    }
    
    hangman_functions.get(guessCount, lambda: print('Estado da forca inválido'))()

def executar(erros):
    """Imprime a forca para o numero de erros. Ponto de entrada publico desta unidade."""
    print_hangman(erros)
