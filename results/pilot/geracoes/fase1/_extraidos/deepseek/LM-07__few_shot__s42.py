"""Gerador de listas de senhas aleatorias, pelo console.

Ponto de entrada publico: executar(). Nao altere o nome nem a assinatura
dessa funcao; o restante do arquivo pode ser reorganizado livremente.
"""

import random
import string
import sys
import os

def _get_user_input(prompt, valid_responses):
    while True:
        answer = input(prompt)
        if answer in valid_responses:
            return answer
        else:
            print("Please enter a valid answer.")

def _generate_passwords(length, special, uppercase, lowercase, numbers, symbols):
    passwords = []
    if special:
        for i in range(length):
            password = ''.join(random.choice(string.punctuation) for _ in range(length))
            passwords.append(password)
            
    if uppercase:
        for i in range(length):
            password = ''.join(random.choice(string.ascii_uppercase) for _ in range(length))
            passwords.append(password)
    
    if lowercase:
        for i in range(length):
            password = ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
            passwords.append(password)
    
    if numbers:
        for i in range(length):
            password = ''.join(random.choice(string.digits) for _ in range(length))
            passwords.append(password)
    
    if symbols:
        for i in range(length):
            password = ''.join(random.choice(string.punctuation) for _ in range(length))
            passwords.append(password)
    return passwords

def _write_to_file(passwords, path):
    with open(os.path.join(path, "passwords.txt"), "w") as file:
        for password in passwords:
            file.write(password + "\n")

def _ask_for_path():
    while True:
        try:
            path = input("Enter the path to the folder where you want to store the text file: ")
            if os.path.exists(path):
                return path
            else:
                print("Please enter a valid path.")
        except ValueError:
            print("Please enter a valid path.")

def _ask_for_length():
    while True:
        try:
            length = int(input("Enter the length of the password: "))
            return length
        except ValueError:
            print("Please enter a valid number.")

def _ask_for_char_types():
    special = _get_user_input("Do you want to include special characters in the password?  (y/n): ", ['y', 'n']) == 'y'
    uppercase = _get_user_input("Do you want to include uppercase letters in the password?  (y/n): ", ['y', 'n']) == 'y'
    lowercase = _get_user_input("Do you want to include lowercase letters in the password?  (y/n): ", ['y', 'n']) == 'y'
    numbers = _get_user_input("Do you want to include numbers in the password?  (y/n): ", ['y', 'n']) == 'y'
    symbols = _get_user_input("Do you want to include symbols in the password?  (y/n): ", ['y', 'n']) == 'y'
    return special, uppercase, lowercase, numbers, symbols

def main():
    print("Welcome to the password generator!")
    print("")
    length = _ask_for_length()
    special, uppercase, lowercase, numbers, symbols = _ask_for_char_types()
    passwords = _generate_passwords(length, special, uppercase, lowercase, numbers, symbols)
    print("\nHere are the generated passwords:")
    for password in passwords:
        print(password)
    print("")
    text = _get_user_input("Do you want to store the list of passwords in a text file?  (y/n): ", ['y', 'n']) == 'y'
    if text:
        path = _ask_for_path()
        _write_to_file(passwords, path)
        print("\nThe passwords have been stored in the text file.")
    print("")

def executar():
    """Roda o gerador interativo. Ponto de entrada publico desta unidade."""
    return main()

if __name__ == '__main__':
    executar()
