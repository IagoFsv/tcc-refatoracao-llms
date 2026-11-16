import random
import string
import sys
import os

def get_password_length():
    while True:
        try:
            length = int(input("Enter the length of the password: "))
            break
        except ValueError:
            print("Please enter a valid number.")

def get_password_options():
    special = input("Do you want to include special characters in the password? (y/n): ").lower() == 'y'
    uppercase = input("Do you want to include uppercase letters in the password? (y/n): ").lower() == 'y'
    lowercase = input("Do you want to include lowercase letters in the password? (y/n): ").lower() == 'y'
    numbers = input("Do you want to include numbers in the password? (y/n): ").lower() == 'y'
    symbols = input("Do you want to include symbols in the password? (y/n): ").lower() == 'y'
    return special, uppercase, lowercase, numbers, symbols

def get_store_option():
    return input("Do you want to store the list of passwords in a text file? (y/n): ").lower() == 'y'

def get_store_path():
    while True:
        try:
            path = input("Enter the path to the folder where you want to store the text file: ")
            if os.path.exists(path):
                break
            else:
                print("Please enter a valid path.")
        except ValueError:
            print("Please enter a valid path.")

def generate_password(length, special, uppercase, lowercase, numbers, symbols):
    password = []
    if special:
        password.append(random.choice(string.punctuation))
    if uppercase:
        password.append(random.choice(string.ascii_uppercase))
    if lowercase:
        password.append(random.choice(string.ascii_lowercase))
    if numbers:
        password.append(random.choice(string.digits))
    if symbols:
        password.append(random.choice(string.punctuation))
    return ''.join(password)

def generate_passwords(length, special, uppercase, lowercase, numbers, symbols, count):
    return [generate_password(length, special, uppercase, lowercase, numbers, symbols) for _ in range(count)]

def store_passwords(passwords, path):
    with open(path + "/passwords.txt", "w") as file:
        for password in passwords:
            file.write(password + "\n")

def main():
    print("Welcome to the password generator!")
    length = get_password_length()
    special, uppercase, lowercase, numbers, symbols = get_password_options()
    store_passwords = get_store_option()
    if store_passwords:
        store_path = get_store_path()
    count = int(input("Enter the number of passwords to generate: "))
    passwords = generate_passwords(length, special, uppercase, lowercase, numbers, symbols, count)
    print("\nHere are the generated passwords:")
    for password in passwords:
        print(password)
    if store_passwords:
        store_passwords(passwords, store_path)
        print("\nThe passwords have been stored in the text file.")
    while True:
        answer = input("\nDo you want to generate more passwords? (y/n): ").lower()
        if answer == 'y':
            main()
        elif answer == 'n':
            print("\nGoodbye.")
            sys.exit()
        else:
            print("Please enter a valid answer.")

def executar():
    return main()

if __name__ == '__main__':
    executar()
