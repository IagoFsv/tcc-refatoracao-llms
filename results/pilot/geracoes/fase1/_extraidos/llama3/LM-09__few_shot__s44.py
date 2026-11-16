"""Sistema bancario simples com cartoes guardados em SQLite.

Ponto de entrada publico: executar(). Nao altere o nome nem a assinatura
essa funcao; o restante do arquivo pode ser reorganizado livremente.
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

        # Luhn algorithm
        card_number_list = [int(i) for i in self.card_number]
        for i in range(0, len(card_number_list), 2):
            card_number_list[i] *= 2
        for i in range(len(card_number_list)):
            if card_number_list[i] > 9:
                card_number_list[i] -= 9
        if sum(card_number_list) % 10 == 0:
            self.card_number += '0'
        else:
            self.card_number += str(10 - (sum(card_number_list) % 10))
        self.pin = str(random.randint(0000, 9999)).zfill(4)
        self.balance = 0
        self.id = random.randint(0000000000, 9999999999)

def check_luhn(card_number):
    # Check Luhn algorithm
    card_number_list = [int(i) for i in card_number]
    for i in range(0, len(card_number_list), 2):
        card_number_list[i] *= 2
    for i in range(len(card_number_list)):
        if card_number_list[i] > 9:
            card_number_list[i] -= 9
    if sum(card_number_list) % 10 == 0:
        return True
    else:
        return False

def create_card(bank):
    # Create a new card
    bank.card_number = '400000' + str(random.randint(000000000, 999999999)).zfill(9)
    card_number_list = [int(i) for i in bank.card_number]
    for i in range(0, len(card_number_list), 2):
        card_number_list[i] *= 2
    for i in range(len(card_number_list)):
        if card_number_list[i] > 9:
            card_number_list[i] -= 9
    if sum(card_number_list) % 10 == 0:
        bank.card_number += '0'
    else:
        bank.card_number += str(10 - (sum(card_number_list) % 10))
    bank.pin = str(random.randint(0000, 9999)).zfill(4)
    bank.balance = 0
    bank.id = random.randint(0000000000, 9999999999)

def add_card_to_database(bank):
    # add data into database
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute('INSERT INTO card (id, number, pin, balance) VALUES (?, ?, ?, ?);', (bank.id, bank.card_number, bank.pin, bank.balance))
    conn.commit()

def check_card(card_number):
    # check card number and pin
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM card WHERE number = ?;', (card_number,))
    conn.commit()
    if cur.fetchone():
        return True
    else:
        return False

def get_balance(card_number):
    # get balance
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute('SELECT balance FROM card WHERE number = ?;', (card_number,))
    conn.commit()
    return cur.fetchone()[0]

def add_income(card_number, income):
    # add income
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute('UPDATE card SET balance = balance + ? WHERE number = ?;', (income, card_number))
    conn.commit()

def transfer(card_number, transfer_card_number, transfer_money):
    # transfer
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute('SELECT balance FROM card WHERE number = ?;', (card_number,))
    conn.commit()
    if cur.fetchone()[0] < transfer_money:
        print('Not enough money!')
    else:
        cur.execute('UPDATE card SET balance = balance - ? WHERE number = ?;', (transfer_money, card_number))
        conn.commit()
        cur.execute('UPDATE card SET balance = balance + ? WHERE number = ?;', (transfer_money, transfer_card_number))
        conn.commit()
        print('Success!')

def close_account(card_number, pin):
    # close account
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute('DELETE FROM card WHERE number = ? AND pin = ?;', (card_number, pin))
    conn.commit()

def main():
    # connect database and create table
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS card (id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);')
    conn.commit()

    # while loop and give chioce to user
    while True:
        print('1. Create an account')
        print('2. Log into account')
        print('0. Exit')
        choice = int(input())
        if choice == 1:
            bank = Bank()
            create_card(bank)
            print('Your card has been created')
            print('Your card number:')
            print(bank.card_number)
            print('Your card PIN:')
            print(bank.pin)
            add_card_to_database(bank)
        elif choice == 2:
            print('Enter your card number:')
            card_number = input()
            print('Enter your PIN:')
            pin = input()
            if check_card(card_number) and pin == bank.pin:
                print('You have successfully logged in!')
                while True:
                    print('1. Balance')
                    print('2. Add income')
                    print('3. Do transfer')
                    print('4. Close account')
                    print('5. Log out')
                    print('0. Exit')
                    choice = int(input())
                    if choice == 1:
                        print('Balance: ' + str(get_balance(card_number)))
                    elif choice == 2:
                        print('Enter income:')
                        income = int(input())
                        add_income(card_number, income)
                        print('Income was added!')
                    elif choice == 3:
                        print('Transfer')
                        print('Enter card number:')
                        transfer_card_number = input()
                        if check_luhn(transfer_card_number):
                            pass
                        else:
                            print('Probably you made a mistake in the card number. Please try again!')
                            continue
                        if check_card(transfer_card_number):
                            print('Enter how much money you want to transfer:')
                            transfer_money = int(input())
                            if get_balance(card_number) < transfer_money:
                                print('Not enough money!')
                            else:
                                transfer(card_number, transfer_card_number, transfer_money)
                                print('Success!')
                        else:
                            print('Such a card does not exist.')
                    elif choice == 4:
                        close_account(card_number, pin)
                        print('The account has been closed!')
                        break
                    elif choice == 5:
                        print('You have successfully logged out!')
                        break
                    elif choice == 0:
                        print("Bye!")
                        exit()
            else:
                print('Wrong card number or PIN!')
        elif choice == 0:
            print('Bye!')
            exit()

def executar():
    """Roda o menu do banco. Ponto de entrada publico desta unidade."""
    return main()


if __name__ == "__main__":
    executar()
