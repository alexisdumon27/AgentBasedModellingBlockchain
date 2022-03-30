from model import MarketModel
import pandas as pd
from dataVisualisationMethods import *
from mesa.batchrunner import BatchRunner
import time
import matplotlib.pyplot as plt

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

corresponding_symbols = [
    "ETH/USDT:USDT/ETH", "ETH/BNB:BNB/ETH", "ETH/BTC:BTC/ETH", "BNB/BTC:BTC/BNB", "BNB/USDT:USDT/BNB", "BTC/USDT:USDT/BTC"
]
strategies = ["pivot_point", "moving_average", "rsi", "macd"]


# number of steps in 14 days of 335!
start_step = 8764 # 2021-01-01 00:52:00
# end_step = 9099 # 2021-01-14 23:52:00

model = MarketModel(starting_date= start_step, ratio_of_random_strategy_to_other=0.5, ratio_of_agents_engaged_each_turn=0.5, num_agents=152)

# print(model.round)

end_step = 8765

start = time.time()

step = start_step
while step <= end_step:
    start_0 = time.time()
    print ("step: ", step - start_step)
    model.step()
    end_0 = time.time()
    print(end_0 - start_0)
    step += 1 

end = time.time()
print(end - start)

### CREATE DATAFRAME CONTAINING ALL THE DATA
model_df = model.datacollector.get_model_vars_dataframe()

### 1. NUMBER OF TRANSACTIONS PER CORRESPONDING CURRENCY PAIRS ***** done ******
# which corresponding currency pair undergoes the most transactions (ETH/USDT:USDT/ETH ... )
## ALREADY COLLECTED by the data.collector --> in model_df
# is an array of the number of transactions though so make sure you get last element to find total! 

### 2. NUMBER OF ORDERS PER CURRENCY PAIRS ***** done ******
# which currency pair undergoes the most orders (ETH/USDT ... )
### currency_market.num_of_orders_by_currency_pairs["ETH/USDT"] = 27
# adding it to model_df

for i in range(12):
    symbol = symbols[i]
    key = "num_orders_"+symbol
    model_df[key] = model.currency_market.num_of_orders_by_currency_pairs[symbol]

### 3. NUMBER OF TRANSACTIONS PER STRATEGY PER CURRENCY PAIR ***** done ******
# which strategy does the most transactions with each corresponding currency pair (ETH/USDT:USDT/ETH ... )
# ALREADY COLLECTED BY data.collector so already in model_df -- "num_transactions_pivot_point_ETH/USDT:USDT/ETH"


### 4. NUMBER OF ORDERS PER STARTEGY PER CURRENCY PAIR ***** done ******
# which strategy does the most orders for each currency pair (ETH/USDT ... )
## currency_market.num_of_orders_dict_by_strategy_by_currency["pivot_point"]["symbol"]

for i in range(4): # for all strategies
    strategy = strategies[i]
    for j in range(12): # for all currency pairs
        symbol = symbols[j]
        key = "num_orders_" + strategy + "_" + symbol
        model_df[key] = model.currency_market.num_of_orders_dict_by_strategy_by_currency[strategy][symbol]

# 110 

### 5. TRANSACTION DATES PER STRATEGY
# when do the transactions happen per strategy per corresponding currency pair
## currency_market.transaction_dates_dict_by_strategy[strategy][corresponding_currency_pairs]
# array of rounds 
# I want to add to model_df number of transactions per turn x [1,2,3,4,5] y = [0,1,0,3,2]
for i in range(4): # for the four strategies

    strategy = strategies[i]
    dictionary = {"ETH/USDT": {}, "USDT/ETH" : {},"ETH/BNB": {}, "BNB/ETH" : {},"ETH/BTC": {}, "BTC/ETH" : {},"BNB/BTC": {}, "BTC/BNB" : {},"BNB/USDT": {}, "USDT/BNB" : {},"BTC/USDT": {}, "USDT/BTC" : {}, }
    num_of_steps = end_step - start_step + 1
    for j in range(6): # for the 6 corresponding currency pairs
        y = []
        symbol = corresponding_symbols[j]
        # add the data to the plot...
        # 1. get the data for strategy -- currency pair
        data = model.currency_market.transaction_dates_dict_by_strategy[strategy][symbol]
        print("strategy: ", strategy, " symbol: ", symbol)
        print (data)
        # 2. find number of times each value appears and put in dictionary
        dictionary[symbol] = {x:data.count(x) for x in data}
        print (dictionary)

        for w in range(start_step, end_step+1):
            print ("index w: ", w)
            if w in dictionary[symbol]:
                y.append(dictionary[symbol][w])
            else:
                y.append(0)
        print ("array added to model_df: ", y)
        key = "dates_transactions_"+ strategy + "_" + symbol
        model_df[key] = y # this did not work ... 

    #     plt.scatter(x, y)
    # plt.show()

