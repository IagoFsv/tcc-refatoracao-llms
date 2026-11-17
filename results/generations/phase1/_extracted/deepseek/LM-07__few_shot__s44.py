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
    length = get_password_length()

    # Ask the user if they want to include special characters in the password
    special = get_user_answer("Do you want to include special characters in the password?  (y/n): ")
    
    # Ask the user if they want to include uppercase letters in the password
    uppercase = get_user_answer("Do you want to include uppercase letters in the password?  (y/n): ")
        
    # Ask the user if they want to include lowercase letters in the password
    lowercase = get_user_answer("Do you want to include lowercase letters in the password?  (y/n): ")
        
    # Ask the user if they want to include numbers in the password
    numbers = get_user_answer("Do you want to include numbers in the password?  (y/n): ")
        
    # Ask the user if they want to include symbols in the password
    symbols = get_user_answer("Do you want to include symbols in the password?  (y/n): ")
        
    # Ask the user if they want to store the list of passwords in a text file
    text = get_user_answer("Do you want to store the list of passwords in a text file?  (y/n): ")
        
    # Ask the user where they want to store the text file
    path = get_file_path()
        
    # Generate the list of passwords
    passwords = generate_passwords(length, special, uppercase, lowercase, numbers, symbols)
        
    # Print the list of passwords
    print_passwords(passwords)
        
    # Ask the user if he wants to store the list of passwords in a text file
    if text: 
        store_passwords_in_file(passwords, path)
        print("The passwords have been stored in the text file.")       
    print("")       
        
    # Ask the user if he wants to generate more passwords       
    if get_user_answer("Do you want to generate more passwords?  (y/n): "):       
        main()       
    else:       
        print("Goodbye.")       
        sys.exit()       


def get_password_length():
    while True:
        try:
            length = int(input("Enter the length of the password: "))
            break
        except ValueError:
            print("Please enter a valid number.")
    return length

def get_user_answer(question):
    while True:
        answer = input(question)
        if answer == 'y':
            return True
        elif answer == 'n':
            return False
        else:
            print("Please enter a valid answer.")

def get_file_path():
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
    passwords = []
    if special:
        passwords.extend(generate_password(length, string.punctuation))
    if uppercase:
        passwords.extend(generate_password(length, string.ascii_uppercase))
    if lowercase:
        passwords.extend(generate_password(length, string.ascii_lowercase))
    if numbers:
        passwords.extend(generate_password(length, string.digits))
    if symbols:
        passwords.extend(generate_password(length, string.punctuation))
    return passwords

def generate_password(length, chars):
    return [''.join(random.choice(chars) for _ in range(length)) for _ in range(length)]

def print_passwords(passwords):
    print("Here are the generated passwords:") 
    for password in passwords: 
        print(password) 
    print("") 

def store_passwords_in_file(passwords, path):
    with open(os.path.join(path, "passwords.txt"), "w") as file:       
        for password in passwords:       
            file.write(password + "\n") 

def run():
    """Runs the interactive generator. Public entry point of this unit."""
    return main()

if __name__ == '__main__':
    run()
