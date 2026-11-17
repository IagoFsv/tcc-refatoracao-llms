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
    length = get_length()
    
    # Ask the user if they want to include special characters in the password
    special = get_special_characters()
    
    # Ask the user if they want to include uppercase letters in the password
    uppercase = get_uppercase_letters()
    
    # Ask the user if they want to include lowercase letters in the password
    lowercase = get_lowercase_letters()
    
    # Ask the user if they want to include numbers in the password
    numbers = get_numbers()
    
    # Ask the user if they want to include symbols in the password
    symbols = get_symbols()
    
    # Generate the list of passwords
    passwords = generate_passwords(length, special, uppercase, lowercase, numbers, symbols)
    
    # Print the list of passwords
    print_passwords(passwords)
    
    # Ask the user if they want to store the list of passwords in a text file
    text = get_text_file()
    
    # Ask the user where they want to store the text file
    path = get_path()
    
    # Write the list of passwords to a text file       
    write_to_file(passwords, path)
    
    # Ask the user if he wants to generate more passwords       
    generate_more_passwords()


def get_length():
    while True:
        try:
            length = int(input("Enter the length of the password: "))
            break
        except ValueError:
            print("Please enter a valid number.")
    return length


def get_special_characters():
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
    return special


def get_uppercase_letters():
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
    return uppercase


def get_lowercase_letters():
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
    return lowercase


def get_numbers():
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
    return numbers


def get_symbols():
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
    return symbols


def generate_passwords(length, special, uppercase, lowercase, numbers, symbols):
    passwords = []
    if special:
        passwords.extend(generate_characters(length, string.punctuation))
    if uppercase:
        passwords.extend(generate_characters(length, string.ascii_uppercase))
    if lowercase:
        passwords.extend(generate_characters(length, string.ascii_lowercase))
    if numbers:
        passwords.extend(generate_characters(length, string.digits))
    if symbols:
        passwords.extend(generate_characters(length, string.punctuation))
    return passwords


def generate_characters(length, characters):
    passwords = []
    for _ in range(length):
        password = ''.join(random.choice(characters) for _ in range(length))
        passwords.append(password)
    return passwords


def print_passwords(passwords):
    print("Here are the generated passwords:")
    for password in passwords:
        print(password)
    print("")


def get_text_file():
    while True:
        answer = input("Do you want to store the list of passwords in a text file?  (y/n): ")
        if answer == 'y':
            text = True
            break
        elif answer == 'n':
            text = False
            break
        else:
            print("Please enter a valid answer.")
    return text


def get_path():
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


def write_to_file(passwords, path):
    with open(path + "/passwords.txt", "w") as file:
        for password in passwords:
            file.write(password + "\n")
    print("The passwords have been stored in the text file.")


def generate_more_passwords():
    while True:
        answer = input("Do you want to generate more passwords?  (y/n): ")
        if answer == 'y':
            main()
        elif answer == 'n':
            print("")
            print("Goodbye.")
            sys.exit()
        else:
            print("Please enter a valid answer.")
            print("")


def run():
    """Runs the interactive generator. Public entry point of this unit."""
    return main()


if __name__ == '__main__':
    run()
