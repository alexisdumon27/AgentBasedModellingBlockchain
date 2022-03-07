import pandas as pd
import pandas_ta as ta
from datetime import datetime
"""
    This file is meant to be run once the raw data files from https://www.cryptoarchive.com.au/downloads
    and from yahoo.com have been downloaded and placed into the rawCSVs folder. Its purpose is to clean and merge
    all the datafiles into one useful .csv file which can be downloaded into a pandas dataframe and accessed easily 
    during the simulation.
"""

# READS THE DOWLOADED FILES INTO PANDAS DATAFRAMES
bnb_btc = pd.read_csv('./rawCSVs/BNBBTC.csv', sep = "|", index_col=False, names = ['timestamp', 'open', 'high', 'low', 'BNB/BTC', 'volume'])
bnb_eth = pd.read_csv('./rawCSVs/BNBETH.csv', sep = "|", index_col=False, names = ['timestamp', 'open', 'high', 'low', 'BNB/ETH', 'volume'])
bnb_usdt = pd.read_csv('./rawCSVs/BNBUSDT.csv', sep = "|", index_col=False, names = ['timestamp', 'open', 'high', 'low', 'BNB/USDT', 'volume'])
btc_usdt = pd.read_csv('./rawCSVs/BTCUSDT.csv', sep = "|", index_col=False, names = ['timestamp', 'open', 'high', 'low', 'BTC/USDT', 'volume'])
eth_btc = pd.read_csv('./rawCSVs/ETHBTC.csv', sep = "|", index_col=False, names = ['timestamp', 'open', 'high', 'low', 'ETH/BTC', 'volume'])
eth_usdt = pd.read_csv('./rawCSVs/ETHUSDT.csv', sep = "|", index_col=False, names = ['timestamp', 'open', 'high', 'low', 'ETH/USDT', 'volume'])

# SETS THE TIME FRAME FOR THE DATA
jan_1st_2020_00h_00m_00s_UNIX = 1577836800
dec_31st_2021_23h_59m_00s_UNIX = 1640995140

# REMOVES UNECESSARY ATTRIBUTES, KEEPS ONLY ROWS IN TIME FRAME and ADDS REVERSED EXCHANGE RATE
index_jan_1st_2020 = bnb_btc.index[bnb_btc['timestamp'] == jan_1st_2020_00h_00m_00s_UNIX].tolist()[0]
index_dec_31st_2021 = bnb_btc.index[bnb_btc['timestamp'] == dec_31st_2021_23h_59m_00s_UNIX].tolist()[0]
bnb_btc = bnb_btc[index_jan_1st_2020:index_dec_31st_2021 + 1].drop(columns = ['open', 'high', 'low', 'volume'])
bnb_btc['BTC/BNB'] = 1 / bnb_btc['BNB/BTC']

index_jan_1st_2020 = bnb_eth.index[bnb_eth['timestamp'] == jan_1st_2020_00h_00m_00s_UNIX].tolist()[0]
index_dec_31st_2021 = bnb_eth.index[bnb_eth['timestamp'] == dec_31st_2021_23h_59m_00s_UNIX].tolist()[0]
bnb_eth = bnb_eth[index_jan_1st_2020:index_dec_31st_2021 + 1].drop(columns = ['open', 'high', 'low', 'volume'])
bnb_eth['ETH/BNB'] = 1 / bnb_eth['BNB/ETH']

index_jan_1st_2020 = bnb_usdt.index[bnb_usdt['timestamp'] == jan_1st_2020_00h_00m_00s_UNIX].tolist()[0]
index_dec_31st_2021 = bnb_usdt.index[bnb_usdt['timestamp'] == dec_31st_2021_23h_59m_00s_UNIX].tolist()[0]
bnb_usdt = bnb_usdt[index_jan_1st_2020:index_dec_31st_2021 + 1].drop(columns = ['open', 'high', 'low', 'volume'])
bnb_usdt['USDT/BNB'] = 1 / bnb_usdt['BNB/USDT']

index_jan_1st_2020 = btc_usdt.index[btc_usdt['timestamp'] == jan_1st_2020_00h_00m_00s_UNIX].tolist()[0]
index_dec_31st_2021 = btc_usdt.index[btc_usdt['timestamp'] == dec_31st_2021_23h_59m_00s_UNIX].tolist()[0]
btc_usdt = btc_usdt[index_jan_1st_2020:index_dec_31st_2021 + 1].drop(columns = ['open', 'high', 'low', 'volume'])
btc_usdt['USDT/BTC'] = 1 / btc_usdt['BTC/USDT']

index_jan_1st_2020 = eth_btc.index[eth_btc['timestamp'] == jan_1st_2020_00h_00m_00s_UNIX].tolist()[0]
index_dec_31st_2021 = eth_btc.index[eth_btc['timestamp'] == dec_31st_2021_23h_59m_00s_UNIX].tolist()[0]
eth_btc = eth_btc[index_jan_1st_2020:index_dec_31st_2021 + 1].drop(columns = ['open', 'high', 'low', 'volume'])
eth_btc['BTC/ETH'] = 1 / eth_btc['ETH/BTC']

