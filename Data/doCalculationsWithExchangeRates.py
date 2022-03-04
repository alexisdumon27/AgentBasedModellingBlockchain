import pandas as pd
import pandas_ta as ta
from datetime import datetime

exchange_rates = pd.read_csv("./cleanedDatafiles/cleanedJoinedExchangeRates-noMath.csv", index_col=False)

exchange_rates.drop(exchange_rates.columns[exchange_rates.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)

list_of_symbols = ['BNB/BTC','BTC/BNB','BNB/ETH','ETH/BNB','BNB/USDT','USDT/BNB','BTC/USDT','USDT/BTC','ETH/USDT','USDT/ETH','ETH/BTC','BTC/ETH']

for symbol in list_of_symbols:
    column_name_0 = '9_ema_' + symbol
    column_name_1 = '12_ema_' + symbol
    column_name_2 = '26_ema_' + symbol

    column_name_3 = 'rsi_' + symbol

    _9_days_in_min = 9 * 24 * 60
    _12_days_in_min = 12 * 24 * 60
    _26_days_in_min = 26 * 24 * 60
    _14_days_in_min = 14 * 24 * 60

    exchange_rates[column_name_0] = exchange_rates[symbol].ewm(span=_9_days_in_min, adjust=False).mean()
    exchange_rates[column_name_1] = exchange_rates[symbol].ewm(span=_12_days_in_min, adjust=False).mean()
    exchange_rates[column_name_2] = exchange_rates[symbol].ewm(span=_26_days_in_min, adjust=False).mean()
    exchange_rates[column_name_3] = exchange_rates.ta.rsi(close=symbol, length = _14_days_in_min, append = False)

exchange_rates.reset_index(drop = True, inplace=True)
exchange_rates.rename(columns={'timestamp':'date'}, inplace = True)
exchange_rates['date'] = pd.to_datetime(exchange_rates['date'],unit='s')

# print (exchange_rates)
# print (exchange_rates.columns)
exchange_rates.to_csv('exchange_rates_no-USD.csv')

