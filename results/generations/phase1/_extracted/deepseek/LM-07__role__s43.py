"""Generator of lists of random passwords, from the console.

Public entry point: run(). Do not change its name or signature; the rest of
the file may be freely reorganized.
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
        answer = input("Do you want to include special characters in the password?  (y/n): ")
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
        answer = input("Do you want to include uppercase letters in the password?  (y/n): ")
        if answer == 'y':
            uppercase = True
            break
        elif answer == 'n':
            uppercase = False
            break
        else:
            print("Please enter a valid answer.")
        
    # Ask the user if they want to include lowercase letters in the password
    while True:
        answer = input("Do you want to include lowercase letters in the password?  (y/n): ")
        if answer == 'y':
            lowercase = True
            break
        elif answer == 'n':
            lowercase = False
            break
        else:
            print("Please enter a valid answer.")
    
    # Ask the user if they want to include numbers in the password
    while True:
        answer = input("Do you want to include numbers in the password?  (y/n): ")
        if answer == 'y':
            numbers = True
            break
        elif answer == 'n':
            numbers = False
            break
        else:
            print("Please enter a valid answer.")
        
    # Ask the user if they want to include symbols in the password
    while True:
        answer = input("Do you want to include symbols in the password?  (y/n): ")
        if answer == 'y':
            symbols = True
            break
        elif answer == 'n':
            symbols = False
            break
        else:
            print("Please enter a valid answer.")
    
    return length, special, uppercase, lowercase, numbers, symbols

def generate_passwords(length, special, uppercase, lowercase, numbers, symbols):
    passwords = []
    
    if special:
        passwords += generate_special_characters_password(length)
    if uppercase:
        passwords += generate_uppercase_letters_password(length)
    if lowercase:
        passwords += generate_lowercase_letters_password(length)
    if numbers:
        passwords += generate_numbers_password(length)
    if symbols:
        passwords += generate_symbols_password(length)
    
    return passwords

def generate_special_characters_password(length):
    return [''.join(random.choice(string.punctuation) for _ in range(length)) for _ in range(length)]

def generate_uppercase_letters_password(length):
    return [''.join(random.choice(string.ascii_uppercase) for _ in range(length)) for _ in range(length)]

def generate_lowercase_letters_password(length):
    return [''.join(random.choice(string.ascii_lowercase) for _ in range(length)) for _ in range(length)]

def generate_numbers_password(length):
    return [''.join(random.choice(string.digits) for _ in range(length)) for _ in range(length)]

def generate_symbols_password(length):
    return [''.join(random.choice(string.punctuation) for _ in range(length)) for _ in range(length)]

def print_passwords(passwords):
    print("\nHere are the generated passwords:\n")
    for password in passwords:
        print(password)

def run():
    """Runs the interactive generator. Public entry point of this unit."""
    length, special, uppercase, lowercase, numbers, symbols = main()
    passwords = generate_passwords(length, special, uppercase, lowercase, numbers, symbols)
    print_passwords(passwords)

if __name__ == '__main__':
    run()
