"""Generator of lists of random passwords, from the console.

Public entry point: run(). Do not change its name or signature; the rest of
the file may be freely reorganized.
"""

import random
import string
import sys
import os

def _get_user_input():
    while True:
        try:
            length = int(input("Enter the length of the password: "))
            break
        except ValueError:
            print("Please enter a valid number.")
    
    special = _get_boolean_input("Do you want to include special characters in the password? (y/n): ")
    uppercase = _get_boolean_input("Do you want to include uppercase letters in the password? (y/n): ")
    lowercase = _get_boolean_input("Do you want to include lowercase letters in the password? (y/n): ")
    numbers = _get_boolean_input("Do you want to include numbers in the password? (y/n): ")
    symbols = _get_boolean_input("Do you want to include symbols in the password? (y/n): ")
    text = _get_boolean_input("Do you want to store the list of passwords in a text file? (y/n): ")
    
    while True:
        try:
            path = input("Enter the path to the folder where you want to store the text file: ")
            if os.path.exists(path):
                break
            else:
                print("Please enter a valid path.")
        except ValueError:
            print("Please enter a valid path.")
    
    return length, special, uppercase, lowercase, numbers, symbols, text, path

def _get_boolean_input(prompt):
    while True:
        answer = input(prompt)
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

def _store_passwords(passwords, path):
    with open(os.path.join(path, "passwords.txt"), "w") as file:
        for password in passwords:
            file.write(password + "\n")

def main():
    length, special, uppercase, lowercase, numbers, symbols, text, path = _get_user_input()
    passwords = _generate_passwords(length, special, uppercase, lowercase, numbers, symbols)
    
    print("Here are the generated passwords:")
    for password in passwords:
        print(password)
    
    if text:
        _store_passwords(passwords, path)
        print("The passwords have been stored in the text file.")
    
    while True:
        answer = input("Do you want to generate more passwords? (y/n): ")
        if answer == 'y':
            main()
        elif answer == 'n':
            print("Goodbye.")
            sys.exit()
        else:
            print("Please enter a valid answer.")

def run():
    """Runs the interactive generator. Public entry point of this unit."""
    return main()


if __name__ == '__main__':
    run()
