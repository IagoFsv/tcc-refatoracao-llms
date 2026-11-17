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
    if get_text_file():
        # Ask the user where they want to store the text file
        path = get_path()
        
        # Write the list of passwords to a text file       
        write_to_file(passwords, path)
        print("The passwords have been stored in the text file.")       
    print("")       
    
    # Ask the user if he wants to generate more passwords       
    if get_more_passwords():
        main()
    else:
        print("Goodbye.")
        sys.exit()

def run():
    """Runs the interactive generator. Public entry point of this unit."""
    return main()

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
            return True
        elif answer == 'n':
            return False
        else:
            print("Please enter a valid answer.")

def get_uppercase_letters():
    while True:
        answer = input("Do you want to include uppercase letters in the password?  (y/n): ")
        if answer == 'y':
            return True
        elif answer == 'n':
            return False
        else:
            print("Please enter a valid answer.")

def get_lowercase_letters():
    while True:
        answer = input("Do you want to include lowercase letters in the password?  (y/n): ")
        if answer == 'y':
            return True
        elif answer == 'n':
            return False
        else:
            print("Please enter a valid answer.")

def get_numbers():
    while True:
        answer = input("Do you want to include numbers in the password?  (y/n): ")
        if answer == 'y':
            return True
        elif answer == 'n':
            return False
        else:
            print("Please enter a valid answer.")

def get_symbols():
    while True:
        answer = input("Do you want to include symbols in the password?  (y/n): ")
        if answer == 'y':
            return True
        elif answer == 'n':
            return False
        else:
            print("Please enter a valid answer.")

def generate_passwords(length, special, uppercase, lowercase, numbers, symbols):
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
    
    if lowercase:
        for i in range(length):
            password = '' 
            for j in range(length): 
                password += random.choice(string.ascii_lowercase) 
            passwords.append(password) 
    
    if numbers: 
        for i in range(length): 
            password = '' 
            for j in range(length): 
                password += random.choice(string.digits) 
            passwords.append(password) 
    
    if symbols: 
        for i in range(length): 
            password = '' 
            for j in range(length): 
                password += random.choice(string.punctuation) 
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
            return True
        elif answer == 'n':
            return False
        else:
            print("Please enter a valid answer.")

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

def get_more_passwords():
    while True:       
        answer = input("Do you want to generate more passwords?  (y/n): ")       
        if answer == 'y':       
            return True       
        elif answer == 'n':       
            return False       
        else:       
            print("Please enter a valid answer.")

if __name__ == '__main__':
    run()
