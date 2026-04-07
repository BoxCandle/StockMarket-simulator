from account_system import Account
from Stock_Market import Stock
import json
import time
import random


with open("accounts.json", "r") as f:
    users = json.load(f)
    users_ids = []
    try:
        for user_id in users.values():
            users_ids.append(user_id["id"])
        Account.user_id = max(users_ids)
    except: Account.user_id = 0

def enter_user_info():
    """ Function to enter user info
    It asks for username and password and stores them in user variable that turn into Account class variable
    returns account"""
    #username = input("Username: ")
    #password = input("Password: ")
    username = "Radamir"
    password = "13245678"
    user = Account(username, password)
    return user

def operate_account(account):
    """ Function to perform account operation
    so far there are 3 options: deposit, withdraw, and Exit for debug
    returns None"""
    #activity = int(input("1. Deposit\t2. Withdraw\t3. Invest\t4. Exit"))
    activity = 3 #1 deposit, 3 invest
    if activity == 1:
        #amount = float(input("Amount: $"))
        amount = 10000
        account.deposit_to_account(amount)
    elif activity == 2:
        amount = float(input("Amount: $"))
        account.withdraw_from_account(amount)
    elif activity == 3:
        with open("stocks_data.json", "r") as f:
            stocks = json.load(f)
            for stock, info in stocks.items():
                print(f'Ticker: {stock}\t{info}')

            #choice = input("Enter a ticker you want to purchase: ")
            choice = "KO"
            if choice not in stocks:
                raise ValueError("Ticker does not exist")
            account.invest_options(choice)
    elif activity == 4:
        raise SystemExit

def main():
    """ Main function
    Gives 2 options: Sign up or Sign in
    If sign in, it will check if password is correct.
    If sign up, it will make sure that username does not already exist.
    It will then add to the accounts.json file"""
    #option = int(input("1. Log in\t2. Sign up "))
    option = 1
    if option == 1:
        login = enter_user_info()
        login.save_user(option)
        operate_account(login)
    elif option == 2:
        login = enter_user_info()
        login.save_user(option)
        operate_account(login)

    with open("accounts.json", "r") as f:
        account = json.load(f)
        for a in account:
            print(f'{account[a].values()}',end='')
        return a

print(main())