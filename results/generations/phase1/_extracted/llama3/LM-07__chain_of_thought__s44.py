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
    
    length = ask_for_length()
    special = ask_for_special_characters()
    uppercase = ask_for_uppercase_letters()
    lowercase = ask_for_lowercase_letters()
    numbers = ask_for_numbers()
    symbols = ask_for_symbols()
    text = ask_to_store_passwords_in_file()
    path = ask_for_path_to_store_file()
    
    passwords = generate_passwords(length, special, uppercase, lowercase, numbers, symbols)
    print_passwords(passwords)
    
    if text:
        with open(path + "/passwords.txt", "w") as file:
            for password in passwords:
                file.write(password + "\n")
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
