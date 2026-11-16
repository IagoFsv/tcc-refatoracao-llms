"""Desenho da forca do jogo da forca, conforme o numero de erros.

Ponto de entrada publico: executar(). Nao altere o nome nem a assinatura
dessa funcao; o restante do arquivo pode ser reorganizado livremente.
"""

def print_hangman(guessCount):
    if guessCount == 0:
        print_hangman_zero()
    elif guessCount == 1:
        print_hangman_first()
    elif guessCount == 2:
        print_hangman_second()
    elif guessCount == 3:
        print_hangman_third()
    elif guessCount == 4:
        print_hangman_fourth()
    elif guessCount == 5:
        print_hangman_fifth()
    elif guessCount == 6:
        print_hangman_sixth()

def print_hangman_zero():
    print('_________')
    print('|       |  ')
    print('|       ')
    print('|')
    print('|')
    print('|')
    print('|')
    print('|')

def print_hangman_first():
    print('_________')
    print('|       |  ')
    print('|       O')
    print('|')
    print('|')
    print('|')
    print('|')
    print('|')

def print_hangman_second():
    print('_________')
    print('|       |  ')
    print('|       O')
    print('|       |  ')
    print('|')
    print('|')
    print('|')
    print('|')

def print_hangman_third():
    print('_________')
    print('|       |  ')
    print('|       O')
    print('|       /|  ')
    print('|')
    print('|')
    print('|')
    print('|')

def print_hangman_fourth():
    print('_________')
    print('|       |  ')
    print('|       O')
    print('|       /|\\ ')
    print('|')
    print('|')
    print('|')
    print('|')

def print_hangman_fifth():
    print('_________')
    print('|       |  ')
    print('|       O')
    print('|       /|\\ ')
    print('|       / ')
    print('|')
    print('|')
    print('|')

def print_hangman_sixth():
    print('_________')
    print('|       |  ')
    print('|       O')
    print('|       /|\\ ')
    print('|       / \\ ')
    print('|')
    print('|')
    print('|')


def executar(erros):
    """Imprime a forca para o numero de erros. Ponto de entrada publico desta unidade."""
    return print_hangman(erros)