index_jan_1st_2020 = eth_usdt.index[eth_usdt['timestamp'] == jan_1st_2020_00h_00m_00s_UNIX].tolist()[0]
index_dec_31st_2021 = eth_usdt.index[eth_usdt['timestamp'] == dec_31st_2021_23h_59m_00s_UNIX].tolist()[0]
eth_usdt = eth_usdt[index_jan_1st_2020:index_dec_31st_2021 + 1].drop(columns = ['open', 'high', 'low', 'volume'])
eth_usdt['USDT/ETH'] = 1 / eth_usdt['ETH/USDT']

# MERGES ALL THE DATA FRAMES INTO ONE
exchange_rates_df_no_usd_no_math = bnb_btc.merge(bnb_eth, how = 'outer', on = 'timestamp')
exchange_rates_df_no_usd_no_math = exchange_rates_df_no_usd_no_math.merge(bnb_usdt, how = 'outer', on = 'timestamp')
exchange_rates_df_no_usd_no_math = exchange_rates_df_no_usd_no_math.merge(btc_usdt, how = 'outer', on = 'timestamp')
exchange_rates_df_no_usd_no_math = exchange_rates_df_no_usd_no_math.merge(eth_usdt, how = 'outer', on = 'timestamp')
exchange_rates_df_no_usd_no_math = exchange_rates_df_no_usd_no_math.merge(eth_btc, how = 'outer', on = 'timestamp')

# DOES ALL THE CALCULATIONS - EMAs and RSI
exchange_rates_df_no_usd_no_math.drop(exchange_rates_df_no_usd_no_math.columns[exchange_rates_df_no_usd_no_math.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
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

    exchange_rates_df_no_usd_no_math[column_name_0] = exchange_rates_df_no_usd_no_math[symbol].ewm(span=_9_days_in_min, adjust=False).mean()
    exchange_rates_df_no_usd_no_math[column_name_1] = exchange_rates_df_no_usd_no_math[symbol].ewm(span=_12_days_in_min, adjust=False).mean()
    exchange_rates_df_no_usd_no_math[column_name_2] = exchange_rates_df_no_usd_no_math[symbol].ewm(span=_26_days_in_min, adjust=False).mean()
    exchange_rates_df_no_usd_no_math[column_name_3] = exchange_rates_df_no_usd_no_math.ta.rsi(close=symbol, length = _14_days_in_min, append = False)

exchange_rates_df_no_usd_no_math.reset_index(drop = True, inplace=True)
exchange_rates_df_no_usd_no_math.rename(columns={'timestamp':'date'}, inplace = True)
exchange_rates_df_no_usd_no_math['date'] = pd.to_datetime(exchange_rates_df_no_usd_no_math['date'],unit='s')

exchange_rates_df_no_usd = exchange_rates_df_no_usd_no_math

# READS THE BTC/USD DATA
btc_usd_daily = pd.read_csv('rawCSVs/BTC-USD.csv', index_col=0)

# CLEANS THE BTC/USD DATA BY REMOVING COLUMNS and KEEPS AVERAGE OF HIGH AND LOW AS DAILY VALUE
btc_usd_daily = btc_usd_daily.drop(columns = ["Open", "Close", 'Adj Close', 'Volume'])
btc_usd_daily['BTC/USD'] = (btc_usd_daily['High'] + btc_usd_daily['Low']) / 2
btc_usd_daily = btc_usd_daily.drop(columns = ["High", 'Low'])

# MERGES BTC/USD DATAFRAME WITH THE EXCHANGE RATES DATAFRAME
exchange_rates_df_no_usd["Date"] = pd.to_datetime(exchange_rates_df_no_usd['date']).dt.floor('d').astype(str)
exchange_rate_with_btc_usd = exchange_rates_df_no_usd.merge(btc_usd_daily, how = "outer", on = "Date")
exchange_rate_with_btc_usd = exchange_rate_with_btc_usd.drop(columns=['Date'])

# ADDS THE EXCHANGE TO USD FOR THE OTHER 3 CRYPTOS
list_of_symbols = ['BTC/BNB', 'BTC/USDT', 'BTC/ETH']
exchange_rate_with_btc_usd['ETH/USD'] =  exchange_rate_with_btc_usd['BTC/USD'] / exchange_rate_with_btc_usd['BTC/ETH']
exchange_rate_with_btc_usd['USDT/USD'] = exchange_rate_with_btc_usd['BTC/USD'] / exchange_rate_with_btc_usd['BTC/USDT'] 
exchange_rate_with_btc_usd['BNB/USD'] =  exchange_rate_with_btc_usd['BTC/USD'] / exchange_rate_with_btc_usd['BTC/BNB']

# SAVES THE FILE
exchange_rate_with_btc_usd.to_csv("exchange_rates.csv")