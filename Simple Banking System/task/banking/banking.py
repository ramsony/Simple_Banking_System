import random


def luhn_algo(numbers):
    check_sum = 0
    odd_numbers = numbers[-1::-2]
    even_numbers = numbers[-2::-2]
    check_sum += sum(odd_numbers)
    for n in even_numbers:
        temp = n * 2
        if temp > 9:
            check_sum += (temp - 9)
        else:
            check_sum += temp
    return True if check_sum % 10 == 0 else False


def generate_card_number():
    bank_identification_number = [4, 0, 0, 0, 0, 0]
    ac = ''
    account_identifier = random.sample(range(0, 10), 10)
    while True:
        if not luhn_algo(bank_identification_number + account_identifier):
            account_identifier = random.sample(range(0, 10), 10)
        else:
            card_number = bank_identification_number + account_identifier
            break
    for numbers in card_number:
        ac += str(numbers)
    return ac


def generate_pin_number():
    pin_ = ''
    pin_random = random.sample(range(9), 4)
    for pins in pin_random:
        pin_ += str(pins)
    return pin_


class BankSystem:
    def __init__(self):
        self.credit_card = {}

    def main(self):
        while True:
            print('1. Create account')
            print('2. Log into account')
            print('0. Exit')
            choice_menu_1 = input()
            if choice_menu_1 == '1':
                card_no = generate_card_number()
                pin_no = generate_pin_number()
                self.credit_card[card_no] = pin_no
                print('Your card has been created')
                print('Your card number:')
                print(card_no)
                print('Your card PIN:')
                print(pin_no)
            if choice_menu_1 == '2':
                card = input('Enter your card number:')
                pin = input('Enter your PIN:')
                if (card, pin) in self.credit_card.items():
                    print('You have successfully logged in!')
                    while True:
                        print('1.Balance')
                        print('2.Log out')
                        print('0.Exit')
                        menu_choice_2 = input()
                        if menu_choice_2 == '1':
                            print('Balance: 0')
                        if menu_choice_2 == '2':
                            print('You have successfully logged out!')
                            break
                        if menu_choice_2 == '0':
                            print('Bye!')
                            exit()
                else:
                    print('Wrong card number or PIN!')
            if choice_menu_1 == '0':
                print('Bye!')
                break


bs = BankSystem()
bs.main()

