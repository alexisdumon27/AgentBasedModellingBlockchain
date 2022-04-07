import pandas as pd
import matplotlib.pyplot as plt
import statistics as stat

"""
    This script visualises the results obtained from running the simulation 10 times
"""

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


## 1. GET THE TOTAL NUMBER OF TRANSACTIONS
name = "Data/simulation_results/model_results_"
number = []
for i in range(10):
    filename = name + str(i) + ".csv"
    data = pd.read_csv(filename)
    print ("total: ", data['num_transactions_total'].iloc[-1] )
    number.append(data['num_transactions_total'].iloc[-1])

## 2. number of transactions per currency pairs per strategy USELESS MIGHT AS WELL LOOK AT PER CURRENCY PAIR PER STRATEGY!!!
for symbol in corresponding_symbols:
    avg = 0
    for i in range(10):
        filename = name + str(i) + ".csv"
        data = pd.read_csv(filename)
        column = "num_transactions_" + symbol
        avg += data[column].iloc[-1]
    avg /= 10
    print ("average for ", symbol, ": ", avg )

## 3. number of transactions as of the 4th day
for symbol in corresponding_symbols:
    total = 0
    for i in range(10):
        filename = name + str(i) + ".csv"
        data = pd.read_csv(filename)
        key = "num_transactions_"+ symbol
        total += data[key].iloc[86]
    print (symbol,": ", total / 10)   

## 4. Plot when the transactions happened
x = list(range(336))
print (x)

for symbol in corresponding_symbols:
    key = "num_transactions_"+symbol
    total = pd.Series()
    for i in range(10):
        filename = name + str(i) + ".csv"
        data = pd.read_csv(filename)
        if total.empty:
            total = data[key]
        else: total += data[key]

    total /= 10
    plt.plot(x, total, label = symbol)

plt.locator_params(axis='y', nbins=10)
_25_tick = round(336 * 0.25),
_50_tick = round(336 * 0.5),
_75_tick = round(336 * 0.75),
plt.xticks([
        0, 
        _25_tick[0],
        _50_tick[0],
        _75_tick[0],
        336
    ],
    [   
        "01/01/21",
        "04/01/21",
        "07/01/21",
        "11/01/21",
        "14/01/21",
    ],
    visible=True, rotation="horizontal")

plt.legend(loc='best')
plt.xlabel("Date")
plt.ylabel("Average Amount of Transactions")
plt.title(label = "Average Number of Transactions per Corresponding Currency Pairs versus Date")
plt.show()

## 5. NUMBER OF TRANSACTIONS PER STRATEGY PER CURRENCY
"num_transactions_pivot_point_ETH/USDT:USDT/ETH"
for strategy in strategies:
    for symbol in corresponding_symbols:
        avg = 0
        for i in range(5):
            filename = name + str(i) + ".csv"
            data = pd.read_csv(filename)
            column = "num_transactions_" +strategy+"_"+symbol
            avg += data[column].iloc[-1]
        avg /= 10
        print ("average for ", strategy + ", ", symbol, ": ", avg )

## 6. WHEN DID strategy x TRANSACTIONS OCCURED?
x = list(range(336))
for symbol in corresponding_symbols:
    key = 'num_transactions_rsi_'+ symbol
    plt.plot(x, data[key], label = symbol.split(':')[0] + "...")
    _25_tick = round(336 * 0.25),
    _50_tick = round(336 * 0.10),
    _75_tick = round(336 * 0.75),
    plt.xticks([
            0, 
            _25_tick[0],
            _50_tick[0],
            _75_tick[0],
            336
        ],
        [   
            "01/01/21",
            "04/01/21",
            "07/01/21",
            "11/01/21",
            "14/01/21",
        ],
        visible=True, rotation="horizontal")

plt.legend(loc='best', fontsize = 'small')
plt.xlabel("Date")
plt.ylabel("Amount of Transactions")
plt.title(label = "RSI Agents Transactions per Corresponding Currency Pairs")
plt.show()

## 7. Plot when the orders happened
x = list(range(336))

