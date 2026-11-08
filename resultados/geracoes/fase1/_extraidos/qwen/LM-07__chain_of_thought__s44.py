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
    
    if text:
        path = input("Enter the path to the folder where you want to store the text file: ")
        while not os.path.exists(path):
            print("Please enter a valid path.")
            path = input("Enter the path to the folder where you want to store the text file: ")
    
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

def store_passwords(passwords, path):
    with open(os.path.join(path, "passwords.txt"), "w") as file:
        for password in passwords:
            file.write(password + "\n")
    print("The passwords have been stored in the text file.")

def main_loop():
    while True:
        length, special, uppercase, lowercase, numbers, symbols, text, path = get_user_input()
        passwords = generate_passwords(length, special, uppercase, lowercase, numbers, symbols)
        
        print("\nHere are the generated passwords:")
        for password in passwords:
            print(password)
        
        if text:
            store_passwords(passwords, path)
        
        answer = input("\nDo you want to generate more passwords? (y/n): ").lower()
        if answer != 'y':
            print("\nGoodbye.")
            sys.exit()

def executar():
    """Roda o gerador interativo. Ponto de entrada publico desta unidade."""
    print("Welcome to the password generator!")
    print("")
    main_loop()

if __name__ == '__main__':
    executar()
