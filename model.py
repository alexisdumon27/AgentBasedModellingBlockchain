from mesa import Model
from mesa.time import RandomActivation, BaseScheduler
from mesa.datacollection import DataCollector
import pandas as pd
from investment_strategies import MACDStrategy, MovingAverageStrategy, PivotPointStrategy, RSIStrategy, Strategy, RandomStrategy
from agents import MarketAgent
from currency_market import CurrencyMarket, Currency
from dataCollectorMethods import *
import json

exchange_rates = pd.read_csv('Data/exchange_rates.csv')


# ethereumData = pd.read_csv('Data/cleanedEuthereumData.csv')
# tetherData = pd.read_csv('Data/cleanedTetherData.csv')

class MarketModel(Model):
    def __init__(self, num_agents = 10, currency_0 = "BNB", currency_1 = "BTC"):
        self.round = 10 # index keeping count of the round of simulation

        ethereum = Currency("Ethereum", "ETH", "crypto", 100, exchange_rates['ETH/USD'])
        tether = Currency('Tether', "USDT", "fiat-backed", 100, exchange_rates['USDT/USD'])
        binance = Currency('Binance', "BNB", "fiat-backed", 100, exchange_rates['BNB/USD'])
        bitcoin = Currency('Bitcoin', "BTC", "fiat-backed", 100, exchange_rates['BTC/USD'])
        
        self.list_of_currencies = []
        self.list_of_currencies.append(ethereum)
        self.list_of_currencies.append(tether)
        self.list_of_currencies.append(binance)
        self.list_of_currencies.append(bitcoin)

        self.currency_market = CurrencyMarket(self.list_of_currencies, exchange_rates)

        self.schedule = RandomActivation(self) # changed from RandomActivation

        self.agents = [] # list that contains all MarketAgent objects
        self.createAgents(num_agents) #

        #### for DATA collection ### 
        self.datacollector = DataCollector(
            model_reporters = {
                            },
            agent_reporters= {
                "Wallets" : "wallet"
            },
        )
        self.running = True
        self.datacollector.collect(self)

    def createAgents(self, num_agents):
        random_strategy = RandomStrategy("random", exchange_rates)
        pivot_point_strategy = PivotPointStrategy("pivot_point", exchange_rates)
        moving_average_strategy = MovingAverageStrategy("moving_average", exchange_rates)
        macd_strategy = MACDStrategy('macd', exchange_rates)
        rsi_strategy = RSIStrategy("rsi", exchange_rates)

        for i in range(num_agents): 
            strategy = random_strategy
            if i % 7 == 1:
                strategy = pivot_point_strategy
            elif i % 7 == 2:
                strategy = moving_average_strategy
            elif i % 7 == 3:
                strategy = macd_strategy
            elif i % 7 == 4:
                strategy = rsi_strategy

            a = MarketAgent(i, self, strategy, self.currency_market) # does nothing for now... 
            self.schedule.add(a)
            self.agents.append(a)

    def step(self):
        self.schedule.step() # runs the step method for all Agents
        
        self.currency_market.order_book.sortOrdersInOrderBook()

        self.currency_market.price_clearing_mechanism() # do all transactions

        order_book_data = self.currency_market.getOrderBook().orders
        simplified_order_book = self.simplifyOrderBook(order_book_data)
        with open('orderBookData.JSON', 'w') as json_file:
            json.dump(simplified_order_book, json_file)

        transaction_data = {
            # num of transactions with each currency # easy to calculate aggregated results # graph
            "num_transactions_eth_usdt" : [1, 2, 3],
            "num_transactions_usdt_eth" : [4, 7, 7],
            "num_transactions_eth_bnb" : [5, 18, 27],
            "num_transactions_bnb_eth" : [3, 19, 33],
            "num_transactions_eth_btc" : [3, 29, 33],
            "num_transactions_btc_eth" : [2, 19, 21],
            "num_transactions_bnb_usdt" : [1, 19, 33],
            "num_transactions_usdt_bnb" : [3, 19, 33],
            "num_transactions_bnb_btc" : [3, 19, 12],
            "num_transactions_btc_bnb" : [3, 19, 37],
            "num_transactions_btc_usdt" : [0, 1, 3],
            "num_transactions_usdt_btc" : [0, 9, 10],
        }
        with open('transactionData.JSON', 'w') as json_file:
            json.dump(transaction_data, json_file)

        wealthiest_agents_data = {
            # top 10 wealthiest agents -- would be nice to make into a bar chart
            "wealthy_0" : {"amount_in_usd": 1027, "strategy": "strategy_name", "num_of_transactions":10, "most_traded_currency_pair" : "ETH/USDT" },
            "wealthy_1" : {"amount_in_usd": 927, "strategy": "strategy_name", "num_of_transactions":10, "most_traded_currency_pair" : "ETH/USDT" },
            "wealthy_2" : {"amount_in_usd": 827, "strategy": "strategy_name", "num_of_transactions":10, "most_traded_currency_pair" : "ETH/USDT" },
            "wealthy_3" : {"amount_in_usd": 727, "strategy": "strategy_name", "num_of_transactions":10, "most_traded_currency_pair" : "ETH/USDT" },
            "wealthy_4" : {"amount_in_usd": 627, "strategy": "strategy_name", "num_of_transactions":10, "most_traded_currency_pair" : "ETH/USDT" },
            "wealthy_5" : {"amount_in_usd": 527, "strategy": "strategy_name", "num_of_transactions":10, "most_traded_currency_pair" : "ETH/USDT" },
            "wealthy_6" : {"amount_in_usd": 427, "strategy": "strategy_name", "num_of_transactions":10, "most_traded_currency_pair" : "ETH/USDT" },
            "wealthy_7" : {"amount_in_usd": 327, "strategy": "strategy_name", "num_of_transactions":10, "most_traded_currency_pair" : "ETH/USDT" },
            "wealthy_8" : {"amount_in_usd": 227, "strategy": "strategy_name", "num_of_transactions":10, "most_traded_currency_pair" : "ETH/USDT" },
            "wealthy_9" : {"amount_in_usd": 127, "strategy": "strategy_name", "num_of_transactions":10, "most_traded_currency_pair" : "ETH/USDT" },
        }
        with open('wealthiestAgentsData.JSON', 'w') as json_file:
            json.dump(wealthiest_agents_data, json_file)

        wealth_distribution_data = {
            # wealth distribution per strategy relative to number of agents (Adds up to 100 pie chart!!!)
            "wealth_distribution_random": 40,
            "wealth_distribution_pivot_point": 20,
            "wealth_distribution_moving_average": 20,
            "wealth_distribution_macd": 10,
            "wealth_distribution_rsi": 10
        }
        
        with open('wealthDistributionData.JSON', 'w') as json_file:
            json.dump(wealth_distribution_data, json_file)
        
        self.datacollector.collect(self)
        self.round += 1 # go to the next round
    
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
# --------------------------------------------------------------------------

model = MarketModel(3)
for i in range(1):
    print (i)
    model.step()


print("")
print("END RESULT")
