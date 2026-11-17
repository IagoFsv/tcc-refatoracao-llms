"""Generator of lists of random passwords, from the console.

Public entry point: run(). Do not change its name or signature; the rest of
the file may be freely reorganized.
"""

import random
import string
import sys
import os

def ask_for_option():
    while True:
        try:
            return int(input("Enter the length of the password: "))
        except ValueError:
            print("Please enter a valid number.")

def ask_for_character_type():
    while True:
        answer = input("Do you want to include {} in the password? (y/n): ")
        if answer == 'y':
            return True
        elif answer == 'n':
            return False
        else:
            print("Please enter a valid answer.")

def ask_for_file_storage():
    while True:
        answer = input("Do you want to store the list of passwords in a text file? (y/n): ")
        if answer == 'y':
            return True
        elif answer == 'n':
            return False
        else:
            print("Please enter a valid answer.")

def ask_for_file_path():
    while True:
        try:
            return input("Enter the path to the folder where you want to store the text file: ")
        except ValueError:
            print("Please enter a valid path.")

def ask_for_generate_more():
    while True:
        answer = input("Do you want to generate more passwords? (y/n): ")
        if answer == 'y':
            return True
        elif answer == 'n':
            print("Goodbye.")
            sys.exit()
        else:
            print("Please enter a valid answer.")

def generate_passwords(length, special, uppercase, lowercase, numbers, symbols):
    passwords = []
    if special:
        for _ in range(length):
            password = ''.join(random.choice(string.punctuation) for _ in range(length))
            passwords.append(password)
    if uppercase:
        for _ in range(length):
            password = ''.join(random.choice(string.ascii_uppercase) for _ in range(length))
            passwords.append(password)
    if lowercase:
        for _ in range(length):
            password = ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
            passwords.append(password)
    if numbers:
        for _ in range(length):
            password = ''.join(random.choice(string.digits) for _ in range(length))
            passwords.append(password)
    if symbols:
        for _ in range(length):
            password = ''.join(random.choice(string.punctuation) for _ in range(length))
            passwords.append(password)
    return passwords

def print_passwords(passwords):
    print("Here are the generated passwords:")
    for password in passwords:
        print(password)
    print()

def store_passwords_in_file(passwords, path):
    with open(path + "/passwords.txt", "w") as file:
        for password in passwords:
            file.write(password + "\n")
    print("The passwords have been stored in the text file.")

def main():
    print("Welcome to the password generator!")
    print("")
    
    length = ask_for_option()
    special = ask_for_character_type("special")
    uppercase = ask_for_character_type("uppercase")
    lowercase = ask_for_character_type("lowercase")
    numbers = ask_for_character_type("numbers")
    symbols = ask_for_character_type("symbols")
    
    passwords = generate_passwords(length, special, uppercase, lowercase, numbers, symbols)
    
    print_passwords(passwords)
    
    if ask_for_file_storage():
        path = ask_for_file_path()
        store_passwords_in_file(passwords, path)
    
    if ask_for_generate_more():
        main()

def run():
    """Runs the interactive generator. Public entry point of this unit."""
    return main()

if __name__ == '__main__':
    run()
