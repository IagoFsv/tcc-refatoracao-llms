"""Gerador de listas de senhas aleatórias, pelo console.

Ponto de entrada público: executar(). Não altere o nome nem a assinatura
dessa função; o restante do arquivo pode ser reorganizado livremente.
"""

import random
import string
import sys
import os

def main():
    print("Bem-vindo ao gerador de senhas!")
    print("")
    
    # Solicitar ao usuário o tamanho da senha
    while True:
        try:
            length = int(input("Digite o tamanho da senha: "))
            break
        except ValueError:
            print("Por favor, digite um número válido.")
            
    # Solicitar ao usuário se deseja incluir caracteres especiais na senha
    while True:
        answer = input("Deseja incluir caracteres especiais na senha? (s/n): ")
        if answer == 's':
            special = True
            break
        elif answer == 'n':
            special = False
            break
        else:
            print("Por favor, digite uma resposta válida.")
        
    # Solicitar ao usuário se deseja incluir letras maiúsculas na senha
    while True:
        answer = input("Deseja incluir letras maiúsculas na senha? (s/n): ")
        if answer == 's':
            uppercase = True
            break
        elif answer == 'n':
            uppercase = False
            break
        else:
            print("Por favor, digite uma resposta válida.")
        
    # Solicitar ao usuário se deseja incluir letras minúsculas na senha
    while True:
        answer = input("Deseja incluir letras minúsculas na senha? (s/n): ")
        if answer == 's':
            lowercase = True
            break
        elif answer == 'n':
            lowercase = False
            break
        else:
            print("Por favor, digite uma resposta válida.")
        
    # Solicitar ao usuário se deseja incluir números na senha
    while True:
        answer = input("Deseja incluir números na senha? (s/n): ")
        if answer == 's':
            numbers = True
            break
        elif answer == 'n':
            numbers = False
            break
        else:
            print("Por favor, digite uma resposta válida.")
        
    # Solicitar ao usuário se deseja incluir símbolos na senha
    while True:
        answer = input("Deseja incluir símbolos na senha? (s/n): ")
        if answer == 's':
            symbols = True
            break
        elif answer == 'n':
            symbols = False
            break
        else:
            print("Por favor, digite uma resposta válida.")
    
    # Retornar as opções de geração de senhas
    return length, special, uppercase, lowercase, numbers, symbols


def gerar_senhas(length, special, uppercase, lowercase, numbers, symbols):
    # Geração das senhas
    pass


def executar():
    """Roda o gerador interativo. Ponto de entrada público desta unidade."""
    length, special, uppercase, lowercase, numbers, symbols = main()
    return gerar_senhas(length, special, uppercase, lowercase, numbers, symbols)


if __name__ == '__main__':
    executar()
