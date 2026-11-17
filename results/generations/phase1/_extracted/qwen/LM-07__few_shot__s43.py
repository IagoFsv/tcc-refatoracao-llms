"""Generator of lists of random passwords, from the console.

Public entry point: run(). Do not change its name or signature; the rest of
the file may be freely reorganized.
"""

import random
import string
import sys
import os

def get_password_length():
    while True:
        try:
            length = int(input("Enter the length of the password: "))
            break
        except ValueError:
            print("Please enter a valid number.")
    return length

def get_password_preferences():
    preferences = {
        'special': False,
        'uppercase': False,
        'lowercase': False,
        'numbers': False,
        'symbols': False
    }
    for key in preferences:
        while True:
            answer = input(f"Do you want to include {key} in the password? (y/n): ")
            if answer == 'y':
                preferences[key] = True
                break
            elif answer == 'n':
                break
            else:
                print("Please enter a valid answer.")
    return preferences

def get_store_path():
    while True:
        try:
            path = input("Enter the path to the folder where you want to store the text file: ")
            if os.path.exists(path):
                break
            else:
                print("Please enter a valid path.")
        except ValueError:
            print("Please enter a valid path.")
    return path

def generate_passwords(length, preferences):
    passwords = []
    for key, value in preferences.items():
        if value:
            for i in range(length):
                password = ''.join(random.choices(getattr(string, key.upper()), k=length))
                passwords.append(password)
    return passwords

def print_passwords(passwords):
    print("\nHere are the generated passwords:")
    for password in passwords:
        print(password)
    print("")

def store_passwords(passwords, path):
    with open(os.path.join(path, "passwords.txt"), "w") as file:
        for password in passwords:
            file.write(password + "\n")
    print("The passwords have been stored in the text file.")

def ask_generate_more():
    while True:
        answer = input("\nDo you want to generate more passwords? (y/n): ")
        if answer == 'y':
            return True
        elif answer == 'n':
            print("\nGoodbye.")
            sys.exit()
        else:
            print("Please enter a valid answer.")

def main():
    print("Welcome to the password generator!")
    length = get_password_length()
    preferences = get_password_preferences()
    path = get_store_path()
    passwords = generate_passwords(length, preferences)
    print_passwords(passwords)
    if preferences['special'] or preferences['uppercase'] or preferences['lowercase'] or preferences['numbers'] or preferences['symbols']:
        store_passwords(passwords, path)
    if ask_generate_more():
        main()

def run():
    """Runs the interactive generator. Public entry point of this unit."""
    return main()


if __name__ == '__main__':
    run()
