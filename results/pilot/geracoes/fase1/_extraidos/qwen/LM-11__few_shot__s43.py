def print_hangman(guessCount):
    figures = [
        '_________\n|       |\n|',
        '_________\n|       |\n|       O',
        '_________\n|       |\n|       O\n|       |',
        '_________\n|       |\n|       O\n|      /|',
        '_________\n|       |\n|       O\n|      /|\\',
        '_________\n|       |\n|       O\n|      /|\\n|      /',
        '_________\n|       |\n|       O\n|      /|\\n|      / \\'
    ]
    print(figures[guessCount])

def executar(erros):
    """Imprime a forca para o numero de erros. Ponto de entrada publico desta unidade."""
    print_hangman(erros)
