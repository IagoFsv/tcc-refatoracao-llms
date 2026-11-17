"""Generator of lists of random passwords, from the console.

Public entry point: run(). Do not change its name or signature; the rest of
the file may be freely reorganized.
"""

import random
import string
import sys
import os

def _get_password_length():
    while True:
        try:
            length = int(input("Enter the length of the password: "))
            break
        except ValueError:
            print("Please enter a valid number.")
    return length

def _get_password_inclusion_options():
    options = {
        'special': False,
        'uppercase': False,
        'lowercase': False,
        'numbers': False,
        'symbols': False
    }
    while True:
        answer = input("Do you want to include special characters in the password? (y/n): ")
        if answer == 'y':
            options['special'] = True
            break
        elif answer == 'n':
            break
        else:
            print("Please enter a valid answer.")
    while True:
        answer = input("Do you want to include uppercase letters in the password? (y/n): ")
        if answer == 'y':
            options['uppercase'] = True
            break
        elif answer == 'n':
            break
        else:
            print("Please enter a valid answer.")
    while True:
        answer = input("Do you want to include lowercase letters in the password? (y/n): ")
        if answer == 'y':
            options['lowercase'] = True
            break
        elif answer == 'n':
            break
        else:
            print("Please enter a valid answer.")
    while True:
        answer = input("Do you want to include numbers in the password? (y/n): ")
        if answer == 'y':
            options['numbers'] = True
            break
        elif answer == 'n':
            break
        else:
            print("Please enter a valid answer.")
    while True:
        answer = input("Do you want to include symbols in the password? (y/n): ")
        if answer == 'y':
            options['symbols'] = True
            break
        elif answer == 'n':
            break
        else:
            print("Please enter a valid answer.")
    return options

def _get_store_in_text_file_option():
    while True:
        answer = input("Do you want to store the list of passwords in a text file? (y/n): ")
        if answer == 'y':
            return True
        elif answer == 'n':
            return False
        else:
            print("Please enter a valid answer.")

def _get_text_file_path():
    while True:
        try:
            path = input("Enter the path to the folder where you want to store the text file: ")
            if os.path.exists(path):
                return path
            else:
                print("Please enter a valid path.")
        except ValueError:
            print("Please enter a valid path.")

def _generate_passwords(length, options):
    passwords = []
    if options['special']:
        for i in range(length):
            password = ''.join(random.choice(string.punctuation) for _ in range(length))
            passwords.append(password)
    if options['uppercase']:
        for i in range(length):
            password = ''.join(random.choice(string.ascii_uppercase) for _ in range(length))
            passwords.append(password)
    if options['lowercase']:
        for i in range(length):
            password = ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
            passwords.append(password)
    if options['numbers']:
        for i in range(length):
            password = ''.join(random.choice(string.digits) for _ in range(length))
            passwords.append(password)
    if options['symbols']:
        for i in range(length):
            password = ''.join(random.choice(string.punctuation) for _ in range(length))
            passwords.append(password)
    return passwords

def _print_passwords(passwords):
    print("\nHere are the generated passwords:")
    for password in passwords:
        print(password)
    print("")

def _store_passwords_in_text_file(passwords, path):
    with open(os.path.join(path, "passwords.txt"), "w") as file:
        for password in passwords:
            file.write(password + "\n")
    print("The passwords have been stored in the text file.\n")

def main():
    print("Welcome to the password generator!")
    length = _get_password_length()
    options = _get_password_inclusion_options()
    store_in_text_file = _get_store_in_text_file_option()
    if store_in_text_file:
        path = _get_text_file_path()
    passwords = _generate_passwords(length, options)
    _print_passwords(passwords)
    if store_in_text_file:
        _store_passwords_in_text_file(passwords, path)
    while True:
        answer = input("\nDo you want to generate more passwords? (y/n): ")
        if answer == 'y':
            main()
        elif answer == 'n':
            print("\nGoodbye.")
            sys.exit()
        else:
            print("Please enter a valid answer.\n")

def run():
    """Runs the interactive generator. Public entry point of this unit."""
    return main()

if __name__ == '__main__':
    run()
