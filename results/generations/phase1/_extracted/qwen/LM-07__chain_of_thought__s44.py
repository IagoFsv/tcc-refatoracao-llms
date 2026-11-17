"""Generator of lists of random passwords, from the console.

Public entry point: run(). Do not change its name or signature; the rest of
the file may be freely reorganized.
"""

import random
import string
import sys
import os

def get_user_input():
    """Handles user input for password generation parameters."""
    while True:
        try:
            length = int(input("Enter the length of the password: "))
            break
        except ValueError:
            print("Please enter a valid number.")
    
    special = get_user_choice("Do you want to include special characters in the password? (y/n): ")
    uppercase = get_user_choice("Do you want to include uppercase letters in the password? (y/n): ")
    lowercase = get_user_choice("Do you want to include lowercase letters in the password? (y/n): ")
    numbers = get_user_choice("Do you want to include numbers in the password? (y/n): ")
    symbols = get_user_choice("Do you want to include symbols in the password? (y/n): ")
    
    return length, special, uppercase, lowercase, numbers, symbols

def get_user_choice(prompt):
    """Handles user input for yes/no choices."""
    while True:
        answer = input(prompt)
        if answer == 'y':
            return True
        elif answer == 'n':
            return False
        else:
            print("Please enter a valid answer.")

def get_file_path():
    """Handles user input for the path to store the text file."""
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

def generate_passwords(length, special, uppercase, lowercase, numbers, symbols):
    """Generates the list of passwords based on user input."""
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

def store_passwords(passwords, path):
    """Stores the list of passwords in a text file."""
    with open(f"{path}/passwords.txt", "w") as file:
        for password in passwords:
            file.write(password + "\n")
    print("The passwords have been stored in the text file.")

def main():
    print("Welcome to the password generator!")
    print("")
    
    length, special, uppercase, lowercase, numbers, symbols = get_user_input()
    
    passwords = generate_passwords(length, special, uppercase, lowercase, numbers, symbols)
    
    print("")
    print("Here are the generated passwords:")
    for password in passwords:
        print(password)
    print("")
    
    if get_user_choice("Do you want to store the list of passwords in a text file? (y/n): "):
        path = get_file_path()
        store_passwords(passwords, path)
    
    while True:
        if get_user_choice("Do you want to generate more passwords? (y/n): "):
            main()
        else:
            print("")
            print("Goodbye.")
            sys.exit()

def run():
    """Runs the interactive generator. Public entry point of this unit."""
    return main()


if __name__ == '__main__':
    run()
