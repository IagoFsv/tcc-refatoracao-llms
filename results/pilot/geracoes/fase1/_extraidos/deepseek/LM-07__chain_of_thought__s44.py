import random
import string
import sys
import os

def ask_for_length():
    while True:
        try:
            length = int(input("Enter the length of the password: "))
            break
        except ValueError:
            print("Please enter a valid number.")
    return length

def ask_for_character_type(character_type):
    while True:
        answer = input(f"Do you want to include {character_type} in the password?  (y/n): ")
        if answer == 'y':
            return True
        elif answer == 'n':
            return False
        else:
            print("Please enter a valid answer.")

def generate_passwords(length, special=False, uppercase=False, lowercase=False, numbers=False, symbols=False):
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

def main():
    print("Welcome to the password generator!")
    print("")
    
    length = ask_for_length()
    
    special = ask_for_character_type("special characters")
    uppercase = ask_for_character_type("uppercase letters")
    lowercase = ask_for_character_type("lowercase letters")
    numbers = ask_for_character_type("numbers")
    symbols = ask_for_character_type("symbols")

    passwords = generate_passwords(length, special, uppercase, lowercase, numbers, symbols)

    print("")
    print("Here are the generated passwords:")
    for password in passwords:
        print(password)
    print("")

    # Rest of the code...

def executar():
    """Roda o gerador interativo. Ponto de entrada publico desta unidade."""
    return main()


if __name__ == '__main__':
    executar()
