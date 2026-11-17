import random
import string
import os
import sys

def _ask_user_for_option(question, valid_answers):
    while True:
        answer = input(question)
        if answer in valid_answers:
            return answer
        else:
            print("Please enter a valid answer.")

def _ask_user_for_path():
    while True:
        try:
            path = input("Enter the path to the folder where you want to store the text file: ")
            if os.path.exists(path):
                return path
            else:
                print("Please enter a valid path.")
        except ValueError:
            print("Please enter a valid path.")

def _generate_password(length, include_special, include_uppercase, include_lowercase, include_numbers, include_symbols):
    password = ''
    if include_special:
        for j in range(length):
            password += random.choice(string.punctuation)
    if include_uppercase:
        for j in range(length):
            password += random.choice(string.ascii_uppercase)
    if include_lowercase:
        for j in range(length):
            password += random.choice(string.ascii_lowercase)
    if include_numbers:
        for j in range(length):
            password += random.choice(string.digits)
    if include_symbols:
        for j in range(length):
            password += random.choice(string.punctuation)
    return password

def _store_passwords(passwords, path):
    with open(path + "/passwords.txt", "w") as file:
        for password in passwords:
            file.write(password + "\n")

def _print_passwords(passwords):
    print("Here are the generated passwords:")
    for password in passwords:
        print(password)

def main():
    print("Welcome to the password generator!")
    print("")
    
    length = int(_ask_user_for_option("Enter the length of the password: ", ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']))
    include_special = _ask_user_for_option("Do you want to include special characters in the password? (y/n): ", ['y', 'n'])
    include_uppercase = _ask_user_for_option("Do you want to include uppercase letters in the password? (y/n): ", ['y', 'n'])
    include_lowercase = _ask_user_for_option("Do you want to include lowercase letters in the password? (y/n): ", ['y', 'n'])
    include_numbers = _ask_user_for_option("Do you want to include numbers in the password? (y/n): ", ['y', 'n'])
    include_symbols = _ask_user_for_option("Do you want to include symbols in the password? (y/n): ", ['y', 'n'])
    
    passwords = []
    for i in range(length):
        password = _generate_password(length, include_special == 'y', include_uppercase == 'y', include_lowercase == 'y', include_numbers == 'y', include_symbols == 'y')
        passwords.append(password)
    
    _print_passwords(passwords)
    print("")
    
    store_in_file = _ask_user_for_option("Do you want to store the list of passwords in a text file? (y/n): ", ['y', 'n'])
    if store_in_file == 'y':
        path = _ask_user_for_path()
        _store_passwords(passwords, path)
        print("The passwords have been stored in the text file.")
    print("")
    
    while True:
        answer = _ask_user_for_option("Do you want to generate more passwords? (y/n): ", ['y', 'n'])
        if answer == 'y':
            main()
        elif answer == 'n':
            print("Goodbye.")
            sys.exit()
        else:
            print("Please enter a valid answer.")
            print("")

def run():
    return main()

if __name__ == '__main__':
    run()
