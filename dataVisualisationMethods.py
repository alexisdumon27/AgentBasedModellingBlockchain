def getTotalTransactions(model):
    return model.currency_market.num_of_transactions_dict['total'][-1]

def getTotalETH_USDTTransactions(model):
    return model.currency_market.num_of_transactions_dict['ETH/USDT:USDT/ETH'][-1]

def getTotalETH_BNBTransactions(model):
    return model.currency_market.num_of_transactions_dict['ETH/BNB:BNB/ETH'][-1]

def getTotalETH_BTCTransactions(model):
    return model.currency_market.num_of_transactions_dict['ETH/BTC:BTC/ETH'][-1]

def getTotalBNB_BTCTransactions(model):
    return model.currency_market.num_of_transactions_dict['BNB/BTC:BTC/BNB'][-1]

def getTotalBNB_USDTTransactions(model):
    return model.currency_market.num_of_transactions_dict['BNB/USDT:USDT/BNB'][-1]

def getTotalBTC_USDTTransactions(model):
    return model.currency_market.num_of_transactions_dict['BTC/USDT:USDT/BTC'][-1]

# def getRelativeTotalWealthRandom(model):
#     random_agents = model.agents_using_each_strategy_dict["random"]
#     return sum(agent.currentUSDValueOfWallet for agent in random_agents) / len(random_agents)

def getRelativeTotalWealthPivotPoint(model):
    pivot_point_agents = model.agents_using_each_strategy_dict["pivot_point"]
    return sum(agent.currentUSDValueOfWallet for agent in pivot_point_agents) / len(pivot_point_agents)

def getRelativeTotalWealthMovingAverage(model):
    moving_average_agents = model.agents_using_each_strategy_dict["moving_average"]
    return sum(agent.currentUSDValueOfWallet for agent in moving_average_agents) / len(moving_average_agents)

def getRelativeTotalWealthMACD(model):
    macd_agents = model.agents_using_each_strategy_dict["macd"]
    return sum(agent.currentUSDValueOfWallet for agent in macd_agents) / len(macd_agents)

def getRelativeTotalWealthRSI(model):
    rsi_agents = model.agents_using_each_strategy_dict["rsi"]
    return sum(agent.currentUSDValueOfWallet for agent in rsi_agents) / len(rsi_agents)

def getWealthiestAgents0(model):
    return sorted(model.list_of_agents_not_including_random, key=lambda x: x.currentUSDValueOfGains, reverse=True)[:10][0].currentUSDValueOfGains # sorts in descending order and keeps first 10

def getWealthiestAgents1(model):
    return sorted(model.list_of_agents_not_including_random, key=lambda x: x.currentUSDValueOfGains, reverse=True)[:10][1].currentUSDValueOfGains # sorts in descending order and keeps first 10

def getWealthiestAgents2(model):
    return sorted(model.list_of_agents_not_including_random, key=lambda x: x.currentUSDValueOfGains, reverse=True)[:10][2].currentUSDValueOfGains # sorts in descending order and keeps first 10

def getWealthiestAgents3(model):
    return sorted(model.list_of_agents_not_including_random, key=lambda x: x.currentUSDValueOfGains, reverse=True)[:10][3].currentUSDValueOfGains # sorts in descending order and keeps first 10

def getWealthiestAgents4(model):
    return sorted(model.list_of_agents_not_including_random, key=lambda x: x.currentUSDValueOfGains, reverse=True)[:10][4].currentUSDValueOfGains # sorts in descending order and keeps first 10

def getWealthiestAgents5(model):
    return sorted(model.list_of_agents_not_including_random, key=lambda x: x.currentUSDValueOfGains, reverse=True)[:10][5].currentUSDValueOfGains # sorts in descending order and keeps first 10

def getWealthiestAgents6(model):
    return sorted(model.list_of_agents_not_including_random, key=lambda x: x.currentUSDValueOfGains, reverse=True)[:10][6].currentUSDValueOfGains # sorts in descending order and keeps first 10

def getWealthiestAgents7(model):
    return sorted(model.list_of_agents_not_including_random, key=lambda x: x.currentUSDValueOfGains, reverse=True)[:10][7].currentUSDValueOfGains # sorts in descending order and keeps first 10

