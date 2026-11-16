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
            
    options = []
    while True:
        answer = input("Do you want to include {} in the password? (y/n): ".format(', '.join(['special characters', 'uppercase letters', 'lowercase letters', 'numbers', 'symbols'])))
        if answer == 'y':
            options.append('special characters')
            break
        elif answer == 'n':
            break
        else:
            print("Please enter a valid answer.")
        
    if options:
        options = [option for option in options if option != 'special characters']
        special = True
    else:
        special = False
    
    if options:
        options = [option for option in options if option != 'uppercase letters']
        uppercase = True
    else:
        uppercase = False
    
    if options:
        options = [option for option in options if option != 'lowercase letters']
        lowercase = True
    else:
        lowercase = False
    
    if options:
        options = [option for option in options if option != 'numbers']
        numbers = True
    else:
        numbers = False
    
    if options:
        options = [option for option in options if option != 'symbols']
        symbols = True
    else:
        symbols = False
    
    text = input("Do you want to store the list of passwords in a text file? (y/n): ")
    if text == 'y':
        text = True
    else:
        text = False
    
    if text:
        path = input("Enter the path to the folder where you want to store the text file: ")
        if os.path.exists(path):
            with open(path + "/passwords.txt", "w") as file:
                for _ in range(length):
                    password = ''
                    if special:
                        password += random.choice(string.punctuation)
                    if uppercase:
                        password += random.choice(string.ascii_uppercase)
                    if lowercase:
                        password += random.choice(string.ascii_lowercase)
                    if numbers:
                        password += random.choice(string.digits)
                    if symbols:
                        password += random.choice(string.punctuation)
                    while len(password) < length:
                        password += random.choice(string.ascii_letters + string.digits + string.punctuation)
                    file.write(password + "\n")
        else:
            print("Please enter a valid path.")
    
    print("Here are the generated passwords:")
    for _ in range(length):
        password = ''
        if special:
            password += random.choice(string.punctuation)
        if uppercase:
            password += random.choice(string.ascii_uppercase)
        if lowercase:
            password += random.choice(string.ascii_lowercase)
        if numbers:
            password += random.choice(string.digits)
        if symbols:
            password += random.choice(string.punctuation)
        while len(password) < length:
            password += random.choice(string.ascii_letters + string.digits + string.punctuation)
        print(password)
    
    while True:
        answer = input("Do you want to generate more passwords? (y/n): ")
        if answer == 'y':
            main()
        elif answer == 'n':
            print("Goodbye.")
            sys.exit()
        else:
            print("Please enter a valid answer.")
            print("")
