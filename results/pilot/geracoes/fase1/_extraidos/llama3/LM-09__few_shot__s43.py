def _create_account(self):
    self.card_number = '400000' + str(random.randint(000000000, 999999999)).zfill(9)
    self.pin = str(random.randint(0000, 9999)).zfill(4)
    self.balance = 0
    self.id = random.randint(0000000000, 9999999999)

def _check_luhn(card_number):
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

def main():
    # ...
    elif choice == 1:
        bank = Bank()
        bank._create_account()
        print('Your card has been created')
        print('Your card number:')
        print(bank.card_number)
        print('Your card PIN:')
        print(bank.pin)
        # ...
    elif choice == 2:
        # ...
        elif choice == 3:
            print('Transfer')
            print('Enter card number:')
            transfer_card_number = input()
            if _check_luhn(transfer_card_number):
                pass
            else:
                print('Probably you made a mistake in the card number. Please try again!')
                continue
            # ...
        # ...
