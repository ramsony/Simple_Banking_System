import sqlite3
import random


def generate_pin_number():
    pin_ = ''
    pin_random = random.sample(range(9), 4)
    for pins in pin_random:
        pin_ += str(pins)
    return pin_


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


def conn_cur():
    conn = sqlite3.connect('card.s3db')
    c = conn.cursor()
    return c, conn


def create_table():
    c, conn = conn_cur()
    c.execute("""CREATE TABLE IF NOT EXISTS card(
            id INTEGER PRIMARY KEY,
            number TEXT,
            pin TEXT,
            balance INTEGER)""")
    conn.commit()
    conn.close()


def insert_data(b_s):
    c, conn = conn_cur()
    c.execute("INSERT INTO card VALUES (:id,:number,:pin,:balance)",
              {'id': b_s.id, 'number': b_s.account_no, 'pin': b_s.pin_no, 'balance': b_s.balance})
    conn.commit()
    conn.close()


def get_balance(card_number):
    c, conn = conn_cur()
    c.execute("SELECT balance FROM card WHERE number=:number",
              {'number': card_number})
    data = c.fetchall()
    return int(data[0][0])


def find_ac_no(pin_number, card_number):
    c, conn = conn_cur()
    c.execute("SELECT number, pin FROM card WHERE number=:number AND pin=:pin",
              {'number': card_number, 'pin': pin_number})
    return c.fetchone()


def find_card_no(card_number):
    c, conn = conn_cur()
    c.execute("SELECT number FROM card WHERE number=:number",
              {'number': card_number})
    return c.fetchone()


def add_income(amount, num):
    c, conn = conn_cur()
    c.execute("UPDATE card SET balance=:balance WHERE number=:number", {'balance': amount, 'number': num})
    conn.commit()
    conn.close()


def drop_table():
    c, conn = conn_cur()
    c.execute("DROP TABLE card")
    conn.commit()
    conn.close()


def do_transfer(cd):
    print('Transfer')
    bal = get_balance(cd)
    transfer_to_no = input('Enter card number:')
    if not luhn_algo([int(x) for x in transfer_to_no]):
        print('Probably you made a mistake in the card number. Please try again!')
    elif find_card_no(transfer_to_no) is None or transfer_to_no not in find_card_no(transfer_to_no):
        print('Such a card does not exist.')
    elif transfer_to_no == cd:
        print("You can't transfer money to the same account!")
    else:
        money_transfer = int(input('Enter how much money you want to transfer:'))
        if money_transfer > bal:
            print('Not enough money!')
        else:
            add_income(bal - money_transfer, cd)
            add_income(money_transfer, transfer_to_no)
            print('Success!')


def close_account(num):
    c, conn = conn_cur()
    c.execute("DELETE FROM card where number=:number", {'number': num})
    conn.commit()
    conn.close()
    print('The account has been closed!')


class BankSystem:
    id_card = 0

    def __init__(self, i_d, number, pin_number, bal):
        self.id = i_d
        self.account_no = number
        self.pin_no = pin_number
        self.balance = bal


drop_table()
create_table()
while True:

    print('1. Create account')
    print('2. Log into account')
    print('0. Exit')
    choice_menu_1 = input()
    if choice_menu_1 == '1':
        BankSystem.id_card += 1
        bs = BankSystem(BankSystem.id_card, generate_card_number(), generate_pin_number(), 0)
        insert_data(bs)
        print('Your card has been created')
        print('Your card number:')
        print(bs.account_no)
        print('Your card PIN:')
        print(bs.pin_no)
    if choice_menu_1 == '2':
        card = input('Enter your card number:')
        pin = input('Enter your PIN:')
        if find_ac_no(pin, card) is not None:
            print('You have successfully logged in!')
            while True:
                print('1.Balance')
                print('2.Add income')
                print('3.Do transfer')
                print('4.Close account')
                print('5.Log out')
                print('0.Exit')
                menu_choice_2 = input()
                if menu_choice_2 == '1':
                    print("Balance:", get_balance(card))
                if menu_choice_2 == '2':
                    in_amount = int(input('Enter income:'))
                    added_amount = in_amount + get_balance(card)
                    add_income(added_amount, card)
                    print('Income was added!')
                if menu_choice_2 == '3':
                    do_transfer(card)
                if menu_choice_2 == '4':
                    close_account(card)
                    break
                if menu_choice_2 == '5':
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
