import pandas as pd
import matplotlib.pyplot as plt

"""
    This script is used to visualise the data before the simulation is run
"""

exchange_rates = pd.read_csv('exchange_rates.csv')

fig = plt.figure()

symbols = ["ETH/USDT", "USDT/ETH",
            "ETH/BNB", "BNB/ETH",
            "ETH/BTC" , "BTC/ETH",
            "BNB/BTC", "BTC/BNB",
            "BNB/USDT", "USDT/BNB",
            "BTC/USDT", "USDT/BTC"]

###### Overall Percent change - ENTIRE
for i in range(12):
    old = exchange_rates[symbols[i]].iloc[0]
    new = exchange_rates[symbols[i]].iloc[-1]
    percent_change = ((new - old) / old) * 100
    print (i,") ", symbols[i], ": ", percent_change, "%", ", old:", old, ", new:", new) 

### Difference between min and max - ENTIRE
for i in range(12):
    data = exchange_rates[symbols[i]]
    min_index = data.idxmin()
    max_index = data.idxmax()
    new_index = 0
    old_index = 0

    if min_index < max_index:
        old_index = min_index
        new_index = max_index
    else:
        old_index = max_index
        new_index = min_index
    diff = data.iloc[new_index] - data.iloc[old_index]
    percent_change = ((data.iloc[new_index] - data.iloc[old_index]) / data.iloc[old_index]) * 100
    print (i,") ", symbols[i], ": ", percent_change)

### maximum MIN-MAX Difference - ENTIRE
for i in range(12):
    a = exchange_rates[symbols[i]]
    vmin = a[0]
    dmax = 0
    min_index = 0
    max_index = 0
    for j in range(len(a)):
        if (a[j] < vmin):
            vmin = a[j]
        elif (a[j] - vmin > dmax):
            min_index = vmin
            max_index = j
            dmax = a[j] - vmin
            percentage_change = (dmax / vmin) * 100
    print(i,") ", symbols[i], ": ", percentage_change)

###### number of Positive Hours - ENTIRE
for i in range(12):
    data = exchange_rates[symbols[i]]
    total = 0
    for j in range(len(data)):
        if j + 1 == len(data):
            break
        if data.iloc[j] < data.iloc[j+1]:
            total += 1
    print(i,") ", symbols[i], ": ", total, ", length: ", len(data))

#### Standard Deviation - ENTIRE
for i in range(12):
    # normalise
    data = exchange_rates[symbols[i]]
    norm = (data - data.mean()) / (data.max() - data.min())
    std_dev = norm.std()
    print (i,") ", symbols[i], ": ", std_dev) 

### maximum MIN-MAX Difference First Two WEEKS
for i in range(12):
    new_index = exchange_rates.index[exchange_rates['date'] == "2021-01-14 23:52:00"].tolist()
    a = exchange_rates[symbols[i]].iloc[0:new_index[0]]
    vmin = a[0]
    dmax = 0
    for j in range(len(a)):
        if (a[j] < vmin):
            vmin = a[j]
        elif (a[j] - vmin > dmax):
            dmax = a[j] - vmin
            percentage_change = (dmax / vmin) * 100
    print(i,") ", symbols[i], ": ", percentage_change, "diff: ", dmax)

###### Percent change - TWO WEEKS
for i in range(12):
    old = exchange_rates[symbols[i]].iloc[0]
    new_index = exchange_rates.index[exchange_rates['date'] == "2021-01-14 23:00:00"].tolist()
    new = exchange_rates[symbols[i]].iloc[new_index[0]]
    percent_change = ((new - old) / old) * 100
    print (i,") ", symbols[i], ": ", percent_change, "%", ", old:", old, ", new:", new) 

###### number of positive hours - TWO WEEKS
for i in range(12):
    end_index = exchange_rates.index[exchange_rates['date'] == "2021-01-14 23:52:00"].tolist()
    data = exchange_rates[symbols[i]].iloc[0:end_index[0]]
    total = 0
    for j in range(len(data)):
        if j + 1 == len(data):
            break
        if data.iloc[j] < data.iloc[j+1]:
            total += 1
    print(i,") ", symbols[i], ": ", total, ", length: ", len(data))

### Difference between min and max - TWO WEEKS
for i in range(12):
    end_index = exchange_rates.index[exchange_rates['date'] == "2021-01-14 23:52:00"].tolist()
    data = exchange_rates[symbols[i]].iloc[0:end_index[0]]
    min_index = data.idxmin()
    max_index = data.idxmax()
    new_index = 0
    old_index = 0

    if min_index < max_index:
        old_index = min_index
        new_index = max_index
    else:
        old_index = max_index
        new_index = min_index
    percent_change = ((data.iloc[new_index] - data.iloc[old_index]) / data.iloc[old_index]) * 100
    print (i,") ", symbols[i], ": ", percent_change, "%")

#### Standard deviation - TWO WEEKS
# for i in range(12):
#     # normalise
#     new_index = exchange_rates.index[exchange_rates['date'] == "2021-01-14 23:52:00"].tolist()
#     data = exchange_rates[symbols[i]].iloc[0:new_index[0]]
#     norm = (data - data.mean()) / (data.max() - data.min())
#     std_dev = norm.std()
#     print (i,") ", symbols[i], ": ", std_dev) 

###### X / US Dollar graph
# _25_tick = round(exchange_rates.shape[0] * 0.25),
# _50_tick = round(exchange_rates.shape[0] * 0.5),
# _75_tick = round(exchange_rates.shape[0] * 0.75),
# plt.xticks([
#         0, 
#         _25_tick[0],
#         _50_tick[0],
#         _75_tick[0],
#         exchange_rates.shape[0]
#     ],
#     [   
#         exchange_rates["date"].iloc[0].split(" ")[0],
#         exchange_rates["date"].iloc[_25_tick[0]].split(" ")[0],
#         exchange_rates["date"].iloc[_50_tick[0]].split(" ")[0],
#         exchange_rates["date"].iloc[_75_tick[0]].split(" ")[0],
#         exchange_rates["date"].iloc[-1].split(" ")[0]
#     ],
#     visible=True, rotation="horizontal")
# plt.plot(range(len(exchange_rates["date"])), exchange_rates["BNB/USD"]) 
# plt.title('BNB/USD')
# plt.xlabel("Time in Days")
# plt.ylabel("BNB/USD price level")
# plt.show()