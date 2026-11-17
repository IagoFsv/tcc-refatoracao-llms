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
    ask_for_uppercase(length)
    
    # Ask the user if they want to include lowercase letters in the password
    ask_for_lowercase(length)
    
    # Ask the user if they want to include numbers in the password
    # Rest of the code...
    
def ask_for_uppercase(length):
    while True:
        answer = input("Do you want to include uppercase letters in the password?  (y/n): ")
        if answer == 'y':
            uppercase = True
            break
        elif answer == 'n':
            break
        else:
            print("Please enter a valid answer.")

def ask_for_lowercase(length):
    while True:
        answer = input("Do you want to include lowercase letters in the password?  (y/n): ")
        if answer == 'y':
            lowercase = True
            break
        elif answer == 'n':
            break
        else:
            print("Please enter a valid answer.")
    
    # Rest of the code...

def run():
    """Runs the interactive generator. Public entry point of this unit."""
    return main()


if __name__ == '__main__':
    run()
