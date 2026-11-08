import random
import string
import sys
import os

def main():
    print("Welcome to the password generator!")
    print("")
    
    # Ask the user for the length of the password
    length = int(input("Enter the length of the password: "))
    
    # Ask the user if they want to include special characters in the password
    special = input("Do you want to include special characters in the password?  (y/n): ") == 'y'
    
    # Ask the user if they want to include uppercase letters in the password
    uppercase = input("Do you want to include uppercase letters in the password?  (y/n): ") == 'y'
    
    # Ask the user if they want to include lowercase letters in the password
    lowercase = input("Do you want to include lowercase letters in the password?  (y/n): ") == 'y'
    
    # Ask the user if they want to include numbers in the password
    numbers = input("Do you want to include numbers in the password?  (y/n): ") == 'y'
    
    # Ask the user if they want to include symbols in the password
    symbols = input("Do you want to include symbols in the password?  (y/n): ") == 'y'
    
    # Ask the user if they want to store the list of passwords in a text file
    text = input("Do you want to store the list of passwords in a text file?  (y/n): ") == 'y'
    
    # Generate the list of passwords
    passwords = generate_passwords(length, special, uppercase, lowercase, numbers, symbols)
    
    # Print the list of passwords
    print("") 
    print("Here are the generated passwords:") 
    for password in passwords: 
        print(password) 
    print("") 
    
    # Ask the user if he wants to store the list of passwords in a text file
    if text: 
        store_passwords_in_file(passwords)
        print("The passwords have been stored in the text file.")       
    print("")       
    
    # Ask the user if he wants to generate more passwords       
    if input("Do you want to generate more passwords?  (y/n): ") == 'y':       
        main()       
    else:       
        print("")       
        print("Goodbye.")       
        sys.exit()       


def generate_passwords(length, special, uppercase, lowercase, numbers, symbols):
    passwords = []
    if special:
        passwords.extend(generate_random_password(length, string.punctuation))
    if uppercase:
        passwords.extend(generate_random_password(length, string.ascii_uppercase))
    if lowercase:
        passwords.extend(generate_random_password(length, string.ascii_lowercase))
    if numbers:
        passwords.extend(generate_random_password(length, string.digits))
    if symbols:
        passwords.extend(generate_random_password(length, string.punctuation))
    return passwords


def generate_random_password(length, chars):
    return [''.join(random.choice(chars) for _ in range(length)) for _ in range(length)]


def store_passwords_in_file(passwords):
    path = input("Enter the path to the folder where you want to store the text file: ")
    with open(os.path.join(path, "passwords.txt"), "w") as file:
        for password in passwords:
            file.write(password + "\n")


def executar():
    """Roda o gerador interativo. Ponto de entrada publico desta unidade."""
    return main()


if __name__ == '__main__':
    executar()
