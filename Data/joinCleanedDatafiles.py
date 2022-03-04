import pandas as pd
from pandas import read_csv
import pandas_ta as ta
from datetime import datetime

bnb_btc = pd.read_csv('./cleanedDatafiles/cleaned_BNB_BTC.csv', index_col=False)
bnb_eth = pd.read_csv('./cleanedDatafiles/cleaned_BNB_ETH.csv', index_col=False)
bnb_usdt = pd.read_csv('./cleanedDatafiles/cleaned_BNB_USDT.csv',index_col=False)
btc_usdt = pd.read_csv('./cleanedDatafiles/cleaned_BTC_USDT.csv', index_col=False)
eth_btc = pd.read_csv('./cleanedDatafiles/cleaned_ETH_BTC.csv', index_col=False)
eth_usdt = pd.read_csv('./cleanedDatafiles/cleaned_ETH_USDT.csv', index_col=False)

exchange_rates_df = bnb_btc.merge(bnb_eth, how = 'outer', on = 'timestamp')
exchange_rates_df = exchange_rates_df.merge(bnb_usdt, how = 'outer', on = 'timestamp')
exchange_rates_df = exchange_rates_df.merge(btc_usdt, how = 'outer', on = 'timestamp')
exchange_rates_df = exchange_rates_df.merge(eth_usdt, how = 'outer', on = 'timestamp')
exchange_rates_df = exchange_rates_df.merge(eth_btc, how = 'outer', on = 'timestamp')

# print (exchange_rates_df)

exchange_rates_df.to_csv("./cleanedDatafiles/cleanedJoinedExchangeRates-noMath.csv")