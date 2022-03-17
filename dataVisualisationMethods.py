
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

def getRelativeTotalWealthRandom(model):
    random_agents = model.agents_using_each_strategy_dict["random"]
    return sum(agent.currentUSDValueOfWallet for agent in random_agents) / len(random_agents)

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
    return sorted(model.schedule.agents, key=lambda x: x.currentUSDValueOfWallet, reverse=True)[:10][0].currentUSDValueOfWallet # sorts in descending order and keeps first 10

def getWealthiestAgents1(model):
    return sorted(model.schedule.agents, key=lambda x: x.currentUSDValueOfWallet, reverse=True)[:10][1].currentUSDValueOfWallet # sorts in descending order and keeps first 10

def getWealthiestAgents2(model):
    return sorted(model.schedule.agents, key=lambda x: x.currentUSDValueOfWallet, reverse=True)[:10][2].currentUSDValueOfWallet # sorts in descending order and keeps first 10

def getWealthiestAgents3(model):
    return sorted(model.schedule.agents, key=lambda x: x.currentUSDValueOfWallet, reverse=True)[:10][3].currentUSDValueOfWallet # sorts in descending order and keeps first 10

def getWealthiestAgents4(model):
    return sorted(model.schedule.agents, key=lambda x: x.currentUSDValueOfWallet, reverse=True)[:10][4].currentUSDValueOfWallet # sorts in descending order and keeps first 10

def getWealthiestAgents5(model):
    return sorted(model.schedule.agents, key=lambda x: x.currentUSDValueOfWallet, reverse=True)[:10][5].currentUSDValueOfWallet # sorts in descending order and keeps first 10

def getWealthiestAgents6(model):
    return sorted(model.schedule.agents, key=lambda x: x.currentUSDValueOfWallet, reverse=True)[:10][6].currentUSDValueOfWallet # sorts in descending order and keeps first 10

def getWealthiestAgents7(model):
    return sorted(model.schedule.agents, key=lambda x: x.currentUSDValueOfWallet, reverse=True)[:10][7].currentUSDValueOfWallet # sorts in descending order and keeps first 10

def getWealthiestAgents8(model):
    return sorted(model.schedule.agents, key=lambda x: x.currentUSDValueOfWallet, reverse=True)[:10][8].currentUSDValueOfWallet # sorts in descending order and keeps first 10

def getWealthiestAgents9(model):
    return sorted(model.schedule.agents, key=lambda x: x.currentUSDValueOfWallet, reverse=True)[:10][9].currentUSDValueOfWallet # sorts in descending order and keeps first 10