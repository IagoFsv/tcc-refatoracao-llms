import random
import string
import sys
import os

def ask_for_input(question, valid_answers):
    while True:
        answer = input(question)
        if answer in valid_answers:
            return answer
        else:
            print("Please enter a valid answer.")

def generate_passwords(length, special, uppercase, lowercase, numbers, symbols):
    passwords = []
    if special:
        passwords.extend(random.choice(string.punctuation) * length for _ in range(length))
    if uppercase:
        passwords.extend(random.choice(string.ascii_uppercase) * length for _ in range(length))
    if lowercase:
        passwords.extend(random.choice(string.ascii_lowercase) * length for _ in range(length))
    if numbers:
        passwords.extend(random.choice(string.digits) * length for _ in range(length))
    if symbols:
        passwords.extend(random.choice(string.punctuation) * length for _ in range(length))
    return passwords

def ask_for_path():
    while True:
        try:
            path = input("Enter the path to the folder where you want to store the text file: ")
            if os.path.exists(path):
                return path
            else:
                print("Please enter a valid path.")
        except ValueError:
            print("Please enter a valid path.")

def store_passwords(passwords, path):
    with open(os.path.join(path, "passwords.txt"), "w") as file:
        for password in passwords:
            file.write(password + "\n")

def main():
    print("Welcome to the password generator!")
    print("")
    length = int(input("Enter the length of the password: "))
    special = ask_for_input("Do you want to include special characters in the password? (y/n): ", ['y', 'n']) == 'y'
    uppercase = ask_for_input("Do you want to include uppercase letters in the password? (y/n): ", ['y', 'n']) == 'y'
    lowercase = ask_for_input("Do you want to include lowercase letters in the password? (y/n): ", ['y', 'n']) == 'y'
    numbers = ask_for_input("Do you want to include numbers in the password? (y/n): ", ['y', 'n']) == 'y'
    symbols = ask_for_input("Do you want to include symbols in the password? (y/n): ", ['y', 'n']) == 'y'
    text = ask_for_input("Do you want to store the list of passwords in a text file? (y/n): ", ['y', 'n']) == 'y'
    
    passwords = generate_passwords(length, special, uppercase, lowercase, numbers, symbols)
    
    print("Here are the generated passwords:")
    for password in passwords:
        print(password)
    print("")
    
    if text:
        path = ask_for_path()
        store_passwords(passwords, path)
        print("The passwords have been stored in the text file.")
    print("")

def executar():
    """Roda o gerador interativo. Ponto de entrada publico desta unidade."""
    return main()

if __name__ == '__main__':
    executar()
