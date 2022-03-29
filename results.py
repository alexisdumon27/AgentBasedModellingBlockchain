import pandas as pd
import matplotlib.pyplot as plt

"""
For today:

    - transaction_dates data seems to be wrong
    - run number of orders per strategy per currency pairs
    - wealthiest agents <-- extract more information
    - most successful risk level
    - diagrams still look like shite from server.py

"""
data = pd.read_csv('smallModelResults.csv')

exchange_rates = pd.read_csv('Data/exchange_rates.csv')

last_row_only = data.iloc[-1]

# GET the TRANSACTION DATES:
"""
transaction_dates_ETH/USDT:USDT/ETH,
transaction_dates_ETH/BNB:BNB/ETH,
transaction_dates_ETH/BTC:BTC/ETH,
transaction_dates_BNB/BTC:BTC/BNB,
transaction_dates_BNB/USDT:USDT/BNB,
transaction_dates_BTC/USDT:USDT/BTC
"""

"""
    make a scatter plot showing when the transactions occurred
"""


print(data['transaction_dates_ETH/USDT:USDT/ETH']) # what the fuck was I appending?

print(len(exchange_rates['ETH/USDT']))




print (last_row_only)
