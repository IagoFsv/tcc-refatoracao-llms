import random
import sqlite3

class Bank:
    # Class for bank
    def __init__(self):
        self.card_number = None
        self.pin = None
        self.balance = None
        self.id = None

    def create_card_number(self):
        # Create a new account
        self.card_number = '400000' + str(random.randint(000000000, 999999999)).zfill(9)

    def create_pin(self):
        # Generate a new PIN
        self.pin = str(random.randint(0000, 9999)).zfill(4)

    def set_initial_balance(self):
        # Set initial balance
        self.balance = 0

    def create_id(self):
        # Generate a new ID
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

# Rest of the code remains the same
