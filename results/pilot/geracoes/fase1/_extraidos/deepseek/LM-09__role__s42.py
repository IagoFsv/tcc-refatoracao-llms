"""Sistema bancario simples com cartoes guardados em SQLite.

Ponto de entrada publico: executar(). Nao altere o nome nem a assinatura
dessa funcao; o restante do arquivo pode ser reorganizado livremente.
"""

import random
import sqlite3

class Bank:
    # Class for bank
    def __init__(self):
        self.card_number = None
        self.pin = None
        self.balance = None
        self.id = None

    def create_account(self):
        # Create a new account
        self.card_number = '400000' + str(random.randint(000000000, 999999999)).zfill(9)
        self.generate_pin()
        self.balance = 0
        self.id = random.randint(0000000000, 9999999999)

    def generate_pin(self):
        # Luhn algorithm
        card_number_list = [int(i) for i in self.card_number]
        self.pin = self.calculate_pin(card_number_list)

    def calculate_pin(self, card_number_list):
        for i in range(0, len(card_number_list), 2):
            card_number_list[i] *= 2
        for i in range(len(card_number_list)):
            if card_number_list[i] > 9:
                card_number_list[i] -= 9
        check_digit = '0' if sum(card_number_list) % 10 == 0 else str(10 - (sum(card_number_list) % 10))
        return str(random.randint(0000, 9999)).zfill(4) + check_digit

def check_luhn(card_number):
    # Check Luhn algorithm
    card_number_list = [int(i) for i in card_number]
    for i in range(0, len(card_number_list), 2):
        card_number_list[i] *= 2
    for i in range(len(card_number_list)):
        if card_number_list[i] > 9:
            card_number_list[i] -= 9
    return sum(card_number_list) % 10 == 0

def main():
    # connect database and create table
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS card  (id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);')
    conn.commit()

    # while loop and give chioce to user
    while True:
        print('1. Create an account')
        print('2. Log into account')
        print('0. Exit')
        choice = int(input())
        if choice == 1:
            bank = Bank()
            bank.create_account()
            print('Your card has been created')
            print('Your card number:')
            print(bank.card_number)
            print('Your card PIN:')
            print(bank.pin)
            # add data into database
            cur.execute('INSERT INTO card  (id, number, pin, balance) VALUES  (?, ?, ?, ?);', 
                        (bank.id, bank.card_number, bank.pin, bank.balance))
            conn.commit()
        # ... rest of the code remains the same
