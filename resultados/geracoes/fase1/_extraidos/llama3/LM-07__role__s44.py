"""Gerador de listas de senhas aleatorias, pelo console.

Ponto de entrada publico: executar(). Nao altere o nome nem a assinatura
dessa funcao; o restante do arquivo pode ser reorganizado livremente.
"""

import random
import string
import sys
import os

def main():
    print("Welcome to the password generator!")
    print("")
    
    while True:
        try:
            length = int(input("Enter the length of the password: "))
            break
        except ValueError:
            print("Please enter a valid number.")
            
    options = {
        'special': False,
        'uppercase': False,
        'lowercase': False,
        'numbers': False,
        'symbols': False,
        'text': False
    }
    
    for option, default in options.items():
        while True:
            answer = input(f"Do you want to include {option.capitalize()} characters in the password? (y/n): ")
            if answer == 'y':
                options[option] = True
                break
            elif answer == 'n':
                break
            else:
                print("Please enter a valid answer.")
                
    passwords = generate_passwords(length, options)
    print("")
    print("Here are the generated passwords:")
    for password in passwords:
        print(password)
    print("")
    
    if options['text']:
        print("")
        path = input("Enter the path to the folder where you want to store the text file: ")
        if os.path.exists(path):
            with open(path + "/passwords.txt", "w") as file:
                for password in passwords:
                    file.write(password + "\n")
            print("")
            print("The passwords have been stored in the text file.")
        else:
            print("Please enter a valid path.")
    
    while True:
        answer = input("Do you want to generate more passwords? (y/n): ")
        if answer == 'y':
            main()
        elif answer == 'n':
            print("")
            print("Goodbye.")
            sys.exit()
        else:
            print("Please enter a valid answer.")
            print("")

def generate_passwords(length, options):
    passwords = []
    if options['special']:
        passwords.extend(generate_passwords_from_set(string.punctuation, length))
    if options['uppercase']:
        passwords.extend(generate_passwords_from_set(string.ascii_uppercase, length))
    if options['lowercase']:
        passwords.extend(generate_passwords_from_set(string.ascii_lowercase, length))
    if options['numbers']:
        passwords.extend(generate_passwords_from_set(string.digits, length))
    if options['symbols']:
        passwords.extend(generate_passwords_from_set(string.punctuation, length))
    return passwords

def generate_passwords_from_set(char_set, length):
    passwords = []
    for _ in range(length):
        password = ''.join(random.choice(char_set) for _ in range(length))
        passwords.append(password)
    return passwords

def executar():
    """Roda o gerador interativo. Ponto de entrada publico desta unidade."""
    return main()

if __name__ == '__main__':
    executar()
