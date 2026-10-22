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
    
    # Ask the user for the length of the password
    while True:
        try:
            length = int(input("Enter the length of the password: "))
            break
        except ValueError:
            print("Please enter a valid number.")
            
    # Ask the user if they want to include special characters in the password
    while True:
        answer = input("Do you want to include special characters in the password? (y/n): ")
        if answer == 'y':
            special = True
            break
        elif answer == 'n':
            special = False
            break
        else:
            print("Please enter a valid answer.")
        
    # Ask the user if they want to include uppercase letters in the password
    while True:
        answer = input("Do you want to include uppercase letters in the password? (y/n): ")
        if answer == 'y':
            uppercase = True
            break
        elif answer == 'n':
            break
        else:
            print("Please enter a valid answer.")
        
    # Ask the user if they want to include lowercase letters in the password
    while True:
        answer = input("Do you want to include lowercase letters in the password? (y/n): ")
        if answer == 'y':
            lowercase = True
            break
        elif answer == 'n':
            break
        else:
            print("Please enter a valid answer.")
    
    # Ask the user if they want to include numbers in the password
    while True:
        answer = input("Do you want to include numbers in the password? (y/n): ")
        if answer == 'y':
            numbers = True
            break
        elif answer == 'n':
            break
        else:
            print("Please enter a valid answer.")
        
    # Ask the user if they want to include symbols in the password
    while True:
        answer = input("Do you want to include symbols in the password? (y/n): ")
        if answer == 'y':
            symbols = True
            break
        elif answer == 'n':
            break
        else:
            print("Please enter a valid answer.")
    
    # Ask the user if they want to store the list of passwords in a text file
    while True:
        answer = input("Do you want to store the list of passwords in a text file? (y/n): ")
        if answer == 'y':
            text = True
            break
        elif answer == 'n':
            text = False
            break
        else:
            print("Please enter a valid answer.")
    
    # Ask the user where they want to store the text file
    while True:
        try:
            path = input("Enter the path to the folder where you want to store the text file: ")
            if os.path.exists(path):
                break
            else:
                print("Please enter a valid path.")
        except ValueError:
            print("Please enter a valid path.")
    
    # Generate the list of passwords
    passwords = []
    if special == True:
        for i in range(length):
            password = ''
            for j in range(length):
                password += random.choice(string.punctuation)
            passwords.append(password)
            
    if uppercase == True:
        for i in range(length):
            password = ''
            for j in range(length):
                password += random.choice(string.ascii_uppercase)
            passwords.append(password)
    
    if lowercase == True:
        for i in range(length):
            password = '' 
            for j in range(length): 
                password += random.choice(string.ascii_lowercase) 
            passwords.append(password) 
    
    if numbers == True: 
        for i in range(length): 
            password = '' 
            for j in range(length): 
                password += random.choice(string.digits) 
            passwords.append(password) 
    
    if symbols == True: 
        for i in range(length): 
            password = '' 
            for j in range(length): 
                password += random.choice(string.punctuation) 
            passwords.append(password) 
    
    # Print the list of passwords
    print("") 
    print("Here are the generated passwords:") 
    for password in passwords: 
        print(password) 
    print("") 
    
    # Ask the user if he wants to store the list of passwords in a text file
    if text == True: 
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
        # Ask the user where they want to store the text file
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
        # Write the list of passwords to a text file       
        with open(path + "/passwords.txt", "w") as file:       
            for password in passwords:       
                file.write(password + "\n")       
        print("")       
        print("The passwords have been stored in the text file.")       
    print("")       
    # Ask the user if he wants to generate more passwords       
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
