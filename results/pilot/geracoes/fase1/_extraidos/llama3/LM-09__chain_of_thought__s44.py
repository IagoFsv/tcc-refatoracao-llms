class Bank:
    # Class for bank
    def __init__(self):
        self.card_number = None
        self.pin = None
        self.balance = None
        self.id = None

    def create_account(self):
        self.card_number = self.create_card_number()
        self.pin = self.create_pin()
        self.balance = 0
        self.id = random.randint(0000000000, 9999999999)
        self.create_account_details()

    def create_card_number(self):
        card_number = '400000' + str(random.randint(000000000, 999999999)).zfill(9)
        card_number_list = [int(i) for i in card_number]
        for i in range(0, len(card_number_list), 2):
            card_number_list[i] *= 2
        for i in range(len(card_number_list)):
            if card_number_list[i] > 9:
                card_number_list[i] -= 9
        if sum(card_number_list) % 10 == 0:
            card_number += '0'
        else:
            card_number += str(10 - (sum(card_number_list) % 10))
        return card_number

    def create_pin(self):
        return str(random.randint(0000, 9999)).zfill(4)

    def create_account_details(self):
        # add data into database
        cur.execute('INSERT INTO card (id, number, pin, balance) VALUES (?, ?, ?, ?);', (self.id, self.card_number, self.pin, self.balance))
        conn.commit()

def main():
    # ...

