def _imprimir_forca(guessCount):
    forca = [
        '_________',
        '|       |',
        '|       O' if guessCount > 0 else '|',
        '|      /|' if guessCount > 1 else '|',
        '|      /|\\' if guessCount > 2 else '|',
        '|      /' if guessCount > 3 else '|',
        '|      / \\' if guessCount > 4 else '|',
        '|'
    ]
    print('\n'.join(forca))


def executar(erros):
    """Imprime a forca para o numero de erros. Ponto de entrada publico desta unidade."""
    _imprimir_forca(erros)
