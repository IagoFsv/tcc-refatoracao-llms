"""Gerador de listas de senhas aleatorias, pelo console.

Ponto de entrada publico: executar(). Nao altere o nome nem a assinatura
dessa funcao; o restante do arquivo pode ser reorganizado livremente.
"""

import random
import string
import sys
import os

def _ask_for_length():
    while True:
        try:
            length = int(input("Enter the length of the password: "))
            break
        except ValueError:
            print("Please enter a valid number.")
    return length

def _ask_for_special_characters():
    while True:
        answer = input("Do you want to include special characters in the password?  (y/n): ")
        if answer == 'y':
            return True
        elif answer == 'n':
            return False
        else:
            print("Please enter a valid answer.")

def _ask_for_uppercase():
    while True:
        answer = input("Do you want to include uppercase letters in the password?  (y/n): ")
        if answer == 'y':
            return True
        elif answer == 'n':
            return False
        else:
            print("Please enter a valid answer.")

def _ask_for_lowercase():
    while True:
        answer = input("Do you want to include lowercase letters in the password?  (y/n): ")
        if answer == 'y':
            return True
        elif answer == 'n':
            return False
        else:
            print("Please enter a valid answer.")

def _ask_for_numbers():
    while True:
        answer = input("Do you want to include numbers in the password?  (y/n): ")
        if answer == 'y':
            return True
        elif answer == 'n':
            return False
        else:
            print("Please enter a valid answer.")

def _ask_for_symbols():
    while True:
        answer = input("Do you want to include symbols in the password?  (y/n): ")
        if answer == 'y':
            return True
        elif answer == 'n':
            return False
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

def _ask_for_text_file(passwords):
    while True:
        answer = input("Do you want to store the list of passwords in a text file?  (y/n): ")
        if answer == 'y':
            return _ask_for_text_file_path(passwords)
        elif answer == 'n':
            return
        else:
            print("Please enter a valid answer.")

def _ask_for_text_file_path(passwords):
    while True:
        try:
            path = input("Enter the path to the folder where you want to store the text file: ")
            if os.path.exists(path):
                return _write_to_text_file(path, passwords)
            else:
                print("Please enter a valid path.")
        except ValueError:
            print("Please enter a valid path.")

def _write_to_text_file(path, passwords):
    with open(os.path.join(path, "passwords.txt"), "w") as file:
        for password in passwords:
            file.write(password + "\n")
    print("The passwords have been stored in the text file.")

def _ask_for_more_passwords():
    while True:
        answer = input("Do you want to generate more passwords?  (y/n): ")
        if answer == 'y':
            return True
        elif answer == 'n':
            print("Goodbye.")
            sys.exit()
        else:
            print("Please enter a valid answer.")

def main():
    print("Welcome to the password generator!")
    print("")
    length = _ask_for_length()
    special = _ask_for_special_characters()
    uppercase = _ask_for_uppercase()
    lowercase = _ask_for_lowercase()
    numbers = _ask_for_numbers()
    symbols = _ask_for_symbols()
    passwords = _generate_passwords(length, special, uppercase, lowercase, numbers, symbols)
    _ask_for_text_file(passwords)
    while _ask_for_more_passwords():
        main()

def executar():
    """Roda o gerador interativo. Ponto de entrada publico desta unidade."""
    return main()

if __name__ == '__main__':
    executar()
