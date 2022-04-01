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
end_step = 9099 # 2021-01-14 23:52:00
# end_step = 8765

for model_run in range(5):
    model = MarketModel(starting_date= start_step, ratio_of_random_strategy_to_other=0.5, ratio_of_agents_engaged_each_turn=0.5, num_agents=152)

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
    # data is per turn --> an index captures the state of the model at each turn
    model_df = model.datacollector.get_model_vars_dataframe()

    ### 1. NUMBER OF TRANSACTIONS PER CORRESPONDING CURRENCY PAIRS ***** done ******
    # which corresponding currency pair undergoes the most transactions (ETH/USDT:USDT/ETH ... )
    ## ALREADY COLLECTED by the data.collector --> in model_df
    # is an ARRAY of the number of transactions though so make sure you get last element to find total!

    ### 2. NUMBER OF ORDERS PER CURRENCY PAIRS ***** done ******
    # which currency pair undergoes the most orders (ETH/USDT ... )
    ### currency_market.num_of_orders_by_currency_pairs["ETH/USDT"] = [0, 1, 1, 4, 5] # should this be an ARRAY
    # adding it to model_df

    for i in range(12):
        symbol = symbols[i]
        key = "num_orders_"+symbol
        model_df[key] = model.currency_market.num_of_orders_by_currency_pairs[symbol] # cannot add an array... 

    # ### 3. NUMBER OF TRANSACTIONS PER STRATEGY PER CURRENCY PAIR ***** done ******
    # # which strategy does the most transactions with each corresponding currency pair (ETH/USDT:USDT/ETH ... )
    # # ALREADY COLLECTED BY data.collector so already in model_df -- "num_transactions_pivot_point_ETH/USDT:USDT/ETH"


    # ### 4. NUMBER OF ORDERS PER STARTEGY PER CURRENCY PAIR ***** done ******
    # # which strategy does the most orders for each currency pair (ETH/USDT ... )
    # ## currency_market.num_of_orders_dict_by_strategy_by_currency["pivot_point"]["symbol"] 

    for i in range(4): # for all strategies
        strategy = strategies[i]
        for j in range(12): # for all currency pairs
            symbol = symbols[j]
            key = "num_orders_" + strategy + "_" + symbol
            model_df[key] = model.currency_market.num_of_orders_dict_by_strategy_by_currency[strategy][symbol]

    # ### 5. AGENT DATA

    agents_by_wealth = sorted(model.list_of_agents_not_including_random, key=lambda x: x.currentUSDValueOfGains, reverse=True)

    agents_data = []
    for i in range(len(agents_by_wealth)):
        agent = agents_by_wealth[i]
        single_agent_data = []
        single_agent_data.append(agent.unique_id)
        single_agent_data.append(agent.strategy.name)
        single_agent_data.append(agent.risk_level)
        single_agent_data.append(agent.currentUSDValueOfGains)
        single_agent_data.append(agent.open_orders) # count to get number of len(open_orders)
        single_agent_data.append(agent.close_orders) # count to get number of
        agent_invest = agent.current_investment
        bought = None
        sold = None
        if agent_invest['bought_currency'] != None:
            bought = agent_invest['bought_currency'].symbol
        if agent_invest['sold_currency'] != None:
            sold = agent_invest['sold_currency'].symbol

        outstanding_investment = {"amount": agent_invest['amount'], 'bought_currency': bought, "sold_currency" : sold}
        single_agent_data.append(outstanding_investment)

        agents_data.append(single_agent_data)

    agents_df = pd.DataFrame(agents_data, columns=['unique_id', 'strategy','risk_level', 'gains', 'open_orders', 'close_orders', 'outstanding_investment'])

    # print (agents_data)
    # print (agents_df)
    # print (agents_df.iloc[0]['outstanding_investment'])
    # print (model_df)

    # compare random to other agents ... no need since 

    agents_df.to_csv("Data/simulation_results/agents_results_"+ str(model_run) +".csv")
    model_df.to_csv("Data/simulation_results/model_results_"+ str(model_run) +".csv")

