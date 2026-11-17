"""Generator of lists of random passwords, from the console.

Public entry point: run(). Do not change its name or signature; the rest of
the file may be freely reorganized.
"""

import random
import string
import sys
import os

def ask_for_input():
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
        answer = input("Do you want to include special characters in the password? (y/n): ")
        if answer == 'y':
            special = True
            break
        elif answer == 'n':
            special = False
            break
        else:
            print("Please enter a valid answer.")
        
    # ... and so on for the other input questions ...

def generate_passwords(special, uppercase, lowercase, numbers, symbols):
    passwords = []
    if special:
        for i in range(length):
            password = ''
            for j in range(length):
                password += random.choice(string.punctuation)
            passwords.append(password)
            
    if uppercase:
        for i in range(length):
            password = ''
            for j in range(length):
                password += random.choice(string.ascii_uppercase)
            passwords.append(password)
    
    # ... and so on for the other password generation logic ...

def print_passwords(passwords):
    print("")
    print("Here are the generated passwords:")
    for password in passwords:
        print(password)
    print("")
    
def store_passwords_in_text_file(passwords, path):
    with open(path + "/passwords.txt", "w") as file:
        for password in passwords:
            file.write(password + "\n")
    print("")
    print("The passwords have been stored in the text file.")
    
def ask_to_generate_more_passwords():
    while True:
        answer = input("Do you want to generate more passwords? (y/n): ")
        if answer == 'y':
            return True
        elif answer == 'n':
            return False
        else:
            print("Please enter a valid answer.")
            print("")
    
def main():
    # Ask the user for input
    ask_for_input()
    
    # Generate the list of passwords
    passwords = generate_passwords(special, uppercase, lowercase, numbers, symbols)
    
    # Print the list of passwords
    print_passwords(passwords)
    
    # Ask the user if they want to store the list of passwords in a text file
    if text:
        path = input("Enter the path to the folder where you want to store the text file: ")
        if os.path.exists(path):
            store_passwords_in_text_file(passwords, path)
    
    # Ask the user if they want to generate more passwords
    if ask_to_generate_more_passwords():
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
