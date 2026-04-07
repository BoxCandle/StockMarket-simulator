import random
import json

class Stock:

    shares = 0
    share_price = 0

    def __init__(self, ticker : str):
        Stock.shares = random.randint(100,1000)
        Stock.share_price = random.randint(10,100)
        self.ticker = ticker
        self.shares = round(float(Stock.shares), 2)
        self.share_price = Stock.share_price

    def generate_stats(self):

        stock_data = {
            "shares": self.shares,
            "share_price": self.share_price,
        }

        with open("stocks_data.json", "r") as f:
            stocks = json.load(f)
            stocks[self.ticker] = stock_data
            stocks[self.ticker]["shares"] = self.shares
            stocks[self.ticker]["share_price"] = round(self.share_price, 2)

        with open("stocks_data.json", "w") as f:
            json.dump(stocks, f, indent=4)

    def fluctuate_price(self):
        with open("stocks_data.json", "r") as f:
            stocks = json.load(f)
            percent = round(random.randint(1,100) / 100 * stocks[self.ticker]["share_price"], 2)
            stocks[self.ticker]["share_price"] += percent

        with open("stocks_data.json", "w") as f:
            json.dump(stocks, f, indent=4)

tickers = [
    "AAPL",   # Apple
    "MSFT",   # Microsoft
    "AMZN",   # Amazon
    "TSLA",   # Tesla
    "NVDA",   # NVIDIA
    "GOOGL",  # Alphabet (Google)
    "META",   # Meta
    "NFLX",   # Netflix
    "KO",     # Coca-Cola
    "MCD"     # McDonald's
]