def getWealthiestAgents8(model):
    return sorted(model.list_of_agents_not_including_random, key=lambda x: x.currentUSDValueOfGains, reverse=True)[:10][8].currentUSDValueOfGains # sorts in descending order and keeps first 10

def getWealthiestAgents9(model):
    return sorted(model.list_of_agents_not_including_random, key=lambda x: x.currentUSDValueOfGains, reverse=True)[:10][9].currentUSDValueOfGains # sorts in descending order and keeps first 10

def getNumRandomOrderbook(model):
    agents = model.agents_using_each_strategy_dict["random"]
    total = 0
    for i in range(len(agents)):
        if agents[i].has_made_open_order and not agents[i].open_transaction_was_successfull:
            total += 1
    return total

def getNumPivotPointOrderbook(model):
    agents = model.agents_using_each_strategy_dict["pivot_point"]
    total = 0
    for i in range(len(agents)):
        if agents[i].has_made_open_order and not agents[i].open_transaction_was_successfull:
            total += 1
        if agents[i].has_made_open_order and agents[i].open_transaction_was_successfull and agents[i].has_made_closing_order and not agents[i].closing_transaction_was_successfull:
            total += 1
    return total

def getNumMovingAverageOrderbook(model):
    agents = model.agents_using_each_strategy_dict["moving_average"]
    total = 0
    for i in range(len(agents)):
        if agents[i].has_made_open_order and not agents[i].open_transaction_was_successfull:
            total += 1
        if agents[i].has_made_open_order and agents[i].open_transaction_was_successfull and agents[i].has_made_closing_order and not agents[i].closing_transaction_was_successfull:
            total += 1
    return total

def getNumRSIOrderbook(model):
    agents = model.agents_using_each_strategy_dict["rsi"]
    total = 0
    for i in range(len(agents)):
        if agents[i].has_made_open_order and not agents[i].open_transaction_was_successfull:
            total += 1
        if agents[i].has_made_open_order and agents[i].open_transaction_was_successfull and agents[i].has_made_closing_order and not agents[i].closing_transaction_was_successfull:
            total += 1
    return total

def getNumMACDOrderbook(model):
    agents = model.agents_using_each_strategy_dict["macd"]
    total = 0
    for i in range(len(agents)):
        if agents[i].has_made_open_order and not agents[i].open_transaction_was_successfull:
            total += 1
        if agents[i].has_made_open_order and agents[i].open_transaction_was_successfull and agents[i].has_made_closing_order and not agents[i].closing_transaction_was_successfull:
            total += 1
    return total

# PIVOT POINT with diff currency pair
def getNumOfTransactionsPivotPointETHUSDT(model):
    return model.currency_market.num_of_transactions_dict_by_strategy['pivot_point']["ETH/USDT:USDT/ETH"]

def getNumOfTransactionsPivotPointETHBNB(model):
    return model.currency_market.num_of_transactions_dict_by_strategy['pivot_point']["ETH/BNB:BNB/ETH"]

def getNumOfTransactionsPivotPointETHBTC(model):
    return model.currency_market.num_of_transactions_dict_by_strategy['pivot_point']["ETH/BTC:BTC/ETH"]

def getNumOfTransactionsPivotPointBNBBTC(model):
    return model.currency_market.num_of_transactions_dict_by_strategy['pivot_point']["BNB/BTC:BTC/BNB"]

def getNumOfTransactionsPivotPointBNBUSDT(model):
    return model.currency_market.num_of_transactions_dict_by_strategy['pivot_point']["BNB/USDT:USDT/BNB"]

def getNumOfTransactionsPivotPointBTCUSDT(model):
    return model.currency_market.num_of_transactions_dict_by_strategy['pivot_point']["BTC/USDT:USDT/BTC"]

# MOVING AVERAGE with diff currency pair
def getNumOfTransactionsMovingAverageETHUSDT(model):
    return model.currency_market.num_of_transactions_dict_by_strategy['moving_average']["ETH/USDT:USDT/ETH"]

