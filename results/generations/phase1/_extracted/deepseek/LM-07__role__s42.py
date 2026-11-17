"""Generator of lists of random passwords, from the console.

Public entry point: run(). Do not change its name or signature; the rest of
the file may be freely reorganized.
"""

import random
import string
import sys
import os

def ask_for_input(prompt, valid_answers):
    while True:
        answer = input(prompt)
        if answer in valid_answers:
            return answer
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

def get_path():
    while True:
        try:
            path = input("Enter the path to the folder where you want to store the text file: ")
            if os.path.exists(path):
                return path
            else:
                print("Please enter a valid path.")
        except ValueError:
            print("Please enter a valid path.")

def write_to_file(path, passwords):
    with open(os.path.join(path, "passwords.txt"), "w") as file:
        for password in passwords:
            file.write(password + "\n")

def main():
    print("Welcome to the password generator!")
    print("")
    
    length = int(input("Enter the length of the password: "))
    special = ask_for_input("Do you want to include special characters in the password? (y/n): ", ['y', 'n']) == 'y'
    uppercase = ask_for_input("Do you want to include uppercase letters in the password? (y/n): ", ['y', 'n']) == 'y'
    lowercase = ask_for_input("Do you want to include lowercase letters in the password? (y/n): ", ['y', 'n']) == 'y'
    numbers = ask_for_input("Do you want to include numbers in the password? (y/n): ", ['y', 'n']) == 'y'
    symbols = ask_for_input("Do you want to include symbols in the password? (y/n): ", ['y', 'n']) == 'y'
    text = ask_for_input("Do you want to store the list of passwords in a text file? (y/n): ", ['y', 'n']) == 'y'
    
    passwords = generate_passwords(length, special, uppercase, lowercase, numbers, symbols)
    
    print("\nHere are the generated passwords:")
    for password in passwords:
        print(password)
    print("")
    
    if text:
        path = get_path()
        write_to_file(path, passwords)
        print("\nThe passwords have been stored in the text file.")
    print("")

def run():
    """Runs the interactive generator. Public entry point of this unit."""
    return main()

if __name__ == '__main__':
    run()
