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
    
    options = {
        "special": False,
        "uppercase": False,
        "lowercase": False,
        "numbers": False,
        "symbols": False,
        "text": False,
    }
    
    for option, default in options.items():
        while True:
            answer = input(f"Do you want to include {option.capitalize()} in the password? (y/n): ")
            if answer == 'y':
                options[option] = True
                break
            elif answer == 'n':
                break
            else:
                print("Please enter a valid answer.")
    
    length = int(input("Enter the length of the password: "))
    path = input("Enter the path to the folder where you want to store the text file: ")
    
    if os.path.exists(path):
        text = True
    else:
        print("Please enter a valid path.")
    
    passwords = []
    for _ in range(length):
        password = ''
        for _ in range(length):
            if options["special"]:
                password += random.choice(string.punctuation)
            if options["uppercase"]:
                password += random.choice(string.ascii_uppercase)
            if options["lowercase"]:
                password += random.choice(string.ascii_lowercase)
            if options["numbers"]:
                password += random.choice(string.digits)
            if options["symbols"]:
                password += random.choice(string.punctuation)
        passwords.append(password)
    
    print("") 
    print("Here are the generated passwords:") 
    for password in passwords: 
        print(password) 
    print("") 
    
    if text:
        print("") 
        print("Do you want to store the list of passwords in a text file? (y/n): ") 
        while True: 
            answer = input()
            if answer == 'y':
                break
            elif answer == 'n':
                break
            else:
                print("Please enter a valid answer.")
        print("")
        with open(path + "/passwords.txt", "w") as file:       
            for password in passwords:       
                file.write(password + "\n")       
        print("")       
        print("The passwords have been stored in the text file.")
    
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


def executar():
    """Roda o gerador interativo. Ponto de entrada publico desta unidade."""
    return main()


if __name__ == '__main__':
    executar()
