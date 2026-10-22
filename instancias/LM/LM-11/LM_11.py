"""Desenho da forca do jogo da forca, conforme o numero de erros.

Ponto de entrada publico: executar(). Nao altere o nome nem a assinatura
dessa funcao; o restante do arquivo pode ser reorganizado livremente.
"""


def print_hangman(guessCount):
    if guessCount == 0:
        print('_________')
        print('|       |')
        print('|')
        print('|')
        print('|')
        print('|')
        print('|')
        print('|')
    elif guessCount == 1:
        print('_________')
        print('|       |')
        print('|       O')
        print('|')
        print('|')
        print('|')
        print('|')
        print('|')
    elif guessCount == 2:
        print('_________')
        print('|       |')
        print('|       O')
        print('|       |')
        print('|')
        print('|')
        print('|')
        print('|')
    elif guessCount == 3:
        print('_________')
        print('|       |')
        print('|       O')
        print('|      /|')
        print('|')
        print('|')
        print('|')
        print('|')
    elif guessCount == 4:
        print('_________')
        print('|       |')
        print('|       O')
        print('|      /|\\')
        print('|')
        print('|')
        print('|')
        print('|')
    elif guessCount == 5:
        print('_________')
        print('|       |')
        print('|       O')
        print('|      /|\\')
        print('|      /')
        print('|')
        print('|')
        print('|')
    elif guessCount == 6:
        print('_________')
        print('|       |')
        print('|       O')
        print('|      /|\\')
        print('|      / \\')
        print('|')
        print('|')
        print('|')


def executar(erros):
    """Imprime a forca para o numero de erros. Ponto de entrada publico desta unidade."""
    return print_hangman(erros)