def getNumOfTransactionsMovingAverageETHBNB(model):
    return model.currency_market.num_of_transactions_dict_by_strategy['moving_average']["ETH/BNB:BNB/ETH"]

def getNumOfTransactionsMovingAverageETHBTC(model):
    return model.currency_market.num_of_transactions_dict_by_strategy['moving_average']["ETH/BTC:BTC/ETH"]

def getNumOfTransactionsMovingAverageBNBBTC(model):
    return model.currency_market.num_of_transactions_dict_by_strategy['moving_average']["BNB/BTC:BTC/BNB"]

def getNumOfTransactionsMovingAverageBNBUSDT(model):
    return model.currency_market.num_of_transactions_dict_by_strategy['moving_average']["BNB/USDT:USDT/BNB"]

def getNumOfTransactionsMovingAverageBTCUSDT(model):
    return model.currency_market.num_of_transactions_dict_by_strategy['moving_average']["BTC/USDT:USDT/BTC"]

# RSI with diff currency pair
def getNumOfTransactionsRSIETHUSDT(model):
    return model.currency_market.num_of_transactions_dict_by_strategy['rsi']["ETH/USDT:USDT/ETH"]

def getNumOfTransactionsRSIETHBNB(model):
    return model.currency_market.num_of_transactions_dict_by_strategy['rsi']["ETH/BNB:BNB/ETH"]

def getNumOfTransactionsRSIETHBTC(model):
    return model.currency_market.num_of_transactions_dict_by_strategy['rsi']["ETH/BTC:BTC/ETH"]

def getNumOfTransactionsRSIBNBBTC(model):
    return model.currency_market.num_of_transactions_dict_by_strategy['rsi']["BNB/BTC:BTC/BNB"]

def getNumOfTransactionsRSIBNBUSDT(model):
    return model.currency_market.num_of_transactions_dict_by_strategy['rsi']["BNB/USDT:USDT/BNB"]

def getNumOfTransactionsRSIBTCUSDT(model):
    return model.currency_market.num_of_transactions_dict_by_strategy['rsi']["BTC/USDT:USDT/BTC"]

# MACD with diff currency pair
def getNumOfTransactionsMACDETHUSDT(model):
    return model.currency_market.num_of_transactions_dict_by_strategy['macd']["ETH/USDT:USDT/ETH"]

def getNumOfTransactionsMACDETHBNB(model):
    return model.currency_market.num_of_transactions_dict_by_strategy['macd']["ETH/BNB:BNB/ETH"]

def getNumOfTransactionsMACDETHBTC(model):
    return model.currency_market.num_of_transactions_dict_by_strategy['macd']["ETH/BTC:BTC/ETH"]

def getNumOfTransactionsMACDBNBBTC(model):
    return model.currency_market.num_of_transactions_dict_by_strategy['macd']["BNB/BTC:BTC/BNB"]

def getNumOfTransactionsMACDBNBUSDT(model):
    return model.currency_market.num_of_transactions_dict_by_strategy['macd']["BNB/USDT:USDT/BNB"]

def getNumOfTransactionsMACDBTCUSDT(model):
    return model.currency_market.num_of_transactions_dict_by_strategy['macd']["BTC/USDT:USDT/BTC"]

def getDatesETH_USDTTransactions(model):
    return model.currency_market.transaction_dates_dict_by_strategy['ETH/USDT:USDT/ETH']

def getDatesETH_BNBTransactions(model):
    return model.currency_market.transaction_dates_dict_by_strategy['ETH/BNB:BNB/ETH']

def getDatesETH_BTCTransactions(model):
    return model.currency_market.transaction_dates_dict_by_strategy['ETH/BTC:BTC/ETH']

def getDatesBNB_BTCTransactions(model):
    return model.currency_market.transaction_dates_dict_by_strategy['BNB/BTC:BTC/BNB']

def getDatesBNB_USDTTransactions(model):
    return model.currency_market.transaction_dates_dict_by_strategy['BNB/USDT:USDT/BNB']

def getDatesBTC_USDTTransactions(model):
    return model.currency_market.transaction_dates_dict_by_strategy['BTC/USDT:USDT/BTC']