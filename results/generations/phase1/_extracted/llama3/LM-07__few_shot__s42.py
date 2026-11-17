import random
import string
import sys
import os

def ask_user_for_length():
    while True:
        try:
            length = int(input("Enter the length of the password: "))
            return length
        except ValueError:
            print("Please enter a valid number.")

def ask_user_for_special_characters():
    while True:
        answer = input("Do you want to include special characters in the password? (y/n): ")
        if answer == 'y':
            return True
        elif answer == 'n':
            return False
        else:
            print("Please enter a valid answer.")

def ask_user_for_uppercase_letters():
    while True:
        answer = input("Do you want to include uppercase letters in the password? (y/n): ")
        if answer == 'y':
            return True
        elif answer == 'n':
            return False
        else:
            print("Please enter a valid answer.")

def ask_user_for_lowercase_letters():
    while True:
        answer = input("Do you want to include lowercase letters in the password? (y/n): ")
        if answer == 'y':
            return True
        elif answer == 'n':
            return False
        else:
            print("Please enter a valid answer.")

def ask_user_for_numbers():
    while True:
        answer = input("Do you want to include numbers in the password? (y/n): ")
        if answer == 'y':
            return True
        elif answer == 'n':
            return False
        else:
            print("Please enter a valid answer.")

def ask_user_for_symbols():
    while True:
        answer = input("Do you want to include symbols in the password? (y/n): ")
        if answer == 'y':
            return True
        elif answer == 'n':
            return False
        else:
            print("Please enter a valid answer.")

def ask_user_for_text_file():
    while True:
        answer = input("Do you want to store the list of passwords in a text file? (y/n): ")
        if answer == 'y':
            return True
        elif answer == 'n':
            return False
        else:
            print("Please enter a valid answer.")

def ask_user_for_path():
    while True:
        try:
            path = input("Enter the path to the folder where you want to store the text file: ")
            if os.path.exists(path):
                return path
            else:
                print("Please enter a valid path.")
        except ValueError:
            print("Please enter a valid path.")

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

def run():
    """Runs the interactive generator. Public entry point of this unit."""
    print("Welcome to the password generator!")
    print("")
    length = ask_user_for_length()
    special = ask_user_for_special_characters()
    uppercase = ask_user_for_uppercase_letters()
    lowercase = ask_user_for_lowercase_letters()
    numbers = ask_user_for_numbers()
    symbols = ask_user_for_symbols()
    passwords = generate_passwords(length, special, uppercase, lowercase, numbers, symbols)
    print_passwords(passwords)
    if ask_user_for_text_file():
        path = ask_user_for_path()
        store_passwords_in_text_file(passwords, path)
    while True:
        answer = input("Do you want to generate more passwords? (y/n): ")
        if answer == 'y':
            run()
        elif answer == 'n':
            print("")
            print("Goodbye.")
            sys.exit()
        else:
            print("Please enter a valid answer.")
            print("")

if __name__ == '__main__':
    run()
