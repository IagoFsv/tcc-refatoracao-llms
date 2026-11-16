import random
import string
import sys
import os

def get_user_input():
    while True:
        try:
            length = int(input("Enter the length of the password: "))
            break
        except ValueError:
            print("Please enter a valid number.")
    
    special = get_boolean_input("Do you want to include special characters in the password? (y/n): ")
    uppercase = get_boolean_input("Do you want to include uppercase letters in the password? (y/n): ")
    lowercase = get_boolean_input("Do you want to include lowercase letters in the password? (y/n): ")
    numbers = get_boolean_input("Do you want to include numbers in the password? (y/n): ")
    symbols = get_boolean_input("Do you want to include symbols in the password? (y/n): ")
    
    while True:
        answer = input("Do you want to store the list of passwords in a text file? (y/n): ")
        if answer == 'y':
            text = True
            break
        elif answer == 'n':
            text = False
            break
        else:
            print("Please enter a valid answer.")
    
    while True:
        try:
            path = input("Enter the path to the folder where you want to store the text file: ")
            if os.path.exists(path):
                break
            else:
                print("Please enter a valid path.")
        except ValueError:
            print("Please enter a valid path.")
    
    return length, special, uppercase, lowercase, numbers, symbols, text, path

def generate_passwords(length, special, uppercase, lowercase, numbers, symbols):
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

def write_to_file(passwords, path):
    with open(f"{path}/passwords.txt", "w") as file:
        for password in passwords:
            file.write(password + "\n")

def get_boolean_input(prompt):
    while True:
        answer = input(prompt)
        if answer == 'y':
            return True
        elif answer == 'n':
            return False
        else:
            print("Please enter a valid answer.")

def main():
    print("Welcome to the password generator!")
    print("")
    
    length, special, uppercase, lowercase, numbers, symbols, text, path = get_user_input()
    
    passwords = generate_passwords(length, special, uppercase, lowercase, numbers, symbols)
    
    print("")
    print("Here are the generated passwords:")
    for password in passwords:
        print(password)
    print("")
    
    if text:
        write_to_file(passwords, path)
        print("")
        print("The passwords have been stored in the text file.")
    
    while True:
        answer = input("Do you want to generate more passwords? (y/n): ")
        if answer == 'y':
            main()
        elif answer == 'n':
            print("")
            print("Goodbye.")
            sys.exit()
        else:
            print("Please enter a valid answer.")
            print("")

def executar():
    return main()

if __name__ == '__main__':
    executar()
