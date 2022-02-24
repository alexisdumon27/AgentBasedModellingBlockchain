"""
    goal of this file is to save a .csv containing the exchange_rates for all the possible currency pairs in the market in a
    DataFrame style table
    as a starter the only two currencies are Ethereum and Tether
    therefore : USDT/ETH and ETH/USDT

    USD / ETH --> how many USD per 1 ETH

"""

import numpy
import math
import csv
import pandas as pd
from pandas import read_csv
import sys
from datetime import datetime


ethereumData = pd.read_csv('cleanedEuthereumData.csv', index_col=False)
tetherData = pd.read_csv('cleanedTetherData.csv', index_col=False)

print (ethereumData)
print (tetherData)

""" join on date attribute --> index | Date | USDT/ETH | ETH/USDT """

exchange_rates_df = tetherData.merge(ethereumData, how = 'outer', on = 'Date' )

# create new column which is USDT / ETH

exchange_rates_df['USDT/ETH'] = exchange_rates_df['USD/USDT'] / exchange_rates_df['USD/ETH']

# create a new column which is ETH / USDT

exchange_rates_df['ETH/USDT'] = exchange_rates_df['USD/ETH'] / exchange_rates_df['USD/USDT']

# print (exchange_rates_df)

exchange_rates_df['5_ema_USDT/ETH'] = exchange_rates_df['USDT/ETH'].ewm(span=5, adjust=False).mean()
exchange_rates_df['10_ema_USDT/ETH'] = exchange_rates_df['USDT/ETH'].ewm(span=10, adjust=False).mean()
exchange_rates_df['15_ema_USDT/ETH'] = exchange_rates_df['USDT/ETH'].ewm(span=15, adjust=False).mean()
exchange_rates_df['50_ema_USDT/ETH'] = exchange_rates_df['USDT/ETH'].ewm(span=50, adjust=False).mean()

exchange_rates_df['5_ema_ETH/USDT'] = exchange_rates_df['ETH/USDT'].ewm(span=5, adjust=False).mean()
exchange_rates_df['10_ema_ETH/USDT'] = exchange_rates_df['ETH/USDT'].ewm(span=10, adjust=False).mean()
exchange_rates_df['15_ema_ETH/USDT'] = exchange_rates_df['ETH/USDT'].ewm(span=15, adjust=False).mean()
exchange_rates_df['50_ema_ETH/USDT'] = exchange_rates_df['ETH/USDT'].ewm(span=50, adjust=False).mean()

# print (exchange_rates_df)
exchange_rates_df.to_csv('exchange_rates.csv')

