import random
import string
import sys
import os

def get_user_input():
    length = int(input("Enter the length of the password: "))
    special = input("Do you want to include special characters in the password? (y/n): ").lower() == 'y'
    uppercase = input("Do you want to include uppercase letters in the password? (y/n): ").lower() == 'y'
    lowercase = input("Do you want to include lowercase letters in the password? (y/n): ").lower() == 'y'
    numbers = input("Do you want to include numbers in the password? (y/n): ").lower() == 'y'
    symbols = input("Do you want to include symbols in the password? (y/n): ").lower() == 'y'
    text = input("Do you want to store the list of passwords in a text file? (y/n): ").lower() == 'y'
    path = input("Enter the path to the folder where you want to store the text file: ")
    return length, special, uppercase, lowercase, numbers, symbols, text, path

def generate_passwords(length, special, uppercase, lowercase, numbers, symbols):
    passwords = []
    if special:
        passwords.extend([''.join(random.choice(string.punctuation) for _ in range(length)) for _ in range(length)])
    if uppercase:
        passwords.extend([''.join(random.choice(string.ascii_uppercase) for _ in range(length)) for _ in range(length)])
    if lowercase:
        passwords.extend([''.join(random.choice(string.ascii_lowercase) for _ in range(length)) for _ in range(length)])
    if numbers:
        passwords.extend([''.join(random.choice(string.digits) for _ in range(length)) for _ in range(length)])
    if symbols:
        passwords.extend([''.join(random.choice(string.punctuation) for _ in range(length)) for _ in range(length)])
    return passwords

def print_passwords(passwords):
    print("\nHere are the generated passwords:")
    for password in passwords:
        print(password)
    print()

def save_passwords_to_file(passwords, path):
    with open(path + "/passwords.txt", "w") as file:
        for password in passwords:
            file.write(password + "\n")
    print("\nThe passwords have been stored in the text file.")

def ask_to_generate_more():
    while True:
        answer = input("Do you want to generate more passwords? (y/n): ").lower()
        if answer == 'y':
            return True
        elif answer == 'n':
            print("\nGoodbye.")
            sys.exit()
        else:
            print("Please enter a valid answer.")

def main():
    length, special, uppercase, lowercase, numbers, symbols, text, path = get_user_input()
    passwords = generate_passwords(length, special, uppercase, lowercase, numbers, symbols)
    print_passwords(passwords)
    if text:
        save_passwords_to_file(passwords, path)
    if ask_to_generate_more():
        main()

def executar():
    """Roda o gerador interativo. Ponto de entrada público desta unidade."""
    return main()

if __name__ == '__main__':
    executar()
