from cProfile import label
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
data = pd.read_csv('simulation_results.csv')

exchange_rates = pd.read_csv('Data/exchange_rates.csv')

corresponding_symbols = [
    "ETH/USDT:USDT/ETH", "ETH/BNB:BNB/ETH", "ETH/BTC:BTC/ETH", "BNB/BTC:BTC/BNB", "BNB/USDT:USDT/BNB", "BTC/USDT:USDT/BTC"
]

symbols = [
    "ETH/USDT",
    "ETH/BNB" ,
    "ETH/BTC",
    "BNB/BTC" ,
    "BNB/USDT",
    "BTC/USDT",
    "USDT/ETH",
    "BNB/ETH" ,
    "BTC/ETH" ,
    "BTC/BNB" ,
    "USDT/BNB",
    "USDT/BTC",
]

strategies = ["pivot_point", "moving_average", "rsi", "macd"]


#### 1. GET THE TOTAL NUMBER OF TRANSACTIONS
# print ("total: ", data["num_transactions_total"].iloc[-1] )
# for i in range(len(corresponding_symbols)):
#     key = "num_transactions_"+corresponding_symbols[i]
#     print (i,") ", corresponding_symbols[i], ": ", data[key].iloc[-1])

### 1.1 number of transactions as of the 4th day
# total = 0
# for i in range(len(corresponding_symbols)):
#     key = "num_transactions_"+corresponding_symbols[i]
#     total += data[key].iloc[86]
# print (total)

#### 2. Plot when the transactions happened
# x = list(range(336))
# # print (x)
# for symbol in corresponding_symbols:
#     key = "num_transactions_"+symbol
#     plt.plot(x, data[key], label = symbol)

# plt.locator_params(axis='y', nbins=5)
# _25_tick = round(336 * 0.25),
# _50_tick = round(336 * 0.5),
# _75_tick = round(336 * 0.75),
# plt.xticks([
#         0, 
#         _25_tick[0],
#         _50_tick[0],
#         _75_tick[0],
#         336
#     ],
#     [   
#         "01/01/21",
#         "04/01/21",
#         "07/01/21",
#         "11/01/21",
#         "14/01/21",
#     ],
#     visible=True, rotation="horizontal")

# plt.legend(loc='best')
# plt.xlabel("Date")
# plt.ylabel("Amount of Transactions")
# plt.title(label = "Number of Transactions per Corresponding Currency Pairs")
# plt.show()

### 3. NUMBER OF TRANSACTIONS PER STRATEGY PER CURRENCY

# "num_transactions_pivot_point_ETH/USDT:USDT/ETH"

# for strategy in strategies:

#     for symbol in corresponding_symbols:

#         key = "num_transactions_"+strategy+"_"+symbol
#         print (strategy,", ", symbol, ": ", data[key].iloc[-1])

### WHEN DID strategy x TRANSACTIONS OCCURED?

# x = list(range(336))
# for symbol in corresponding_symbols:
#     key = 'num_transactions_rsi_'+ symbol
#     plt.plot(x, data[key], label = symbol.split(':')[0] + "...")
#     _25_tick = round(336 * 0.25),
#     _50_tick = round(336 * 0.5),
#     _75_tick = round(336 * 0.75),
#     plt.xticks([
#             0, 
#             _25_tick[0],
#             _50_tick[0],
#             _75_tick[0],
#             336
#         ],
#         [   
#             "01/01/21",
#             "04/01/21",
#             "07/01/21",
#             "11/01/21",
#             "14/01/21",
#         ],
#         visible=True, rotation="horizontal")

# plt.legend(loc='best', fontsize = 'small')
# plt.xlabel("Date")
# plt.ylabel("Amount of Transactions")
# plt.title(label = "RSI Agents Transactions per Corresponding Currency Pairs")
# plt.show()



#### 4. GET THE TOTAL NUMBER OF ORDERS
# for i in range(len(symbols)):
#     key = "num_orders_"+symbols[i]
#     print (i,") ", symbols[i], ": ", data[key].iloc[-1])

### 5. NUMBER OF ORDERS PER STRATEGY PER CURRENCY

for strategy in strategies:
    for symbol in symbols:
        key = "num_orders_"+strategy+"_"+symbol
        print (strategy,", ", symbol, ": ", data[key].iloc[-1])