import random
import string
import sys
import os

def get_user_input(prompt, valid_responses):
    while True:
        answer = input(prompt)
        if answer in valid_responses:
            return answer
        else:
            print("Please enter a valid answer.")

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

def save_passwords_to_file(passwords, path):
    with open(path + "/passwords.txt", "w") as file:
        for password in passwords:
            file.write(password + "\n")

def main():
    print("Welcome to the password generator!")
    print("")
    length = int(input("Enter the length of the password: "))
    special = get_user_input("Do you want to include special characters in the password? (y/n): ", ['y', 'n']) == 'y'
    uppercase = get_user_input("Do you want to include uppercase letters in the password? (y/n): ", ['y', 'n']) == 'y'
    lowercase = get_user_input("Do you want to include lowercase letters in the password? (y/n): ", ['y', 'n']) == 'y'
    numbers = get_user_input("Do you want to include numbers in the password? (y/n): ", ['y', 'n']) == 'y'
    symbols = get_user_input("Do you want to include symbols in the password? (y/n): ", ['y', 'n']) == 'y'
    text = get_user_input("Do you want to store the list of passwords in a text file? (y/n): ", ['y', 'n']) == 'y'
    path = input("Enter the path to the folder where you want to store the text file: ")
    
    passwords = generate_passwords(length, special, uppercase, lowercase, numbers, symbols)
    print("\nHere are the generated passwords:")
    for password in passwords:
        print(password)
    print("")
    
    if text:
        save_passwords_to_file(passwords, path)
        print("The passwords have been stored in the text file.")
    print("")

def executar():
    """Roda o gerador interativo. Ponto de entrada publico desta unidade."""
    return main()


if __name__ == '__main__':
    executar()
