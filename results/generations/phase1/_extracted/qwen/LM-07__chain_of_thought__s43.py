"""Generator of lists of random passwords, from the console.

Public entry point: run(). Do not change its name or signature; the rest of
the file may be freely reorganized.
"""

import random
import string
import sys
import os

def get_user_input():
    length = int(input("Enter the length of the password: "))
    special = input("Do you want to include special characters in the password? (y/n): ").lower() == 'y'
    uppercase = input("Do you want to include uppercase letters in the password? (y/n): ").lower() == 'y'
    lowercase = input("Do you want to include lowercase letters in the password? (y/n): ").lower() == 'y'
    numbers = input("Do you want to include numbers in the password? (y/n): ").lower() == 'y'
    symbols = input("Do you want to include symbols in the password? (y/n): ").lower() == 'y'
    text = input("Do you want to store the list of passwords in a text file? (y/n): ").lower() == 'y'
    path = input("Enter the path to the folder where you want to store the text file: ")
    return length, special, uppercase, lowercase, numbers, symbols, text, path

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

def store_passwords(passwords, path):
    with open(os.path.join(path, "passwords.txt"), "w") as file:
        for password in passwords:
            file.write(password + "\n")

def ask_to_generate_more():
    answer = input("Do you want to generate more passwords? (y/n): ").lower()
    return answer == 'y'

def main():
    print("Welcome to the password generator!")
    print("")
    
    length, special, uppercase, lowercase, numbers, symbols, text, path = get_user_input()
    
    passwords = generate_passwords(length, special, uppercase, lowercase, numbers, symbols)
    
    print("")
    print("Here are the generated passwords:")
    for password in passwords:
        print(password)
    print("")
    
    if text:
        store_passwords(passwords, path)
        print("")
        print("The passwords have been stored in the text file.")
    
    if ask_to_generate_more():
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