print (model_df.columns)
print (model_df.shape) # 110 + 24 = 134

### 6. ORDER DATES PER STRATEGY PER CURRENCY PAIR
# when do the orders happen per strategy per currency pair
## currency_market.order_dates_by_strategy_by_currency[strategy][currency_pair]

for i in range(4): # for the four strategies

    strategy = strategies[i]
    dictionary = {"ETH/USDTUSDT/ETH" : {},"ETH/BNB:BNB/ETH" : {},"ETH/BTC:BTC/ETH" : {},"BNB/BTC:BTC/BNB" : {},"BNB/USDT:USDT/BNB" : {},"BTC/USDT:USDT/BTC" : {}, }
    num_of_steps = end_step - start_step + 1
    for j in range(12): # for the 12 currency pairs
        y = []
        symbol = symbols[j]
        # add the data to the plot...
        # 1. get the data for strategy -- currency pair
        data = model.currency_market.order_dates_by_strategy_by_currency[strategy][symbol]
        print("strategy: ", strategy, " symbol: ", symbol)
        print (data)
        # 2. find number of times each value appears and put in dictionary
        dictionary[symbol] = {x:data.count(x) for x in data}
        print (dictionary)

        for w in range(start_step, end_step+1):
            print ("index w: ", w)
            if w in dictionary[symbol]:
                y.append(dictionary[symbol][w])
            else:
                y.append(0)
        print ("array added to model_df: ", y)
        key = "dates_transactions_"+ strategy + "_" + symbol
        model_df[key] = y # this did not work ...

print (model_df.columns)
print (model_df.shape) # 110 + 24 = 134  + 48 = 182

### 7. DATA ON TOP 10 WEALTHIEST AGENTS
# what do the top 10 wealthiest agents look like?
## wealthy_1_data = [strategy, currentUSDValueOfGains, risk_level, number_of_open_orders, number_of_closed_orders]
agents_by_wealth = sorted(model.list_of_agents_not_including_random, key=lambda x: x.currentUSDValueOfGains, reverse=True)[:10]
for i in range(10):
    key = "wealthy_"+ str(i)
    agent = agents_by_wealth[i]
    data = [agent.strategy.name, agent.currentUSDValueOfGains, agent.risk_level, agent.num_of_open_orders, agent.num_of_close_orders]
    model_df[key] = []
    model_df.at[0, data]

print (model_df.columns)
print (model_df.shape) # 110 + 24 = 134  + 48 = 182

###### -----------------------------------------------------------------------------------------------------------------------------------

# ### 8. ADDS NUMBER OF OPEN & CLOSE ORDERS BY CURRENCY PAIRS
# open_orders = model.currency_market.open_order_by_currency_pair
# close_orders = model.currency_market.close_order_by_currency_pair
# model_df = model.datacollector.get_model_vars_dataframe()

# for i in range(12):
#     symbol = symbols[i]
#     open_key = "open_" + symbol
#     model_df[open_key] = open_orders[symbol]

#     close_key = "close_" + symbol # number of times this symbol was closed is number of opposite currency order ETH/USDT was closed number of USDT/ETH
#     currencies = symbol.split("/")
#     opposite_symbol = currencies[1] + "/" + currencies[0]
#     model_df[close_key] = close_orders[opposite_symbol]


### 9. ADDS NUMBER OF ORDERS WITH EACH CURRENCY PAIR
# for i in range(4):
#     strategy = strategies[i]
#     for j in range(12): # finds the opposite keys
#         symbol = symbols[j]
#         key = "order_"+strategy+"_"+symbol
#         model_df[key] = model.currency_market.num_of_orders_dict_by_strategy_by_currency[strategy][symbol]  


# graphStrategyByCurrencyPairData(model.currency_market.transaction_dates_dict)

# print (model_df)

