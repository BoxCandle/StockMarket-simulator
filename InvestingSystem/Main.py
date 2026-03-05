import random
import numpy as np


class Stocks:


    def __init__(self, ticker):
        self.ticker = ticker
        self.shares_volume = 0
        self.share_price = 0.0
        self.market_cap = self.shares_volume * self.share_price
        self.portfolio = {}


    def generate_price(self):
        num = np.random.uniform(50, 100)
        self.share_price += round(num, 2)


    def generate_shares_volume(self):
        num = np.random.randint(1000, 100000)
        self.shares_volume += num


    def calculate_market_cap(self):
        self.market_cap = round(self.share_price * self.shares_volume, 2)


    def generate_stock_stats(self):
        self.generate_price()
        self.generate_shares_volume()
        self.calculate_market_cap()


    def __str__(self):
        return (f'Ticker: {self.ticker} '
                f'Share Price: ${self.share_price} '
                f'Share Volume: {self.shares_volume} '
                f'Market Capitalization: ${self.market_cap} ')


class InvestingAccount:


    def __init__(self, name):
        self.name = name
        self.cash = 0
        self.portfolio = {}


    def deposit(self, amount):
        self.cash += amount
        return f'${amount}'


    def withdraw(self, amount):
        if self.cash < amount:
            raise Exception("Insufficient funds")
        self.cash -= amount
        return f'${amount}'


def create_account():
    username = input("Enter your name: ")
    user = InvestingAccount(username)
    return user


def generate_companies():
    alphabet = [
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
        "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"
               ]
    letter_pairs = []
    tickers = []
    for i in range(5):
        letter_pairs.append(random.sample(alphabet, np.random.randint(1, 4)))
    for letter in letter_pairs:
        letter = "".join(letter)
        tickers.append(letter)
    return tickers
#find out how to rename variables and arguments when you are using the same thing lines 85-100

def generate_company_stats(company_tickers):
    stock_market = {}
    for ticker in company_tickers:
        ticker_stock = Stocks(ticker)
        ticker_stock.generate_stock_stats()
        stock_market[ticker] = ticker_stock.share_price, ticker_stock.shares_volume, ticker_stock.market_cap
    for ticker, info in stock_market.items():
        print(f'{ticker}: {info}')
    return stock_market


def operate_account(account, market):
    account.cash = 0
    while True:
        print(f'\nCurrent cash: ${account.cash}')
        operation : int = int(input("\n1. Deposit 2. Withdraw 3. Invest: 4. Discard\t"))
        if operation == 1:
            deposit_amount : float = float(input("\nEnter deposit amount: $"))
            account.deposit(deposit_amount)
        elif operation == 2 and account.cash > 0:
            withdraw_amount : float = float(input("\nEnter withdraw amount: $"))
            if account.cash < withdraw_amount:
                return ValueError("Insufficient funds")
            account.withdraw(withdraw_amount)
        elif operation == 3:
            ticker: str = input("\nSearch up ticker:\t")
            if ticker not in market:
                return ValueError("Stock is not found")
            print(f'{ticker}: {market[ticker]}')
            buy_option = input("\nBuy with: Cash/Stock\t")
            if buy_option == "Cash":
                cash_amount = float(input("\nEnter cash amount:\t$"))
                if cash_amount > account.cash:
                    print("\nNot enough cash")
                account.cash -= cash_amount
                owned_company_shares = account.portfolio[ticker] = cash_amount / market[ticker][0]
                account.portfolio[ticker] = round(owned_company_shares, 2), cash_amount
                print(f'{account.portfolio}')
        elif operation == 4:
            print(f'Account: {account.name}\n'
                  f'Cash: ${account.cash}\n'
                  f'\nStock Portfolio\n')
            for company, info in account.portfolio.items():
                print(f'{company} : {info[0]} Shares, Value: ${info[1]} ')
            break
    account.portfolio["Cash"] = f'${account.cash}'
    return account.portfolio


def main():
    operate_account(create_account(), generate_company_stats(generate_companies()))

main()