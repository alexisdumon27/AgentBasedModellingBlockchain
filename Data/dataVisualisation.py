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

###### Overall Percent change = ((new - old) / old) * 100
# for i in range(12):
#     old = exchange_rates[symbols[i]].iloc[0]
#     new = exchange_rates[symbols[i]].iloc[-1]
#     percent_change = ((new - old) / old) * 100
#     print (i,") ", symbols[i], ": ", percent_change, "%", ", old:", old, ", new:", new) 

### Difference between min and max (must be min left max right)
# for i in range(12):
#     data = exchange_rates[symbols[i]]
#     min_index = data.idxmin()
#     max_index = data.idxmax()
#     new_index = 0
#     old_index = 0

#     if min_index < max_index:
#         old_index = min_index
#         new_index = max_index
#     else:
#         old_index = max_index
#         new_index = min_index
#     percent_change = ((data.iloc[new_index] - data.iloc[old_index]) / data.iloc[old_index]) * 100
#     print (i,") ", symbols[i], ": ", percent_change, "%")

### maximum MIN-MAX Difference ENTIRE
# for i in range(12):
#     a = exchange_rates[symbols[i]]
#     vmin = a[0]
#     dmax = 0
#     for j in range(len(a)):
#         if (a[j] < vmin):
#             vmin = a[i]
#         elif (a[j] - vmin > dmax):
#             dmax = a[j] - vmin
#             percentage_change = (dmax / vmin) * 100
#     print(i,") ", symbols[i], ": ", percentage_change, "diff: ", dmax)

### maximum MIN-MAX Difference First Two MONTHS
for i in range(12):
    new_index = exchange_rates.index[exchange_rates['date'] == "2020-02-28 23:54:00"].tolist()
    a = exchange_rates[symbols[i]].iloc[0:new_index[0]]
    vmin = a[0]
    dmax = 0
    for j in range(len(a)):
        if (a[j] < vmin):
            vmin = a[i]
        elif (a[j] - vmin > dmax):
            dmax = a[j] - vmin
            percentage_change = (dmax / vmin) * 100
    print(i,") ", symbols[i], ": ", percentage_change, "diff: ", dmax)

###### First Two months Percent change = ((new - old) / old) * 100
# for i in range(12):
#     old = exchange_rates[symbols[i]].iloc[0]
#     # find index where date = "2020-02-28 23:54:00"
#     new_index = exchange_rates.index[exchange_rates['date'] == "2020-02-28 23:54:00"].tolist()
#     new = exchange_rates[symbols[i]].iloc[new_index[0]]
#     percent_change = ((new - old) / old) * 100
#     print (i,") ", symbols[i], ": ", percent_change, "%", ", old:", old, ", new:", new) 

### Difference between min and max (must be min left max right) FIRST TWO MONTHS
# for i in range(12):
#     end_index = exchange_rates.index[exchange_rates['date'] == "2020-02-28 23:54:00"].tolist()
#     data = exchange_rates[symbols[i]].iloc[0:end_index[0]]
#     min_index = data.idxmin()
#     max_index = data.idxmax()
#     new_index = 0
#     old_index = 0

#     if min_index < max_index:
#         old_index = min_index
#         new_index = max_index
#     else:
#         old_index = max_index
#         new_index = min_index
#     percent_change = ((data.iloc[new_index] - data.iloc[old_index]) / data.iloc[old_index]) * 100
#     print (i,") ", symbols[i], ": ", percent_change, "%")

#### Standard Deviation Entire data
# for i in range(12):
#     # normalise
#     data = exchange_rates[symbols[i]]
#     norm = (data - data.mean()) / (data.max() - data.min())
#     std_dev = norm.std()
#     print (i,") ", symbols[i], ": ", std_dev) 


#### Standard deviation first two months
# for i in range(12):
#     # normalise
#     new_index = exchange_rates.index[exchange_rates['date'] == "2020-02-28 23:54:00"].tolist()
#     data = exchange_rates[symbols[i]].iloc[0:new_index[0]]
#     norm = (data - data.mean()) / (data.max() - data.min())
#     std_dev = norm.std()
#     print (i,") ", symbols[i], ": ", std_dev) 

###### DAILY PERCENTAGE CHANGE GRAPHS ######
# for i in range(12):
#     # get daily percentage change for first month!
#     exchange = exchange_rates[symbols[i]].to_frame()[symbols[i]] * 10
#     dates = exchange_rates['date']
#     exchange = pd.merge(dates, exchange, left_index=True, right_index=True)
#     exchange_daily = exchange.iloc[:1442:24, :]
#     # for every row calculate the percentage change
#     percent_change_df = exchange_daily[symbols[i]].astype(int).pct_change(fill_method='ffill')
    
#     _25_tick = round(exchange_daily.shape[0] * 0.25),
#     _50_tick = round(exchange_daily.shape[0] * 0.5),
#     _75_tick = round(exchange_daily.shape[0] * 0.75),
#     plt.xticks([
#             0, 
#             _25_tick[0],
#             _50_tick[0],
#             _75_tick[0],
#             exchange_daily.shape[0]
#         ],
#         [   
#             exchange_daily["date"].iloc[0].split(" ")[0],
#             exchange_daily["date"].iloc[_25_tick[0]].split(" ")[0],
#             exchange_daily["date"].iloc[_50_tick[0]].split(" ")[0],
#             exchange_daily["date"].iloc[_75_tick[0]].split(" ")[0],
#             exchange_daily["date"].iloc[-1].split(" ")[0]
#         ],
#         visible=True, rotation="horizontal")
#     colors = []
#     for w in range(len(percent_change_df)):
#         if percent_change_df.iloc[w] > 0:
#             colors.append("green")
#         else: colors.append("red")
#     print (len(colors))
#     plt.bar(range(len(exchange_daily["date"])), percent_change_df, color = colors) 
#     plt.title(symbols[i])
#     plt.xlabel("Time in Days")
#     plt.ylabel(symbols[i] + " daily percent change (%) ")
#     plt.show()
    
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