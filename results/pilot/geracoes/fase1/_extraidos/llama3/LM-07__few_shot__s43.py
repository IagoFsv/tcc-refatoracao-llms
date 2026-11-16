import random
import string
import sys
import os

def ask_question(question, valid_answers):
    while True:
        answer = input(question)
        if answer in valid_answers:
            return answer
        print("Please enter a valid answer.")

def ask_password_options():
    print("Do you want to include:")
    print("  - Special characters?")
    print("  - Uppercase letters?")
    print("  - Lowercase letters?")
    print("  - Numbers?")
    print("  - Symbols?")
    special = ask_question("Do you want to include special characters? (y/n): ", ['y', 'n'])
    uppercase = ask_question("Do you want to include uppercase letters? (y/n): ", ['y', 'n'])
    lowercase = ask_question("Do you want to include lowercase letters? (y/n): ", ['y', 'n'])
    numbers = ask_question("Do you want to include numbers? (y/n): ", ['y', 'n'])
    symbols = ask_question("Do you want to include symbols? (y/n): ", ['y', 'n'])
    return special, uppercase, lowercase, numbers, symbols

def ask_path():
    while True:
        try:
            path = input("Enter the path to the folder where you want to store the text file: ")
            if os.path.exists(path):
                return path
            else:
                print("Please enter a valid path.")
        except ValueError:
            print("Please enter a valid path.")

def generate_password(length, special, uppercase, lowercase, numbers, symbols):
    passwords = []
    if special:
        for _ in range(length):
            password = ''.join(random.choice(string.punctuation) for _ in range(length))
            passwords.append(password)
    if uppercase:
        for _ in range(length):
            password = ''.join(random.choice(string.ascii_uppercase) for _ in range(length))
            passwords.append(password)
    if lowercase:
        for _ in range(length):
            password = ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
            passwords.append(password)
    if numbers:
        for _ in range(length):
            password = ''.join(random.choice(string.digits) for _ in range(length))
            passwords.append(password)
    if symbols:
        for _ in range(length):
            password = ''.join(random.choice(string.punctuation) for _ in range(length))
            passwords.append(password)
    return passwords

def print_passwords(passwords):
    print("Here are the generated passwords:")
    for password in passwords:
        print(password)
    print("")

def store_passwords(passwords, path):
    with open(path + "/passwords.txt", "w") as file:
        for password in passwords:
            file.write(password + "\n")
    print("The passwords have been stored in the text file.")

def main():
    print("Welcome to the password generator!")
    print("")
    length = int(ask_question("Enter the length of the password: ", ['1-100']))
    special, uppercase, lowercase, numbers, symbols = ask_password_options()
    passwords = generate_password(length, special, uppercase, lowercase, numbers, symbols)
    print_passwords(passwords)
    if ask_question("Do you want to store the list of passwords in a text file? (y/n): ", ['y', 'n']):
        path = ask_path()
        store_passwords(passwords, path)
    while True:
        answer = ask_question("Do you want to generate more passwords? (y/n): ", ['y', 'n'])
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
