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
        "special": False,
        "uppercase": False,
        "lowercase": False,
        "numbers": False,
        "symbols": False,
        "text": False
    }

    while True:
        answer = input("Do you want to include special characters in the password? (y/n): ")
        if answer == 'y':
            options["special"] = True
            break
        elif answer == 'n':
            break
        else:
            print("Please enter a valid answer.")
            
    while True:
        answer = input("Do you want to include uppercase letters in the password? (y/n): ")
        if answer == 'y':
            options["uppercase"] = True
            break
        elif answer == 'n':
            break
        else:
            print("Please enter a valid answer.")
            
    while True:
        answer = input("Do you want to include lowercase letters in the password? (y/n): ")
        if answer == 'y':
            options["lowercase"] = True
            break
        elif answer == 'n':
            break
        else:
            print("Please enter a valid answer.")
            
    while True:
        answer = input("Do you want to include numbers in the password? (y/n): ")
        if answer == 'y':
            options["numbers"] = True
            break
        elif answer == 'n':
            break
        else:
            print("Please enter a valid answer.")
            
    while True:
        answer = input("Do you want to include symbols in the password? (y/n): ")
        if answer == 'y':
            options["symbols"] = True
            break
        elif answer == 'n':
            break
        else:
            print("Please enter a valid answer.")
            
    while True:
        answer = input("Do you want to store the list of passwords in a text file? (y/n): ")
        if answer == 'y':
            options["text"] = True
            break
        elif answer == 'n':
            break
        else:
            print("Please enter a valid answer.")
            
    while True:
        try:
            path = input("Enter the path to the folder where you want to store the text file: ")
            if os.path.exists(path):
                break
            else:
                print("Please enter a valid path.")
        except ValueError:
            print("Please enter a valid path.")
            
    passwords = []
    if options["special"]:
        passwords += generate_password(length, string.punctuation)
    if options["uppercase"]:
        passwords += generate_password(length, string.ascii_uppercase)
    if options["lowercase"]:
        passwords += generate_password(length, string.ascii_lowercase)
    if options["numbers"]:
        passwords += generate_password(length, string.digits)
    if options["symbols"]:
        passwords += generate_password(length, string.punctuation)
        
    print("")
    print("Here are the generated passwords:")
    for password in passwords:
        print(password)
    print("")
        
    if options["text"]:
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
        while True:
            try:
                path = input("Enter the path to the folder where you want to store the text file: ")
                if os.path.exists(path):
                    break
                else:
                    print("Please enter a valid path.")
            except ValueError:
                print("Please enter a valid path.")
        print("")
        with open(path + "/passwords.txt", "w") as file:
            for password in passwords:
                file.write(password + "\n")
        print("")
        print("The passwords have been stored in the text file.")
    print("")
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
            
def generate_password(length, chars):
    return [random.choice(chars) * length for _ in range(1)]

def executar():
    """Roda o gerador interativo. Ponto de entrada publico desta unidade."""
    return main()

if __name__ == '__main__':
    executar()