all_orders = pd.Series()
for symbol in symbols:
    key = "num_orders_"+symbol
    total = pd.Series()
    for i in range(10):
        filename = name + str(i) + ".csv"
        data = pd.read_csv(filename)
        if total.empty:
            total = data[key]
        else: total += data[key]
    total /= 10
    if all_orders.empty:
        all_orders = total
    else: all_orders += total
    
fig, ax = plt.subplots()

plt.plot(x, all_orders, label = "orders")


## 8.
total_transactions = pd.Series()
for i in range(10):
    filename = name + str(i) + ".csv"
    data = pd.read_csv(filename)
    if total_transactions.empty:
        total_transactions = data['num_transactions_total']
    else: total_transactions += data['num_transactions_total']
total_transactions /= 10


ax_2 = ax.twinx()
plt.plot(x, total_transactions, color = 'red', label = "transactions")

plt.locator_params(axis='y', nbins=5)
_25_tick = round(336 * 0.25),
_50_tick = round(336 * 0.5),
_75_tick = round(336 * 0.75),
plt.xticks([
        0, 
        _25_tick[0],
        _50_tick[0],
        _75_tick[0],
        336
    ],
    [   
        "01/01/21",
        "04/01/21",
        "07/01/21",
        "11/01/21",
        "14/01/21",
    ],
    visible=True, rotation="horizontal")

plt.legend(loc='best')
plt.xlabel("Date")
plt.ylabel("Average Amount")
plt.title(label = "Average Number of Orders & Transactions versus Date")
plt.show()


## 9. DATA leading to day 4 -- number of orders
# Look at the most ordered currency pair leading up to it
# around step 84 and around step 252
# find the one with the highest number of orders around the 4th of Jan
# 2021-01-04 00:52:00 index 8836 # for exchange rates data
# 8812,2021-01-03 00:52:00 # for exchange rates data
# 9004 for 2021-01-11
start_exchange_data = 8965 
end_exchange_data = 9016
start = 213 
end = 264

symbol_considered = 'BNB/BNB'

x = list(range(start, end))

fig, ax = plt.subplots()

y_prices = exchange_rates[symbol_considered].iloc[start_exchange_data: end_exchange_data]
ax.plot(x, y_prices, color = '#d4b35b', label = 'exchange rate')
ax.set_xlabel("Date")
ax.set_ylabel('Exchange Rate')

total = pd.Series()
for i in range(10):
    filename = name + str(i) + ".csv"
    data = pd.read_csv(filename)
    if total.empty:
        total = data['num_orders_'+symbol_considered][start:end]
    else: total += data['num_orders_'+symbol_considered][start:end]
y_orders = total / 10

ax_2 = ax.twinx()
ax_2.plot(x, y_orders, color = '#3f72e0', label = "orders")
ax_2.set_ylabel('Number of Orders')

plt.locator_params(axis='y', nbins=5)
_25_tick = round(((end - start) * 0.25) + start),
_50_tick = round(((end - start) * 0.5) + start ),
_75_tick = round(((end - start) * 0.75) + start),
plt.xticks([
        start, 
        _25_tick[0],
        _50_tick[0],
        _75_tick[0],
        end
    ],
    [   
        "09/01 10h",
        "10/01 4h30",
        "10/01 23h00",
        "11/01 17h30",
        "12/01 12h",
    ],
    visible=True, rotation="horizontal")

ax.legend(loc = "best")
ax_2.legend(loc = "center left")
plt.title(label = "Avg Orders and Exchange Price for "+ symbol_considered +" versus Date")
plt.show()
# https://cmdlinetips.com/2019/10/how-to-make-a-plot-with-two-different-y-axis-in-python-with-matplotlib/

## 10.
start_exchange_data = 8764
end_exchange_data = 8862
start = 0 
end = 98

# 1st january to the 5th of january

plt.locator_params(axis='y', nbins=5)
_25_tick = round(((end - start) * 0.25) + start),
_50_tick = round(((end - start) * 0.5) + start ),
_75_tick = round(((end - start) * 0.75) + start),
plt.xticks([
        start, 
        _25_tick[0],
        _50_tick[0],
        _75_tick[0],
        end
    ],
    [   
        "01/01",
        "02/01",
        "03/01",
        "04/01",
        "05/01",
    ],
    visible=True, rotation="horizontal")
