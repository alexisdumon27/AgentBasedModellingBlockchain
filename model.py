import random
from mesa import Model
from mesa.time import RandomActivation, BaseScheduler
from mesa.datacollection import DataCollector
import pandas as pd
from investment_strategies import MACDStrategy, MovingAverageStrategy, PivotPointStrategy, RSIStrategy, Strategy, RandomStrategy
from agents import MarketAgent
from currency_market import CurrencyMarket, Currency
from dataVisualisationMethods import *

class MarketModel(Model):
    def __init__(self, starting_date = 1, ratio_of_random_strategy_to_other = 0.5, ratio_of_agents_engaged_each_turn = 0.5, num_agents = 10):
        self.round = self.dateToRoundNumber(starting_date) # index keeping count of the round of simulation
        self.num_of_agents = num_agents
        self.ratio_of_agents_engaged_each_turn = ratio_of_agents_engaged_each_turn
        self.ratio_of_random_strategy_to_other = ratio_of_random_strategy_to_other
        
        self.exchange_rates = pd.read_csv('Data/exchange_rates.csv')

        self.currency_market = CurrencyMarket(self.exchange_rates)

        self.schedule = RandomActivation(self) # changed from RandomActivation

        self.list_of_agents = []
        self.createAgents()

        self.datacollector = DataCollector(
            model_reporters={
                "num_transactions_total" : getTotalTransactions,
                "num_transactions_ETH/USDT:USDT/ETH" : getTotalETH_USDTTransactions,
                "num_transactions_ETH/BNB:BNB/ETH" : getTotalETH_BNBTransactions,
                "num_transactions_ETH/BTC:BTC/ETH" : getTotalETH_BTCTransactions,
                "num_transactions_BNB/BTC:BTC/BNB" : getTotalBNB_BTCTransactions,
                "num_transactions_BNB/USDT:USDT/BNB" : getTotalBNB_USDTTransactions,
                "num_transactions_BTC/USDT:USDT/BTC" : getTotalBTC_USDTTransactions,
                "Random" : getRelativeTotalWealthRandom,
                "Pivot Point": getRelativeTotalWealthPivotPoint,
                "Moving Average": getRelativeTotalWealthMovingAverage,
                "RSI": getRelativeTotalWealthRSI,
                "MACD": getRelativeTotalWealthMACD,
                "Wealthy 0": getWealthiestAgents0,
                "Wealthy 1": getWealthiestAgents1,
                "Wealthy 2": getWealthiestAgents2,
                "Wealthy 3": getWealthiestAgents3,
                "Wealthy 4": getWealthiestAgents4,
                "Wealthy 5": getWealthiestAgents5,
                "Wealthy 6": getWealthiestAgents6,
                "Wealthy 7": getWealthiestAgents7,
                "Wealthy 8": getWealthiestAgents8,
                "Wealthy 9": getWealthiestAgents9,
                "Random orderbook" : getNumRandomOrderbook,
                "Pivot Point orderbook": getNumPivotPointOrderbook,
                "Moving Average orderbook": getNumMovingAverageOrderbook,
                "RSI orderbook": getNumRSIOrderbook,
                "MACD orderbook": getNumMACDOrderbook,
            }
        )

        self.running = True

    def createAgents(self):
        random_strategy = RandomStrategy("random", self.exchange_rates)
        pivot_point_strategy = PivotPointStrategy("pivot_point", self.exchange_rates)
        moving_average_strategy = MovingAverageStrategy("moving_average", self.exchange_rates)
        macd_strategy = MACDStrategy('macd', self.exchange_rates)
        rsi_strategy = RSIStrategy("rsi", self.exchange_rates)

        risk_levels = ["averse", "neutral", "taker"]

        # list of agents using each strategy
        self.agents_using_each_strategy_dict = {
            "random" : [],
            "pivot_point" : [],
            "moving_average" : [],
            "macd" : [],
            "rsi": []
        }
        num_of_random_agents = self.num_of_agents * self.ratio_of_random_strategy_to_other
        agent_number = 0
        while agent_number < self.num_of_agents: 
            risk_level = random.choice(risk_levels)
            a = None
            if agent_number < num_of_random_agents:
                a = MarketAgent(agent_number, self, random_strategy, risk_level, self.currency_market)
                self.agents_using_each_strategy_dict["random"].append(a)
            else:
                if agent_number % 4 == 0:
                    a = MarketAgent(agent_number, self, pivot_point_strategy, risk_level, self.currency_market)
                    self.agents_using_each_strategy_dict["pivot_point"].append(a)
                elif agent_number % 4 == 1:
                    a = MarketAgent(agent_number, self, moving_average_strategy, risk_level, self.currency_market)
                    self.agents_using_each_strategy_dict["moving_average"].append(a)
                elif agent_number % 4 == 2:
                    a = MarketAgent(agent_number, self, macd_strategy, risk_level, self.currency_market)
                    self.agents_using_each_strategy_dict["macd"].append(a)
                elif agent_number % 4 == 3:
                    a = MarketAgent(agent_number, self, rsi_strategy, risk_level, self.currency_market)
                    self.agents_using_each_strategy_dict["rsi"].append(a)
            self.schedule.add(a)
            self.list_of_agents.append(a)
            agent_number += 1

    def step(self):
        print ("Is it different to 0.5? :", self.ratio_of_agents_engaged_each_turn)
        num_of_agents_per_turn = round(self.num_of_agents * self.ratio_of_agents_engaged_each_turn)
        for i in range(num_of_agents_per_turn):
            self.schedule.step() # runs the step method for all Agents

        self.currency_market.order_book.sortOrdersInOrderBook()

        self.dataGathering()

        self.currency_market.priceClearingMechanism() # do all transactions

        self.datacollector.collect(self)
        self.round += 1 # go to the next round
    
    def dateToRoundNumber(self, date):
        return 27

    def dataGathering(self):
        order_book_data = self.currency_market.getOrderBook().orders
        simplified_order_book = self.simplifyOrderBook(order_book_data)
        # with open('orderBookData.JSON', 'w') as json_file:
        #     json.dump(simplified_order_book, json_file)
        # if self.round == 999: self.getInitialOrderbookTable() to JSON
        transaction_data = {
            # num of transactions with each currency and total !!! works !!!!!!!!
            "num_transactions_total" : self.currency_market.num_of_transactions_dict['total'],
            "num_transactions_ETH/USDT:USDT/ETH" : self.currency_market.num_of_transactions_dict['ETH/USDT:USDT/ETH'],
            "num_transactions_ETH/BNB:BNB/ETH" : self.currency_market.num_of_transactions_dict['ETH/BNB:BNB/ETH'],
            "num_transactions_ETH/BTC:BTC/ETH" : self.currency_market.num_of_transactions_dict['ETH/BTC:BTC/ETH'],
            "num_transactions_BNB/BTC:BTC/BNB" : self.currency_market.num_of_transactions_dict['BNB/BTC:BTC/BNB'],
            "num_transactions_BNB/USDT:USDT/BNB" : self.currency_market.num_of_transactions_dict['BNB/USDT:USDT/BNB'],
            "num_transactions_BTC/USDT:USDT/BTC" : self.currency_market.num_of_transactions_dict['BTC/USDT:USDT/BTC']
        }
        # with open('transactionData.JSON', 'w') as json_file:
        #     json.dump(transaction_data, json_file)

        wealthiest_agents_data = self.getWealthiestAgentsInformation(self.getTenWealthiestAgents())
        # with open('wealthiestAgentsData.JSON', 'w') as json_file:
        #     json.dump(wealthiest_agents_data, json_file)

        wealth_distribution_data = self.getWealthDistributionByStrategy()
        # with open('wealthDistributionData.JSON', 'w') as json_file:
        #     json.dump(wealth_distribution_data, json_file)

    def getTenWealthiestAgents(self):
        return sorted(self.schedule.agents, key=lambda x: x.currentUSDValueOfWallet, reverse=True)[:10] # sorts in descending order and keeps first 10

    def getWealthiestAgentsInformation(self, agents):
        wealthy_dict = {
        }
        name = "wealthy_"
        for i in range(len(agents)):
            wealthy_number_key = name + str(i)
            wealthy_dict[wealthy_number_key] = {"amount_in_usd": 0, "strategy": "", "num_of_transactions": 0, "most_traded_currency_pair" : "" }
            wealthy_dict[wealthy_number_key]["amount_in_usd"] = agents[i].currentUSDValueOfWallet
            wealthy_dict[wealthy_number_key]["strategy"] = agents[i].strategy.name
            wealthy_dict[wealthy_number_key]["num_of_transactions"] = 10 # not implemented yet
            wealthy_dict[wealthy_number_key]["most_traded_currency_pair"] = "ETH/USDT" # not implemented yet
        return wealthy_dict

    def getWealthDistributionByStrategy(self):
        random_agents = self.agents_using_each_strategy_dict["random"]
        moving_avg_agents = self.agents_using_each_strategy_dict["pivot_point"]
        pivot_point_agents = self.agents_using_each_strategy_dict["moving_average"]
        macd_agents = self.agents_using_each_strategy_dict["macd"]
        rsi_agents = self.agents_using_each_strategy_dict["rsi"]
        wealth_distribution_data = {
            "wealth_distribution_random": 0,
            "wealth_distribution_pivot_point": 0,
            "wealth_distribution_moving_average": 0,
            "wealth_distribution_macd": 0,
            "wealth_distribution_rsi": 0
        }
        wealth_distribution_data["wealth_distribution_random"] = sum(agent.currentUSDValueOfWallet for agent in random_agents)
        wealth_distribution_data["wealth_distribution_moving_average"] = sum(agent.currentUSDValueOfWallet for agent in moving_avg_agents)
        wealth_distribution_data["wealth_distribution_pivot_point"] = sum(agent.currentUSDValueOfWallet for agent in pivot_point_agents)
        wealth_distribution_data["wealth_distribution_macd"] = sum(agent.currentUSDValueOfWallet for agent in macd_agents)
        wealth_distribution_data["wealth_distribution_rsi"] = sum(agent.currentUSDValueOfWallet for agent in rsi_agents)
        return wealth_distribution_data

    # desperatily needs to be cleaned !!! Perhaps BLEACHED!!!
    def simplifyOrderBook(self, order_book_data):
        orders = {
            "ETH/USDT:USDT/ETH" : { 'ETH/USDT' : {}, 'USDT/ETH' : {} },
            "ETH/BNB:BNB/ETH" : { 'ETH/BNB' : {}, 'BNB/ETH' : {} },
            "ETH/BTC:BTC/ETH" : { 'ETH/BTC' : {}, 'BTC/ETH' : {} },
            "BNB/BTC:BTC/BNB" : { 'BNB/BTC' : {}, 'BTC/BNB' : {} },
            "BNB/USDT:USDT/BNB" :{ 'BNB/USDT' : {}, 'USDT/BNB' : {} },
            "BTC/USDT:USDT/BTC" : { 'BTC/USDT' : {}, 'USDT/BTC' : {} },
        }
        for item in order_book_data.items():
            symbol_orders = order_book_data[item[0]]
            for order in symbol_orders:
                if symbol_orders[order]:
                    i = 0
                    for agent_key in symbol_orders[order].keys():
                        value_array = symbol_orders[order][agent_key]
                        amount = value_array[0]
                        limit_price = value_array[-1]
                        exchange_price = 1 / limit_price
                        temp = {"amount":amount, "limit_price":limit_price, "exchange_price": exchange_price}
                        orders[item[0]][order][i] = temp
                        i += 1
        return orders

    def getInitialOrderbookTable(self):
        return {
            "ETH/USDT:USDT/ETH" : { 'ETH/USDT' : {}, 'USDT/ETH' : {} },
            "ETH/BNB:BNB/ETH" : { 'ETH/BNB' : {}, 'BNB/ETH' : {} },
            "ETH/BTC:BTC/ETH" : { 'ETH/BTC' : {}, 'BTC/ETH' : {} },
            "BNB/BTC:BTC/BNB" : { 'BNB/BTC' : {}, 'BTC/BNB' : {} },
            "BNB/USDT:USDT/BNB" :{ 'BNB/USDT' : {}, 'USDT/BNB' : {} },
            "BTC/USDT:USDT/BTC" : { 'BTC/USDT' : {}, 'USDT/BTC' : {} },
        }
# --------------------------------------------------------------------------

# import os 

# if __name__ == "__main__":
#     cwd = os.getcwd()

    # url = "file://" + cwd + "/index.html" # must be changed to own files location
    # webbrowser.open(url,new=2)
    # model = MarketModel()
    # for i in range(2):
    #     model.step()

    # os.remove("transactionData.JSON")
    # os.remove("/Users/alexisdumon/Desktop/PRJ/AgentBasedModellingBlockchain/wealthDistributionData.JSON")
    # os.remove("/Users/alexisdumon/Desktop/PRJ/AgentBasedModellingBlockchain/wealthiestAgentsData.JSON")
    # os.remove("/Users/alexisdumon/Desktop/PRJ/AgentBasedModellingBlockchain/orderBookData.JSON")

