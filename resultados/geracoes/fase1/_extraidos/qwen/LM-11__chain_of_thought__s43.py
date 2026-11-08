def print_base():
    print('_________')
    print('|       |')

def print_head():
    print('|       O')

def print_body():
    print('|       |')

def print_arm_left():
    print('|      /|')

def print_arm_right():
    print('|      /|\\')

def print_leg_left():
    print('|      /')

def print_leg_right():
    print('|      / \\')

def print_hangman(guessCount):
    print_base()
    if guessCount >= 1:
        print_head()
    if guessCount >= 2:
        print_body()
    if guessCount >= 3:
        print_arm_left()
    if guessCount >= 4:
        print_arm_right()
    if guessCount >= 5:
        print_leg_left()
    if guessCount >= 6:
        print_leg_right()

def executar(erros):
    """Imprime a forca para o numero de erros. Ponto de entrada publico desta unidade."""
    return print_hangman(erros)
