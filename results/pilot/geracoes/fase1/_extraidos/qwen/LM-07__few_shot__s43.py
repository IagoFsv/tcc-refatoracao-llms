import random
import string
import sys
import os

def _get_password_length():
    while True:
        try:
            length = int(input("Enter the length of the password: "))
            break
        except ValueError:
            print("Please enter a valid number.")
    return length

def _get_password_preferences():
    preferences = {
        'special': False,
        'uppercase': False,
        'lowercase': False,
        'numbers': False,
        'symbols': False
    }
    while True:
        answer = input("Do you want to include special characters in the password? (y/n): ")
        preferences['special'] = answer == 'y'
        answer = input("Do you want to include uppercase letters in the password? (y/n): ")
        preferences['uppercase'] = answer == 'y'
        answer = input("Do you want to include lowercase letters in the password? (y/n): ")
        preferences['lowercase'] = answer == 'y'
        answer = input("Do you want to include numbers in the password? (y/n): ")
        preferences['numbers'] = answer == 'y'
        answer = input("Do you want to include symbols in the password? (y/n): ")
        preferences['symbols'] = answer == 'y'
        if all(preferences.values()):
            break
        else:
            print("Please select at least one option.")
    return preferences

def _get_file_path():
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

def _generate_password(length, include_special, include_uppercase, include_lowercase, include_numbers, include_symbols):
    characters = ''
    if include_special:
        characters += string.punctuation
    if include_uppercase:
        characters += string.ascii_uppercase
    if include_lowercase:
        characters += string.ascii_lowercase
    if include_numbers:
        characters += string.digits
    if include_symbols:
        characters += string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def _generate_passwords(length, preferences, num_passwords):
    return [_generate_password(length, **preferences) for _ in range(num_passwords)]

def _print_passwords(passwords):
    print("Here are the generated passwords:")
    for password in passwords:
        print(password)
    print("")

def _write_passwords_to_file(passwords, path):
    with open(f"{path}/passwords.txt", "w") as file:
        for password in passwords:
            file.write(password + "\n")
    print("The passwords have been stored in the text file.")

def _ask_to_generate_more():
    while True:
        answer = input("Do you want to generate more passwords? (y/n): ")
        if answer == 'y':
            return True
        elif answer == 'n':
            print("Goodbye.")
            sys.exit()
        else:
            print("Please enter a valid answer.")

def main():
    length = _get_password_length()
    preferences = _get_password_preferences()
    path = _get_file_path()
    passwords = _generate_passwords(length, preferences, 1)
    _print_passwords(passwords)
    if preferences['special'] or preferences['uppercase'] or preferences['lowercase'] or preferences['numbers'] or preferences['symbols']:
        _write_passwords_to_file(passwords, path)
    if _ask_to_generate_more():
        main()

def executar():
    return main()

if __name__ == '__main__':
    executar()
