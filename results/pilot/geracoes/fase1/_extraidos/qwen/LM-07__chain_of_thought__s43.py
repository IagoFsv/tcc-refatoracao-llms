import random
import string
import sys
import os

def solicitar_preferencias():
    while True:
        try:
            length = int(input("Enter the length of the password: "))
            break
        except ValueError:
            print("Please enter a valid number.")
    
    special = input("Do you want to include special characters in the password? (y/n): ").lower() == 'y'
    uppercase = input("Do you want to include uppercase letters in the password? (y/n): ").lower() == 'y'
    lowercase = input("Do you want to include lowercase letters in the password? (y/n): ").lower() == 'y'
    numbers = input("Do you want to include numbers in the password? (y/n): ").lower() == 'y'
    symbols = input("Do you want to include symbols in the password? (y/n): ").lower() == 'y'
    
    text = input("Do you want to store the list of passwords in a text file? (y/n): ").lower() == 'y'
    if text:
        while True:
            try:
                path = input("Enter the path to the folder where you want to store the text file: ")
                if os.path.exists(path):
                    break
                else:
                    print("Please enter a valid path.")
            except ValueError:
                print("Please enter a valid path.")
    
    return length, special, uppercase, lowercase, numbers, symbols, text, path if text else None

def gerar_senhas(length, special, uppercase, lowercase, numbers, symbols):
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

def armazenar_senhas(passwords, path):
    with open(path + "/passwords.txt", "w") as file:
        for password in passwords:
            file.write(password + "\n")
    print("The passwords have been stored in the text file.")

def main():
    print("Welcome to the password generator!")
    print("")
    
    length, special, uppercase, lowercase, numbers, symbols, text, path = solicitar_preferencias()
    passwords = gerar_senhas(length, special, uppercase, lowercase, numbers, symbols)
    
    print("Here are the generated passwords:")
    for password in passwords:
        print(password)
    print("")
    
    if text:
        armazenar_senhas(passwords, path)
    
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
    """Roda o gerador interativo. Ponto de entrada publico desta unidade."""
    return main()

if __name__ == '__main__':
    executar()
