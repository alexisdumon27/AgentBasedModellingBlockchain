from turtle import color
from matplotlib import markers
import pandas as pd
import matplotlib.pyplot as plt

exchange_rates = pd.read_csv('exchange_rates.csv')

# print (exchange_rates)

"""
    12 graphs of different exchange rates over time
"""
fig = plt.figure()

symbols = ["ETH/USDT", "USDT/ETH",
            "ETH/BNB", "BNB/ETH",
            "ETH/BTC" , "BTC/ETH",
            "BNB/BTC", "BTC/BNB",
            "BNB/USDT", "USDT/BNB",
            "BTC/USDT", "USDT/BTC"
        ]

###### DAILY PERCENTAGE CHANGE GRAPHS ######

for i in range(12):
    print ("NEW SYMBOL!!!")
    # get daily percentage change for first month!
    exchange = exchange_rates[symbols[i]].to_frame()[symbols[i]] * 10
    print (exchange)
    dates = exchange_rates['date']
    exchange = pd.merge(dates, exchange, left_index=True, right_index=True)
    exchange_daily = exchange.iloc[:1442:24, :]
    # for every row calculate the percentage change
    percent_change_df = exchange_daily[symbols[i]].astype(int).pct_change(fill_method='ffill')
    print (percent_change_df)
    
    _25_tick = round(exchange_daily.shape[0] * 0.25),
    _50_tick = round(exchange_daily.shape[0] * 0.5),
    _75_tick = round(exchange_daily.shape[0] * 0.75),
    # print (_25_tick[0], ", ", _50_tick[0], ", ", _75_tick[0])
    plt.xticks([
            0, 
            _25_tick[0],
            _50_tick[0],
            _75_tick[0],
            exchange_daily.shape[0]
        ],
        [   
            exchange_daily["date"].iloc[0].split(" ")[0],
            exchange_daily["date"].iloc[_25_tick[0]].split(" ")[0],
            exchange_daily["date"].iloc[_50_tick[0]].split(" ")[0],
            exchange_daily["date"].iloc[_75_tick[0]].split(" ")[0],
            exchange_daily["date"].iloc[-1].split(" ")[0]
        ],
        visible=True, rotation="horizontal")
    colors = []
    for w in range(len(percent_change_df)):
        if percent_change_df.iloc[w] > 0:
            colors.append("green")
        else: colors.append("red")
    print (len(colors))
    plt.bar(range(len(exchange_daily["date"])), percent_change_df, color = colors) 
    plt.title(symbols[i])
    plt.xlabel("Time in Days")
    plt.ylabel(symbols[i] + " daily percent change (%) ")
    plt.show()
    




###### LONG TIME FRAME DIAGRAMS ########
# for i in range(1, 13):
#     plt.locator_params(axis='y', nbins=5)
#     _25_tick = round(exchange_rates.shape[0] * 0.25),
#     _50_tick = round(exchange_rates.shape[0] * 0.5),
#     _75_tick = round(exchange_rates.shape[0] * 0.75),
#     print (_25_tick[0], ", ", _50_tick[0], ", ", _75_tick[0])
#     plt.xticks([
#             0, 
#             _25_tick[0],
#             _50_tick[0],
#             _75_tick[0],
#             exchange_rates.shape[0]
#         ],
#         [   
#             exchange_rates["date"].iloc[0].split(" ")[0],
#             exchange_rates["date"].iloc[_25_tick[0]].split(" ")[0],
#             exchange_rates["date"].iloc[_50_tick[0]].split(" ")[0],
#             exchange_rates["date"].iloc[_75_tick[0]].split(" ")[0],
#             exchange_rates["date"].iloc[-1].split(" ")[0]
#         ],
#         visible=True, rotation="horizontal")
#     plt.plot(range(len(exchange_rates["date"])), exchange_rates[symbols[i - 1]]) 
#     plt.title(symbols[i - 1])
#     plt.xlabel("Time in Days")
#     plt.ylabel(symbols[i - 1] + " price level ")
#     plt.show()

##### SHORT TIME FRAME DIAGRAMS (DAYLY) ###########
# show 27 September 2021 --> 15205 to 15229 (24 ticks)
# one_day = 24 # 1 day of data
# start = 15205
# end = 15229
# for i in range(12):
#     # plt.locator_params(axis='y', nbins=5)
#     plt.xticks(range(0, 25, 4),
#         [   
#             exchange_rates["date"].iloc[start].split(" ")[1].split(":")[0] + "h00",
#             exchange_rates["date"].iloc[start + 4].split(" ")[1].split(":")[0] + "h00",
#             exchange_rates["date"].iloc[start + 8].split(" ")[1].split(":")[0] + "h00",
#             exchange_rates["date"].iloc[start + 12].split(" ")[1].split(":")[0] + "h00",
#             exchange_rates["date"].iloc[start + 16].split(" ")[1].split(":")[0] + "h00",
#             exchange_rates["date"].iloc[start + 20].split(" ")[1].split(":")[0] + "h00",
#             "24h00",
#         ],
#         visible=True, rotation="horizontal")
#     print (symbols[i])
#     print ("MIN")
#     print(exchange_rates[symbols[i]].iloc[15205:15229].min())
#     print(exchange_rates.iloc[exchange_rates[symbols[i]].iloc[15205:15229].idxmin()]['date'])
#     print ("MAX")
#     print(exchange_rates[symbols[i]].iloc[15205:15229].max())
#     print(exchange_rates.iloc[exchange_rates[symbols[i]].iloc[15205:15229].idxmax()]['date'])

#     plt.plot(range(one_day), exchange_rates[symbols[i]].iloc[15205:15229], marker='.') 
#     plt.title(symbols[i] + " Daily")
#     plt.xlabel("Time in Days from 27/09/21 to 28/09/21")
#     plt.ylabel(symbols[i] + " price level ")
#     plt.show()