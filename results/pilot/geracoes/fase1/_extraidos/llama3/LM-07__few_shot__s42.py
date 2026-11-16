import random
import string
import os
import sys

def ask_user_for_input(prompt, valid_values):
    while True:
        answer = input(prompt)
        if answer in valid_values:
            return answer
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

def generate_password(length, include_special, include_uppercase, include_lowercase, include_numbers, include_symbols):
    passwords = []
    if include_special:
        passwords.extend([''.join(random.choice(string.punctuation) for _ in range(length)) for _ in range(length)])
    if include_uppercase:
        passwords.extend([''.join(random.choice(string.ascii_uppercase) for _ in range(length)) for _ in range(length)])
    if include_lowercase:
        passwords.extend([''.join(random.choice(string.ascii_lowercase) for _ in range(length)) for _ in range(length)])
    if include_numbers:
        passwords.extend([''.join(random.choice(string.digits) for _ in range(length)) for _ in range(length)])
    if include_symbols:
        passwords.extend([''.join(random.choice(string.punctuation) for _ in range(length)) for _ in range(length)])
    return passwords

def print_passwords(passwords):
    print("Here are the generated passwords:")
    for password in passwords:
        print(password)
    print()

def store_passwords_in_file(passwords, path):
    with open(path + "/passwords.txt", "w") as file:
        for password in passwords:
            file.write(password + "\n")
    print("The passwords have been stored in the text file.")

def main():
    print("Welcome to the password generator!")
    print()
    
    length = int(ask_user_for_input("Enter the length of the password: ", [str(i) for i in range(1, 101)]))
    include_special = ask_user_for_input("Do you want to include special characters in the password? (y/n): ", ['y', 'n'])
    include_uppercase = ask_user_for_input("Do you want to include uppercase letters in the password? (y/n): ", ['y', 'n'])
    include_lowercase = ask_user_for_input("Do you want to include lowercase letters in the password? (y/n): ", ['y', 'n'])
    include_numbers = ask_user_for_input("Do you want to include numbers in the password? (y/n): ", ['y', 'n'])
    include_symbols = ask_user_for_input("Do you want to include symbols in the password? (y/n): ", ['y', 'n'])
    text = ask_user_for_input("Do you want to store the list of passwords in a text file? (y/n): ", ['y', 'n'])
    path = ask_user_for_path()
    
    passwords = generate_password(length, include_special == 'y', include_uppercase == 'y', include_lowercase == 'y', include_numbers == 'y', include_symbols == 'y')
    print_passwords(passwords)
    
    if text == 'y':
        store_passwords_in_file(passwords, path)
    
    while True:
        answer = ask_user_for_input("Do you want to generate more passwords? (y/n): ", ['y', 'n'])
        if answer == 'y':
            main()
        elif answer == 'n':
            print("Goodbye.")
            sys.exit()
        else:
            print("Please enter a valid answer.")

def executar():
    return main()

if __name__ == '__main__':
    executar()