plt.plot(range(start, end), exchange_rates['BNB/BTC'].iloc[start_exchange_data: end_exchange_data], label = "BNB/BTC")
plt.legend(loc = "best")
plt.ylabel('Exchange Rate')
plt.xlabel('Date')
plt.title(label = "BNB/BTC Exchange Rate versus Date")
plt.show()

symbol_considered = 'ETH/BTC'

## 11. 
x = list(range(start, end))

fig, ax = plt.subplots()

y_prices = exchange_rates[symbol_considered].iloc[start_exchange_data: end_exchange_data]
ax.plot(x, y_prices, color = '#d4b35b', label = 'exchange rate')
ax.set_xlabel("Date")
ax.set_ylabel('Exchange Rate')

total = pd.Series()
for i in range(10):
    filename = name + str(i) + ".csv"
    data = pd.read_csv(filename)
    if total.empty:
        total = data['num_orders_'+symbol_considered][start:end]
    else: total += data['num_orders_'+symbol_considered][start:end]
y_orders = total / 10

ax_2 = ax.twinx()
ax_2.plot(x, y_orders, color = '#3f72e0', label = "orders")
ax_2.set_ylabel('Number of Orders')

plt.locator_params(axis='y', nbins=5)
_25_tick = round(((end - start) * 0.25) + start),
_50_tick = round(((end - start) * 0.5) + start ),
_75_tick = round(((end - start) * 0.75) + start),
plt.xticks([
        start, 
        _25_tick[0],
        _50_tick[0],
        _75_tick[0],
        end
    ],
    [   
        "02/01 10h",
        "03/01 4h30",
        "03/01 23h00",
        "04/01 17h30",
        "05/01 12h",
    ],
    visible=True, rotation="horizontal")

ax.legend(loc = "center left")
ax_2.legend(loc = "lower left")
plt.title(label = "Avg Orders and Exchange Price for "+ symbol_considered +" versus Date")
plt.show()


## 12. best number of orders over the start and end period
for symbol in symbols:
    key = "num_orders_" + symbol
    avg = 0
    for i in range(10):
        filename = name + str(i) + ".csv"
        data = pd.read_csv(filename)
        before = data[key].iloc[start]
        after = data[key].iloc[end]
        avg += after - before
    print (symbol, ": ", avg / 10)

## 13. GET THE TOTAL NUMBER OF ORDERS
for symbol in symbols:
    key = "num_orders_"+symbol
    print (i,") ", symbol, ": ", data[key].iloc[-1])

## 14. NUMBER OF ORDERS PER STRATEGY PER CURRENCY
for strategy in strategies:
    for symbol in symbols:
        avg = 0
        for i in range(10):
            filename = name + str(i) + ".csv"
            data = pd.read_csv(filename)
            column = "num_orders_"+strategy+"_"+symbol
            avg += data[column].iloc[-1]
        avg /= 10
        print (strategy,", ", symbol, ": ", avg)


###### AGENT RESULTS
import ast

# print (ast.literal_eval("[[8764, 'BTC', 'BNB', 0.017183206404403257]]")[0])
# print (convert_string_to_list("[[8764, 'BTC', 'BNB', 0.017183206404403257]]"))
# ,unique_id,strategy,risk_level,gains, open_orders, close_orders, outstanding_investment
# look at when there were open orders for BNB/USDT and USDT/BNB

# start_step = 8764 # 2021-01-01 00:52:00
# end_step = 9099 # 2021-01-14 23:52:00

agent_csv_name = "Data/simulation_results/agents_results_"
symbol_dict = {
    "ETH/USDT":0,
    "ETH/BNB" :0,
    "ETH/BTC":0,
    "BNB/BTC" :0,
    "BNB/USDT":0,
    "BTC/USDT":0,
    "USDT/ETH":0,
    "BNB/ETH" :0,
    "BTC/ETH" :0,
    "BTC/BNB" :0,
    "USDT/BNB":0,
    "USDT/BTC":0,
}

