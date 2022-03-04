import pandas as pd

bnb_btc = pd.read_csv('./rawCSVs/BNBBTC.csv', sep = "|", index_col=False, names = ['timestamp', 'open', 'high', 'low', 'BNB/BTC', 'volume'])
bnb_eth = pd.read_csv('./rawCSVs/BNBETH.csv', sep = "|", index_col=False, names = ['timestamp', 'open', 'high', 'low', 'BNB/ETH', 'volume'])
bnb_usdt = pd.read_csv('./rawCSVs/BNBUSDT.csv', sep = "|", index_col=False, names = ['timestamp', 'open', 'high', 'low', 'BNB/USDT', 'volume'])
btc_usdt = pd.read_csv('./rawCSVs/BTCUSDT.csv', sep = "|", index_col=False, names = ['timestamp', 'open', 'high', 'low', 'BTC/USDT', 'volume'])
eth_btc = pd.read_csv('./rawCSVs/ETHBTC.csv', sep = "|", index_col=False, names = ['timestamp', 'open', 'high', 'low', 'ETH/BTC', 'volume'])
eth_usdt = pd.read_csv('./rawCSVs/ETHUSDT.csv', sep = "|", index_col=False, names = ['timestamp', 'open', 'high', 'low', 'ETH/USDT', 'volume'])

jan_1st_2020_00h_00m_00s_UNIX = 1577836800
dec_31st_2021_23h_59m_00s_UNIX = 1640995140 # since per min data

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

# print (bnb_usdt)
# print (bnb_btc)
# print (bnb_eth)
# print (eth_btc)
# print (eth_usdt)
# print (btc_usdt)

bnb_usdt.to_csv("./cleanedDatafiles/cleaned_BNB_USDT.csv", index = False)
bnb_btc.to_csv("./cleanedDatafiles/cleaned_BNB_BTC.csv", index = False)
bnb_eth.to_csv("./cleanedDatafiles/cleaned_BNB_ETH.csv", index = False)
eth_btc.to_csv("./cleanedDatafiles/cleaned_ETH_BTC.csv", index = False)
eth_usdt.to_csv("./cleanedDatafiles/cleaned_ETH_USDT.csv", index = False)
btc_usdt.to_csv("./cleanedDatafiles/cleaned_BTC_USDT.csv", index = False)

