class Bank:
    # Class for bank
    def __init__(self):
        self.card_number = None
        self.pin = None
        self.balance = None
        self.id = None

    def generate_card_number(self):
        # Generate a new card number
        self.card_number = '400000' + str(random.randint(000000000, 999999999)).zfill(9)

    def generate_pin(self):
        # Generate a new PIN
        self.pin = str(random.randint(0000, 9999)).zfill(4)

    def create_account(self):
        # Create a new account
        self.generate_card_number()
        self.generate_pin()
        self.balance = 0
        self.id = random.randint(0000000000, 9999999999)

    # ... (rest of the code remains the same)
