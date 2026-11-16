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
    return length

def get_password_options():
    options = {
        'special': False,
        'uppercase': False,
        'lowercase': False,
        'numbers': False,
        'symbols': False
    }
    for option in options:
        while True:
            answer = input(f"Do you want to include {option} in the password? (y/n): ")
            if answer == 'y':
                options[option] = True
                break
            elif answer == 'n':
                break
            else:
                print("Please enter a valid answer.")
    return options

def get_storage_path():
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

def generate_passwords(length, options):
    passwords = []
    if options['special']:
        for _ in range(length):
            password = ''.join(random.choice(string.punctuation) for _ in range(length))
            passwords.append(password)
    if options['uppercase']:
        for _ in range(length):
            password = ''.join(random.choice(string.ascii_uppercase) for _ in range(length))
            passwords.append(password)
    if options['lowercase']:
        for _ in range(length):
            password = ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
            passwords.append(password)
    if options['numbers']:
        for _ in range(length):
            password = ''.join(random.choice(string.digits) for _ in range(length))
            passwords.append(password)
    if options['symbols']:
        for _ in range(length):
            password = ''.join(random.choice(string.punctuation) for _ in range(length))
            passwords.append(password)
    return passwords

def store_passwords(passwords, path):
    with open(os.path.join(path, "passwords.txt"), "w") as file:
        for password in passwords:
            file.write(password + "\n")

def main():
    print("Welcome to the password generator!")
    length = get_password_length()
    options = get_password_options()
    path = get_storage_path()
    
    passwords = generate_passwords(length, options)
    
    print("\nHere are the generated passwords:")
    for password in passwords:
        print(password)
    
    if options['special']:
        store_passwords(passwords, path)
        print("\nThe passwords have been stored in the text file.")

    while True:
        answer = input("\nDo you want to generate more passwords? (y/n): ")
        if answer == 'y':
            main()
        elif answer == 'n':
            print("\nGoodbye.")
            sys.exit()
        else:
            print("Please enter a valid answer.")

def executar():
    """Roda o gerador interativo. Ponto de entrada publico desta unidade."""
    return main()

if __name__ == '__main__':
    executar()