agents_info_dict = {
    "pivot_point" : {
        "averse" : {"number":0, "gains":0, "orders":0 }, 
        "neutral": {"number":0, "gains":0, "orders":0 }, 
        "taker": {"number":0, "gains":0, "orders":0 }
    },
    "moving_average" : {
        "averse" : {"number":0, "gains":0, "orders":0 }, 
        "neutral": {"number":0, "gains":0, "orders":0 }, 
        "taker": {"number":0, "gains":0, "orders":0 }
    },
    "rsi" : {
        "averse" : {"number":0, "gains":0, "orders":0 }, 
        "neutral": {"number":0, "gains":0, "orders":0 }, 
        "taker": {"number":0, "gains":0, "orders":0 }
    },
    "macd" : {
        "averse" : {"number":0, "gains":0, "orders":0 }, 
        "neutral": {"number":0, "gains":0, "orders":0 }, 
        "taker": {"number":0, "gains":0, "orders":0 }
    },
}
# 15. GET AGENTS strategy, risk level, and average gains
for i in range(10):
    filename = agent_csv_name+str(i)+".csv"
    data = pd.read_csv(filename)

    for index, row in data.iterrows():
        print(row)
        strat = row["strategy"]
        risk = row["risk_level"]
        gain = row["gains"]
        open_orders_num = len(ast.literal_eval(row["open_orders"]))
        close_orders_num = len(ast.literal_eval(row["close_orders"]))
        total_orders = open_orders_num + close_orders_num
        agents_info_dict[strat][risk]["gains"] += gain
        agents_info_dict[strat][risk]['number'] += 1
        agents_info_dict[strat][risk]['orders'] += total_orders
    
    print (agents_info_dict.items())


# 16.
for symbol in symbols:
    print ("-------- SYMBOL: ", symbol, " ---------")
    dates_of_open = []
    dates_of_close = []

    symbol_total = 0
    currency_0 = symbol.split("/")[0] # ETH
    currency_1 = symbol.split("/")[1] # USDT

    for i in range(10):
        filename = agent_csv_name + str(i) + ".csv"
        data = pd.read_csv(filename)
        
        for j in range(len(data["open_orders"])):
            open = ast.literal_eval(data["open_orders"].iloc[j])
            for order in open:
                if order[0] >= start_exchange_data and order[0] <= end_exchange_data: # only count orders within date range
                    if order[1] == currency_0 and order[2] == currency_1:
                        # ETH/USDT --> OPEN
                        dates_of_open.append(order[0])
                        symbol_dict[currency_0 +"/"+currency_1] += 1

        for j in range(len(data["close_orders"])):
            close = ast.literal_eval(data["close_orders"].iloc[j])
            for order in close:
                if order[0] >= start_exchange_data and order[0] <= end_exchange_data:
                    if order[1] == currency_1 and order[2] == currency_0:
                        # USDT/ETH and labelled CLOSE than closing a ETH/USDT investment
                        dates_of_close.append(order[0])
                        symbol_total += 1
                        symbol_dict[currency_1 +"/"+currency_0] += 1

    dates_of_open.sort()
    dates_of_close.sort()

    open_symbol = dict((x, dates_of_open.count(x) / 10) for x in set(dates_of_open))
    print ("open total: ", sum(open_symbol.values()))
    close_symbol = dict((x, dates_of_close.count(x) / 10) for x in set(dates_of_close))
    print ("close total: ", sum(close_symbol.values()))
    print (symbol, " total: ", symbol_dict[symbol] / 10)

fig, ax = plt.subplots()

plt.locator_params(axis='y', nbins=5)
_25_tick = round(((end_exchange_data - start_exchange_data) * 0.25) + start_exchange_data),
_50_tick = round(((end_exchange_data - start_exchange_data) * 0.5) + start_exchange_data),
_75_tick = round(((end_exchange_data - start_exchange_data) * 0.75) + start_exchange_data),
plt.xticks([
        start_exchange_data, 
        _25_tick[0],
        _50_tick[0],
        _75_tick[0],
        end_exchange_data
    ],
    [   
        "01/01",
        "02/01",
        "03/01",
        "04/01",
        "05/01",
    ],
    visible=True, rotation="horizontal")

ax.set_ylabel('AVG number of orders')
plt.xlabel('Date')
ax.legend(loc='best')
plt.title("Open & Close orders for BNB/USDT & USDT/BNB over time")
plt.show()
