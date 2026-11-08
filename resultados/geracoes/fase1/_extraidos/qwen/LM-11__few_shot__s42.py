def print_hangman(guessCount):
    stages = [
        '_________',
        '_________|       |',
        '_________|       O',
        '_________|      /|',
        '_________|      /|\\',
        '_________|      /|\\',
        '_________|      /|\\',
        '_________|      /|\\'
    ]
    print(stages[guessCount])

def executar(erros):
    """Imprime a forca para o numero de erros. Ponto de entrada publico desta unidade."""
    return print_hangman(erros)
