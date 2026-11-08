"""Desenho da forca do jogo da forca, conforme o numero de erros.

Ponto de entrada publico: executar(). Nao altere o nome nem a assinatura
dessa funcao; o restante do arquivo pode ser reorganizado livremente.
"""


def print_hangman(guessCount):
    if guessCount == 0:
        print_hangman_0()
    elif guessCount == 1:
        print_hangman_1()
    elif guessCount == 2:
        print_hangman_2()
    elif guessCount == 3:
        print_hangman_3()
    elif guessCount == 4:
        print_hangman_4()
    elif guessCount == 5:
        print_hangman_5()
    elif guessCount == 6:
        print_hangman_6()


def print_hangman_0():
    print('_________')
    print('|       |  ')
    print('|       O  ')
    print('|      /|\\ ')
    print('|      / \\ ')
    print('|')
    print('|')
    print('|')
    print('|')


def print_hangman_1():
    print('_________')
    print('|       |  ')
    print('|       O  ')
    print('|')
    print('|')
    print('|')
    print('|')
    print('|')


def print_hangman_2():
    print('_________')
    print('|       |  ')
    print('|       O  ')
    print('|       |  ')
    print('|')
    print('|')
    print('|')
    print('|')


def print_hangman_3():
    print('_________')
    print('|       |  ')
    print('|       O  ')
    print('|      |  ')
    print('|')
    print('|')
    print('|')
    print('|')


def print_hangman_4():
    print('_________')
    print('|       |  ')
    print('|       O  ')
    print('|      |  ')
    print('|')
    print('|')
    print('|')
    print('|')


def print_hangman_5():
    print('_________')
    print('|       |  ')
    print('|       O  ')
    print('|      |  ')
    print('|       /  ')
    print('|')
    print('|')
    print('|')


def print_hangman_6():
    print('_________')
    print('|       |  ')
    print('|       O  ')
    print('|      |  ')
    print('|       / \\ ')
    print('|')
    print('|')
    print('|')


def executar(erros):
    """Imprime a forca para o numero de erros. Ponto de entrada publico desta unidade."""
    return print_hangman(erros)
