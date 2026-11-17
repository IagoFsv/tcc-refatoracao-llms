"""Simple banking system with cards stored in SQLite.

Public entry point: run(). Do not change its name or signature; the rest of
the file may be freely reorganized.
"""

import random
import sqlite3

class Bank:
    # Class for bank
    def  __init__(self):
        self.card_number = None
        self.pin = None
        self.balance = None
        self.id = None

    def create_account(self):
        # Create a new account
        self.generate_card_number()
        self.generate_pin()
        self.balance = 0
        self.id = random.randint(0000000000, 9999999999)

    def generate_card_number(self):
        self.card_number = '400000' + str(random.randint(000000000, 999999999)).zfill(9)
        card_number_list = [int(i) for i in self.card_number]
        self.apply_luhn_algorithm(card_number_list)

    def generate_pin(self):
        self.pin = str(random.randint(0000, 9999)).zfill(4)

    def apply_luhn_algorithm(self, card_number_list):
        for i in range(0, len(card_number_list), 2):
            card_number_list[i] *= 2
        for i in range(len(card_number_list)):
            if card_number_list[i] > 9:
                card_number_list[i] -= 9
        if sum(card_number_list) % 10 == 0:
            self.card_number += '0'
        else:
            self.card_number += str(10 - (sum(card_number_list) % 10))

# The rest of the code remains the same, the only changes are in the `create_account` method
