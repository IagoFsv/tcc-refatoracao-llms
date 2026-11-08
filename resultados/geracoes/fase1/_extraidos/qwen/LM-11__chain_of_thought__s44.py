def print_hangman(guessCount):
    print_base()
    print_head(guessCount)
    print_body(guessCount)
    print_rope(guessCount)
    print_arms(guessCount)
    print_legs(guessCount)

def print_base():
    print('_________')

def print_head(guessCount):
    if guessCount >= 1:
        print('|       O')

def print_body(guessCount):
    if guessCount >= 2:
        print('|       |')

def print_rope(guessCount):
    if guessCount >= 3:
        print('|      /|')

def print_arms(guessCount):
    if guessCount >= 4:
        print('|      /|\\')

def print_legs(guessCount):
    if guessCount >= 5:
        print('|      / \\')

def executar(erros):
    """Imprime a forca para o numero de erros. Ponto de entrada publico desta unidade."""
    return print_hangman(erros)
