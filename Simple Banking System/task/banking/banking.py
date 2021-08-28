import random

account_number = []
pin_numbers = []


def card_number():
    check_sum = '2'
    iin = '400000'
    ac = ''
    customer_account_number = random.sample(range(9), 9)
    for acc in customer_account_number:
        ac += str(acc)
    account_number.append(iin + ac + check_sum)
    return iin + ac + check_sum


def pin_number():
    pin = ''
    pin_random = random.sample(range(9), 4)
    for pins in pin_random:
        pin += str(pins)
    pin_numbers.append(pin)
    return pin


while True:
    print('1. Create account')
    print('2. Log into account')
    print('0. Exit')
    choice = input()
    if choice == '1':
        print('Your card has been created')
        print('Your card number:')
        print(card_number())
        print('Your card PIN:')
        print(pin_number())
    if choice == '2':
        card_no = input('Enter your card number:')
        pin_no = input('Enter your PIN:')
        if card_no not in account_number or pin_no not in pin_numbers:
            print('Wrong card number or PIN!')
        else:
            print('You have successfully logged in!')
            check2 = True
            while check2:
                print('1.Balance')
                print('2.Log out')
                print('0.Exit')
                choice2 = input()
                if choice2 == '1':
                    print('Balance: 0')
                if choice2 == '2':
                    print('You have successfully logged out!')
                    check2 = False
                if choice2 == '0':
                    print('Bye!')
                    exit()
    if choice == '0':
        print('Bye!')
        break
