import random
import string
import sys
import os

def _obter_opcao_usuario(mensagem, opcoes):
    while True:
        answer = input(mensagem)
        if answer in opcoes:
            return answer
        else:
            print("Please enter a valid answer.")

def _gerar_senha(length, special, uppercase, lowercase, numbers, symbols):
    password = ''
    if special:
        password += random.choice(string.punctuation)
    if uppercase:
        password += random.choice(string.ascii_uppercase)
    if lowercase:
        password += random.choice(string.ascii_lowercase)
    if numbers:
        password += random.choice(string.digits)
    if symbols:
        password += random.choice(string.punctuation)
    return ''.join(random.sample(password, length))

def _gerar_passwords(length, special, uppercase, lowercase, numbers, symbols, quantidade):
    return [_gerar_senha(length, special, uppercase, lowercase, numbers, symbols) for _ in range(quantidade)]

def _obter_caminho_valido(mensagem):
    while True:
        try:
            path = input(mensagem)
            if os.path.exists(path):
                return path
            else:
                print("Please enter a valid path.")
        except ValueError:
            print("Please enter a valid path.")

def _salvar_passwords(passwords, path):
    with open(path + "/passwords.txt", "w") as file:
        for password in passwords:
            file.write(password + "\n")

def _executar_interativo():
    print("Welcome to the password generator!")
    print("")
    length = int(input("Enter the length of the password: "))
    special = _obter_opcao_usuario("Do you want to include special characters in the password? (y/n): ", ['y', 'n']) == 'y'
    uppercase = _obter_opcao_usuario("Do you want to include uppercase letters in the password? (y/n): ", ['y', 'n']) == 'y'
    lowercase = _obter_opcao_usuario("Do you want to include lowercase letters in the password? (y/n): ", ['y', 'n']) == 'y'
    numbers = _obter_opcao_usuario("Do you want to include numbers in the password? (y/n): ", ['y', 'n']) == 'y'
    symbols = _obter_opcao_usuario("Do you want to include symbols in the password? (y/n): ", ['y', 'n']) == 'y'
    quantidade = int(input("Enter the number of passwords to generate: "))
    path = _obter_caminho_valido("Enter the path to the folder where you want to store the text file: ")
    
    passwords = _gerar_passwords(length, special, uppercase, lowercase, numbers, symbols, quantidade)
    
    print("")
    print("Here are the generated passwords:")
    for password in passwords:
        print(password)
    print("")
    
    if _obter_opcao_usuario("Do you want to store the list of passwords in a text file? (y/n): ", ['y', 'n']) == 'y':
        _salvar_passwords(passwords, path)
        print("The passwords have been stored in the text file.")
    
    while _obter_opcao_usuario("Do you want to generate more passwords? (y/n): ", ['y', 'n']) == 'y':
        _executar_interativo()
    print("Goodbye.")
    sys.exit()

def executar():
    _executar_interativo()

if __name__ == '__main__':
    executar()
