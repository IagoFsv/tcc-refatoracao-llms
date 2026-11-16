import random
import string
import sys
import os

def _get_user_input(prompt, validator):
    while True:
        try:
            value = input(prompt)
            if validator(value):
                return value
            else:
                print("Please enter a valid answer.")
        except ValueError:
            print("Please enter a valid number.")

def _generate_password(length, special, uppercase, lowercase, numbers, symbols):
    password = ''
    if special:
        password += ''.join(random.choice(string.punctuation) for _ in range(length))
    if uppercase:
        password += ''.join(random.choice(string.ascii_uppercase) for _ in range(length))
    if lowercase:
        password += ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
    if numbers:
        password += ''.join(random.choice(string.digits) for _ in range(length))
    if symbols:
        password += ''.join(random.choice(string.punctuation) for _ in range(length))
    return ''.join(random.sample(password, len(password)))

def _store_passwords_to_file(passwords, path):
    with open(path + "/passwords.txt", "w") as file:
        for password in passwords:
            file.write(password + "\n")

def _ask_to_generate_more():
    while True:
        answer = input("Do you want to generate more passwords? (y/n): ")
        if answer == 'y':
            return True
        elif answer == 'n':
            print("")
            print("Goodbye.")
            sys.exit()
        else:
            print("Please enter a valid answer.")
            print("")

def main():
    print("Welcome to the password generator!")
    print("")
    
    length = int(_get_user_input("Enter the length of the password: ", lambda x: x.isdigit()))
    
    special = _get_user_input("Do you want to include special characters in the password? (y/n): ", lambda x: x.lower() in ['y', 'n']).lower() == 'y'
    uppercase = _get_user_input("Do you want to include uppercase letters in the password? (y/n): ", lambda x: x.lower() in ['y', 'n']).lower() == 'y'
    lowercase = _get_user_input("Do you want to include lowercase letters in the password? (y/n): ", lambda x: x.lower() in ['y', 'n']).lower() == 'y'
    numbers = _get_user_input("Do you want to include numbers in the password? (y/n): ", lambda x: x.lower() in ['y', 'n']).lower() == 'y'
    symbols = _get_user_input("Do you want to include symbols in the password? (y/n): ", lambda x: x.lower() in ['y', 'n']).lower() == 'y'
    
    text = _get_user_input("Do you want to store the list of passwords in a text file? (y/n): ", lambda x: x.lower() in ['y', 'n']).lower() == 'y'
    
    if text:
        path = _get_user_input("Enter the path to the folder where you want to store the text file: ", lambda x: os.path.exists(x))
    else:
        path = None
    
    passwords = [_generate_password(length, special, uppercase, lowercase, numbers, symbols) for _ in range(length)]
    
    print("") 
    print("Here are the generated passwords:") 
    for password in passwords: 
        print(password) 
    print("") 
    
    if text:
        _store_passwords_to_file(passwords, path)
        print("The passwords have been stored in the text file.")
    
    if _ask_to_generate_more():
        main()

def executar():
    """Roda o gerador interativo. Ponto de entrada publico desta unidade."""
    return main()


if __name__ == '__main__':
    executar()
