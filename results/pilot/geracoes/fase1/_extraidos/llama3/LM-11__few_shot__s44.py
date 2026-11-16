def _print_head():
    print('_________')
    print('|       |')

def _print_body(guessCount):
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

def _print_footer():
    print('|')
    print('|')
    print('|')
    print('|')
    print('|')

def executar(erros):
    """Imprime a forca para o numero de erros. Ponto de entrada publico desta unidade."""
    _print_head()
    _print_body(erros)
    _print_footer()
