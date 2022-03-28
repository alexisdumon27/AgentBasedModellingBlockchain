import random
from mesa import Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import pandas as pd
from investment_strategies import MACDStrategy, MovingAverageStrategy, PivotPointStrategy, RSIStrategy, Strategy, RandomStrategy
from agents import MarketAgent
from currency_market import CurrencyMarket
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

        self.list_of_agents_not_including_random = []
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
                "num_transactions_pivot_point_ETH/USDT:USDT/ETH": getNumOfTransactionsPivotPointETHUSDT,
                "num_transactions_pivot_point_ETH/BNB:BNB/ETH": getNumOfTransactionsPivotPointETHBNB,
                "num_transactions_pivot_point_ETH/BTC:BTC/ETH": getNumOfTransactionsPivotPointETHBTC,
                "num_transactions_pivot_point_BNB/BTC:BTC/BNB": getNumOfTransactionsPivotPointBNBBTC,
                "num_transactions_pivot_point_BNB/USDT:USDT/BNB": getNumOfTransactionsPivotPointBNBUSDT,
                "num_transactions_pivot_point_BTC/USDT:USDT/BTC": getNumOfTransactionsPivotPointBTCUSDT,   
                "num_transactions_moving_average_ETH/USDT:USDT/ETH": getNumOfTransactionsMovingAverageETHUSDT,
                "num_transactions_moving_average_ETH/BNB:BNB/ETH": getNumOfTransactionsMovingAverageETHBNB,
                "num_transactions_moving_average_ETH/BTC:BTC/ETH": getNumOfTransactionsMovingAverageETHBTC,
                "num_transactions_moving_average_BNB/BTC:BTC/BNB": getNumOfTransactionsMovingAverageBNBBTC,
                "num_transactions_moving_average_BNB/USDT:USDT/BNB": getNumOfTransactionsMovingAverageBNBUSDT,
                "num_transactions_moving_average_BTC/USDT:USDT/BTC": getNumOfTransactionsMovingAverageBTCUSDT,
                "num_transactions_rsi_ETH/USDT:USDT/ETH": getNumOfTransactionsRSIETHUSDT,
                "num_transactions_rsi_ETH/BNB:BNB/ETH": getNumOfTransactionsRSIETHBNB,
                "num_transactions_rsi_ETH/BTC:BTC/ETH": getNumOfTransactionsRSIETHBTC,
                "num_transactions_rsi_BNB/BTC:BTC/BNB": getNumOfTransactionsRSIBNBBTC,
                "num_transactions_rsi_BNB/USDT:USDT/BNB": getNumOfTransactionsRSIBNBUSDT,
                "num_transactions_rsi_BTC/USDT:USDT/BTC": getNumOfTransactionsRSIBTCUSDT,   
                "num_transactions_macd_ETH/USDT:USDT/ETH": getNumOfTransactionsMACDETHUSDT,
                "num_transactions_macd_ETH/BNB:BNB/ETH": getNumOfTransactionsMACDETHBNB,
                "num_transactions_macd_ETH/BTC:BTC/ETH": getNumOfTransactionsMACDETHBTC,
                "num_transactions_macd_BNB/BTC:BTC/BNB": getNumOfTransactionsMACDBNBBTC,
                "num_transactions_macd_BNB/USDT:USDT/BNB": getNumOfTransactionsMACDBNBUSDT,
                "num_transactions_macd_BTC/USDT:USDT/BTC": getNumOfTransactionsMACDBTCUSDT,       
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
                self.list_of_agents_not_including_random.append(a)
                
            self.schedule.add(a)
            agent_number += 1

    def step(self):
        print ("Is it different to 0.5? :", self.ratio_of_agents_engaged_each_turn)
        num_of_agents_per_turn = round(self.num_of_agents * self.ratio_of_agents_engaged_each_turn)
        for i in range(num_of_agents_per_turn):
            self.schedule.step() # runs the step method for all Agents

        self.currency_market.order_book.sortOrdersInOrderBook()

        self.currency_market.priceClearingMechanism() # do all transactions

        self.datacollector.collect(self)
        self.round += 1 # go to the next round
    
    def dateToRoundNumber(self, date):
        return 27

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



