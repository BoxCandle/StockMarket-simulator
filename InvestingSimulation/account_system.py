import json

class Account:

    not_enough_cash_error = "Not enough cash"
    user_id = 0

    def __init__(self, name, password):
        Account.user_id += 1
        self.id = Account.user_id
        self.name = name
        self.password = password
        self.cash = 0
        self.portfolio = {"owned_shares": 0,
                          "share_price": 0,
                          "value": 0}

        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")

    def save_user(self, option : int):
        acc_info = {
            "id": self.id,
            "password": self.password,
            "cash": self.cash,
            "portfolio": self.portfolio
        }

        with open("accounts.json", "r") as f:
            acc = json.load(f)

            if option == 1:
                if self.name in acc.keys():
                    if self.password != acc[self.name]["password"]:
                        raise ValueError("Wrong username or password")
                    print(acc[self.name])
                    return acc[self.name]
                raise ValueError("Username does not exist")
            elif option == 2:
                if self.name in acc.keys():
                    raise ValueError("Account already exists")
        with open("accounts.json", "w") as f:
            acc[self.name] = acc_info
            json.dump(acc, f, indent=4)


    def deposit_to_account(self, amount, user):
            user[self.name]["cash"] += amount


    def withdraw_from_account(self, amount, user):
            if user[self.name]["cash"] < amount:
                raise ValueError("Not enough cash")
            user[self.name]["cash"] -= amount


    def cash_to_shares(self, amount, market):
        shares = amount / market
        return shares

    def buy_with_cash(self,amount, ticker, user, market):
        market_shares = market[ticker]["share_price"]
        purchased_cash_in_shares = self.cash_to_shares(amount, market_shares)
        if ticker in user[self.name]["portfolio"].keys():
            user_shares = user[self.name]["portfolio"][ticker]["owned_shares"]
            user_value = user[self.name]["portfolio"][ticker]["value"]
            new_shares = user_shares + purchased_cash_in_shares
            new_value = user_value + amount
            user[self.name]["portfolio"][ticker]["value"] = new_value
            user[self.name]["portfolio"][ticker]["owned_shares"] = new_shares
        else:
            self.portfolio = {"owned_shares": purchased_cash_in_shares,
                                      "share_price" : market_shares,
                                      "value" : amount}

            user[self.name]["portfolio"][ticker] = self.portfolio

    def sell_with_cash(self, amount, ticker, user, market):
        market_shares = market[ticker]["share_price"]
        purchased_cash_in_shares = self.cash_to_shares(amount, market_shares)
        if ticker in user[self.name]["portfolio"].keys():
            user_shares = user[self.name]["portfolio"][ticker]["owned_shares"]
            user_value = user[self.name]["portfolio"][ticker]["value"]
            new_shares = user_shares - purchased_cash_in_shares
            new_value = user_value - amount
            if new_shares < 0:
                raise ValueError(Account.not_enough_cash_error)
            elif new_shares == 0:
                self.remove_stock(ticker, user)
            else:
                user[self.name]["portfolio"][ticker]["value"] = new_value
                user[self.name]["portfolio"][ticker]["owned_shares"] = new_shares

    def remove_stock(self, ticker, user):
        del user[self.name]["portfolio"][ticker]

    def buy_with_shares(self, amount, ticker, user, market):
        market_share_price = market[ticker]["share_price"]
        user_cash_balance = user[self.name]["cash"]
        user_purchased_value = market_share_price * amount
        if user_cash_balance < user_purchased_value:
            raise ValueError(Account.not_enough_cash_error)
        if ticker not in user[self.name]["portfolio"].keys():
            self.portfolio["owned_shares"] += amount
            self.portfolio["share_price"] = market_share_price
            self.portfolio["value"] = user_purchased_value
            user[self.name]["portfolio"][ticker] = self.portfolio
        else:
            user_owned_shares = user[self.name]["portfolio"][ticker]["owned_shares"]
            user_owned_value = user[self.name]["portfolio"][ticker]["value"]
            self.withdraw_from_account(user_purchased_value, user)
            user_owned_value += user_purchased_value
            user_owned_shares += amount
            user[self.name]["portfolio"][ticker]["owned_shares"] = user_owned_shares
            user[self.name]["portfolio"][ticker]["share_price"] = market_share_price
            user[self.name]["portfolio"][ticker]["value"] = user_owned_value

    def sell_with_shares(self, amount, ticker, user, market):
        market_share_price = market[ticker]["share_price"]
        user_owned_shares = user[self.name]["portfolio"][ticker]["owned_shares"]
        user_owned_value = user[self.name]["portfolio"][ticker]["value"]
        user_owned_shares -= amount
        user_owned_value -= amount * market_share_price
        user[self.name]["portfolio"][ticker]["owned_shares"] = user_owned_shares
        user[self.name]["portfolio"][ticker]["share_price"] = market_share_price
        user[self.name]["portfolio"][ticker]["value"] = user_owned_value
        if user_owned_shares == 0:
            self.remove_stock(ticker, user)

    def invest_options(self, ticker : str):
        with open("accounts.json", "r") as f1, open("stocks_data.json", "r") as f2:
            user_data = json.load(f1)
            stocks_data = json.load(f2)

            #option = int(input("1.Buy\t2.Sell"))
            option = 2
            if option == 1:
                #amount = float(input("Enter amount to invest: $"))
                buy_choice = int(input("1.Cash\t2.Shares"))
                #buy_choice = 2
                amount = 10
                if buy_choice == 1:
                    self.buy_with_cash(amount, ticker, user_data, stocks_data)
                elif buy_choice == 2:
                    self.buy_with_shares(amount, ticker, user_data, stocks_data)

            elif option == 2:
                amount = 10
                sell_choice = 2
                if sell_choice == 1:
                    self.sell_with_cash(amount, ticker, user_data, stocks_data)
                elif sell_choice == 2:
                    self.sell_with_shares(amount, ticker, user_data, stocks_data)


            with open("accounts.json", "w") as f1, open("stocks_data.json", "w") as f2:
                json.dump(user_data, f1, indent=4)
                json.dump(stocks_data, f2, indent=4)


