import pandas as pd

btc_usd_daily = pd.read_csv('./cleanedDatafiles/cleanedBTCUSD.csv')
exchange_rate_no_usd = pd.read_csv('exchange_rates_no-USD.csv', index_col=0)

exchange_rate_no_usd["Date"] = pd.to_datetime(exchange_rate_no_usd['date']).dt.floor('d').astype(str)

# btc_usd_daily.Date.astype('datetime64[ns]')
exchange_rate_with_btc_usd = exchange_rate_no_usd.merge(btc_usd_daily, how = "outer", on = "Date")

exchange_rate_with_btc_usd = exchange_rate_with_btc_usd.drop(columns=['Date'])

# add symbol / USD values

list_of_symbols = ['BTC/BNB', 'BTC/USDT', 'BTC/ETH']

# print (exchange_rate_with_btc_usd['BTC/ETH'])
# print (exchange_rate_with_btc_usd['BTC/USDT'])
# print (exchange_rate_with_btc_usd['BTC/BNB'])

exchange_rate_with_btc_usd['ETH/USD'] =  exchange_rate_with_btc_usd['BTC/USD'] / exchange_rate_with_btc_usd['BTC/ETH']
exchange_rate_with_btc_usd['USDT/USD'] = exchange_rate_with_btc_usd['BTC/USD'] / exchange_rate_with_btc_usd['BTC/USDT'] 
exchange_rate_with_btc_usd['BNB/USD'] =  exchange_rate_with_btc_usd['BTC/USD'] / exchange_rate_with_btc_usd['BTC/BNB']

# print (exchange_rate_with_btc_usd['ETH/USD'])
# print (exchange_rate_with_btc_usd['USDT/USD'])
# print (exchange_rate_with_btc_usd['BNB/USD'])

print (exchange_rate_with_btc_usd)
print (exchange_rate_with_btc_usd.shape)
print (exchange_rate_with_btc_usd.columns)
exchange_rate_with_btc_usd.to_csv("exchange_rates.csv")

