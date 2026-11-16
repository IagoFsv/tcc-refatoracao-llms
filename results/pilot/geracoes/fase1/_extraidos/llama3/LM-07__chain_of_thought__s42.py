import random
import string
import sys
import os

def ask_for_length():
    while True:
        try:
            length = int(input("Enter the length of the password: "))
            return length
        except ValueError:
            print("Please enter a valid number.")

def ask_for_special_characters():
    while True:
        answer = input("Do you want to include special characters in the password? (y/n): ")
        if answer == 'y':
            return True
        elif answer == 'n':
            return False
        else:
            print("Please enter a valid answer.")

def ask_for_uppercase_letters():
    while True:
        answer = input("Do you want to include uppercase letters in the password? (y/n): ")
        if answer == 'y':
            return True
        elif answer == 'n':
            return False
        else:
            print("Please enter a valid answer.")

# ...

def generate_passwords(length, special, uppercase, numbers, symbols):
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
    # ...
    return passwords

def write_passwords_to_file(passwords, path):
    with open(path + "/passwords.txt", "w") as file:
        for password in passwords:
            file.write(password + "\n")
    print("The passwords have been stored in the text file.")

def main():
    print("Welcome to the password generator!")
    print("")
    length = ask_for_length()
    special = ask_for_special_characters()
    uppercase = ask_for_uppercase_letters()
    numbers = ask_for_numbers()
    symbols = ask_for_symbols()
    passwords = generate_passwords(length, special, uppercase, numbers, symbols)
    print("Here are the generated passwords:")
    for password in passwords:
        print(password)
    print("")
    if ask_for_text_file():
        path = ask_for_path()
        write_passwords_to_file(passwords, path)
        print("The passwords have been stored in the text file.")
    print("")
    while True:
        answer = input("Do you want to generate more passwords? (y/n): ")
        if answer == 'y':
            main()
        elif answer == 'n':
            print("Goodbye.")
            sys.exit()
        else:
            print("Please enter a valid answer.")
            print("")

def executar():
    return main()

if __name__ == '__main__':
    executar()
