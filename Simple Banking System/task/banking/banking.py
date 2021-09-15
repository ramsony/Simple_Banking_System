import sqlite3
import random


class BankSystem:
    card_count = 0

    def __init__(self, number, pin_number, bal):
        self.id_no = self.card_count + 1
        self.account_no = number
        self.pin_no = pin_number
        self.balance = bal

    @classmethod
    def luhn_algo(cls, numbers):
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

    @classmethod
    def generate_card_number(cls):
        bank_identification_number = [4, 0, 0, 0, 0, 0]
        ac = ''
        account_identifier = random.sample(range(0, 10), 10)
        while True:
            if not cls.luhn_algo(bank_identification_number + account_identifier):
                account_identifier = random.sample(range(0, 10), 10)
            else:
                card_number = bank_identification_number + account_identifier
                break
        for numbers in card_number:
            ac += str(numbers)
        return ac

    @classmethod
    def generate_pin_number(cls):
        pin_ = ''
        pin_random = random.sample(range(9), 4)
        for pins in pin_random:
            pin_ += str(pins)
        return pin_

    @classmethod
    def conn_db(cls):
        conn = sqlite3.connect('card.s3db')
        c = conn.cursor()
        return conn, c

    @classmethod
    def create_table(cls):
        conn, c = cls.conn_db()
        c.execute("""CREATE TABLE IF NOT EXISTS card(
                id INTEGER,
                number TEXT,
                pin TEXT,
                balance INTEGER)""")
        conn.commit()
        conn.close()

    @classmethod
    def insert_data(cls, id_no, account_no, pin_num, balance):
        conn, c = cls.conn_db()
        c.execute("INSERT INTO card VALUES (:id,:number,:pin,:balance)",
                  {'id': id_no, 'number': account_no, 'pin': pin_num, 'balance': balance})
        conn.commit()
        conn.close()

    @classmethod
    def select_data(cls, account_no):
        conn, c = cls.conn_db()
        c.execute("SELECT number, pin FROM card WHERE number=:number", {'number': account_no})
        data = c.fetchone()
        conn.commit()
        conn.close()
        return data


BankSystem.create_table()
while True:
    print('1. Create account')
    print('2. Log into account')
    print('0. Exit')
    choice_menu_1 = input()
    if choice_menu_1 == '1':
        bs = BankSystem(BankSystem.generate_card_number(), BankSystem.generate_pin_number(), 0)
        bs.insert_data(bs.id_no, bs.account_no, bs.pin_no, bs.balance)
        print('Your card has been created')
        select_data = bs.select_data(bs.account_no)
        print('Your card number:')
        print(select_data[0])
        print('Your card PIN:')
        print(select_data[1])
    if choice_menu_1 == '2':
        card = input('Enter your card number:')
        pin = input('Enter your PIN:')
        if card == select_data[0] and pin == select_data[1]:
            print('You have successfully logged in!')
            while True:
                print('1.Balance')
                print('2.Log out')
                print('0.Exit')
                menu_choice_2 = input()
                if menu_choice_2 == '1':
                    print(select_data[2])
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
