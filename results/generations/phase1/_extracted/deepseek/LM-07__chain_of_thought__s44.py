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

def ask_for_yes_no(question):
    while True:
        answer = input(question)
        if answer.lower() in ['y', 'n']:
            return answer.lower() == 'y'
        else:
            print("Please enter a valid answer.")

def generate_passwords(length, special, uppercase, lowercase, numbers, symbols):
    passwords = []
    if special:
        passwords.extend(generate_random_string(length, string.punctuation) for _ in range(length))
    if uppercase:
        passwords.extend(generate_random_string(length, string.ascii_uppercase) for _ in range(length))
    if lowercase:
        passwords.extend(generate_random_string(length, string.ascii_lowercase) for _ in range(length))
    if numbers:
        passwords.extend(generate_random_string(length, string.digits) for _ in range(length))
    if symbols:
        passwords.extend(generate_random_string(length, string.punctuation) for _ in range(length))
    return passwords

def generate_random_string(length, chars):
    return ''.join(random.choice(chars) for _ in range(length))

def ask_for_path():
    while True:
        try:
            path = input("Enter the path to the folder where you want to store the text file: ")
            if os.path.exists(path):
                return path
            else:
                print("Please enter a valid path.")
        except ValueError:
            print("Please enter a valid path.")

def save_passwords_to_file(passwords, path):
    with open(os.path.join(path, "passwords.txt"), "w") as file:
        for password in passwords:
            file.write(password + "\n")

def handle_text_option(passwords, path):
    print("Do you want to store the list of passwords in a text file?  (y/n):")
    if ask_for_yes_no(""):
        path = ask_for_path()
        save_passwords_to_file(passwords, path)
        print("The passwords have been stored in the text file.")

def handle_more_passwords_option():
    print("Do you want to generate more passwords?  (y/n):")
    return ask_for_yes_no("")

def main():
    print("Welcome to the password generator!")
    print("")

    length = ask_for_length()

    special = ask_for_yes_no("Do you want to include special characters in the password?  (y/n): ")
    uppercase = ask_for_yes_no("Do you want to include uppercase letters in the password?  (y/n): ")
    lowercase = ask_for_yes_no("Do you want to include lowercase letters in the password?  (y/n): ")
    numbers = ask_for_yes_no("Do you want to include numbers in the password?  (y/n): ")
    symbols = ask_for_yes_no("Do you want to include symbols in the password?  (y/n): ")

    passwords = generate_passwords(length, special, uppercase, lowercase, numbers, symbols)

    print("\nHere are the generated passwords:")
    for password in passwords:
        print(password)
    print("")

    handle_text_option(passwords, ask_for_path())

    print("")
    if handle_more_passwords_option():
        main()
    else:
        print("Goodbye.")
        sys.exit()

def run():
    """Runs the interactive generator. Public entry point of this unit."""
    main()

if __name__ == '__main__':
    run()
