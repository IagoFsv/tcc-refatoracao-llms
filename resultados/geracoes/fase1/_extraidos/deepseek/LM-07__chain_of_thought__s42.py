import random
import string
import sys
import os

def ask_user_for_input(prompt):
    while True:
        answer = input(prompt)
        if answer == 'y':
            return True
        elif answer == 'n':
            return False
        else:
            print("Please enter a valid answer.")

def generate_passwords(length, special, uppercase, lowercase, numbers, symbols):
    passwords = []
    if special:
        for i in range(length):
            password = ''.join(random.choice(string.punctuation) for _ in range(length))
            passwords.append(password)
            
    if uppercase:
        for i in range(length):
            password = ''.join(random.choice(string.ascii_uppercase) for _ in range(length))
            passwords.append(password)
    
    if lowercase:
        for i in range(length):
            password = ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
            passwords.append(password)
    
    if numbers:
        for i in range(length):
            password = ''.join(random.choice(string.digits) for _ in range(length))
            passwords.append(password)
    
    if symbols:
        for i in range(length):
            password = ''.join(random.choice(string.punctuation) for _ in range(length))
            passwords.append(password)
    
    return passwords

def main():
    print("Welcome to the password generator!")
    print("")
    
    # Ask the user for the length of the password
    length = int(input("Enter the length of the password: "))
    
    # Ask the user if they want to include special characters in the password
    special = ask_user_for_input("Do you want to include special characters in the password?  (y/n): ")
        
    # Ask the user if they want to include uppercase letters in the password
    uppercase = ask_user_for_input("Do you want to include uppercase letters in the password?  (y/n): ")
        
    # Ask the user if they want to include lowercase letters in the password
    lowercase = ask_user_for_input("Do you want to include lowercase letters in the password?  (y/n): ")
        
    # Ask the user if they want to include numbers in the password
    numbers = ask_user_for_input("Do you want to include numbers in the password?  (y/n): ")
        
    # Ask the user if they want to include symbols in the password
    symbols = ask_user_for_input("Do you want to include symbols in the password?  (y/n): ")
    
    # Generate the list of passwords
    passwords = generate_passwords(length, special, uppercase, lowercase, numbers, symbols)
    
    # Print the list of passwords
    print("") 
    print("Here are the generated passwords:") 
    for password in passwords: 
        print(password) 
    print("") 
    
    # Restante do código omitido para brevidade

def executar():
    """Roda o gerador interativo. Ponto de entrada publico desta unidade."""
    return main()

if __name__ == '__main__':
    executar()
