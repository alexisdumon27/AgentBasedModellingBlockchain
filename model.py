from mesa import Model
from mesa.time import RandomActivation, BaseScheduler
from mesa.datacollection import DataCollector
import pandas as pd
from investment_strategies import MACDStrategy, MovingAverageStrategy, PivotPointStrategy, RSIStrategy, Strategy, RandomStrategy
from agents import MarketAgent
from currency_market import CurrencyMarket, Currency
from dataCollectorMethods import *

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

        self.bnb_usd = exchange_rates["BNB/USD"][self.round]
        self.bnb_usdt = exchange_rates["BNB/USDT"][self.round]
        self.bnb_eth = exchange_rates["BNB/ETH"][self.round]
        self.bnb_btc = exchange_rates["BNB/BTC"][self.round]

        self.currency_0 = currency_0
        self.currency_1 = currency_1
        self.desired_exchange_rate = exchange_rates[self.currency_0 + "/" + self.currency_1][self.round]

        #### for DATA collection ### 
        self.datacollector = DataCollector(
            model_reporters = {
                                "BNB/USD" : getBNBtoUS,
                                "BNB/USDT" : getBNBtoUSDT,
                                "BNB/BTC" : getBNBtoBTC,
                                "BNB/ETH" : getBNBtoETH,
                                "desired_exchange" : getDesiredExchangeRate,

                                # "ETH/USD" : getBNBDollarPrice,
                                # "BTC/USD" : getBNBDollarPrice,
                                # "USDT/USD" : getBNBDollarPrice,
                                # "most_traded_currency_pair" : getMostTradedCurrPair,
                                # "ten_most_wealthy_investors" : getMostWealthy,

                                
                                # "9_day_EMA_BNB/USDT": getBNB_9_day,
                                # "12_day_EMA_BNB/BTC": ,
                                # "26_day_EMA_BNB/ETH" ,

                                # "num_of_transactions" : totalTransactions,
                                # "num_of_ethereum_transactions": getNumberOfEthereumTransactions,
                                # "tether_price": getTetherPrice,
                                # "ethereum_price": getEthereumPrice,
                            },
            agent_reporters= {
                "Wallets" : "wallet"
            }
        )
        self.running = True
        self.datacollector.collect(self)

    def createAgents(self, num_agents):
        random_strategy = RandomStrategy("Random strategy", exchange_rates)
        pivot_point_strategy = PivotPointStrategy("Pivot point strategy", exchange_rates)
        moving_average_strategy = MovingAverageStrategy("Moving average strategy", exchange_rates)
        macd_strategy = MACDStrategy('MACD Strategy', exchange_rates)
        rsi_strategy = RSIStrategy("RSI Strategy", exchange_rates)

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
        
        self.bnb_usd = exchange_rates["BNB/USD"][self.round]
        self.bnb_usdt = exchange_rates["BNB/USDT"][self.round]
        self.bnb_btc = exchange_rates["BNB/BTC"][self.round]
        self.bnb_eth = exchange_rates["BNB/ETH"][self.round]
        # self.currency_0 = 
        self.desired_exchange_rate = exchange_rates[self.currency_0 + "/" + self.currency_1][self.round]

        self.schedule.step() # runs the step method for all Agents
        
        self.currency_market.orderBook.sortOrdersInOrderBook()

        # print ("OrderBook BEFORE transactions: ")
        # self.currency_market.getOrderBook().printOrderBook() # to know what the order book looks like before transactions

        self.currency_market.price_clearing_mechanism() # do all transactions

        # print ("OrderBook AFTER transactions: ")
        # self.currency_market.getOrderBook().printOrderBook()

        # for i in self.agents:
        #     print(i, ", wallet: ", i.wallet)
        #     print ("wallet value: ", i.currentUSDValueOfWallet, ", diff: ", i.currentUSDValueOfWallet - i.initialUSDValueOfWallet)

        self.datacollector.collect(self)

        self.round += 1 # go to the next round

        # print ("-------- A step has happened -------------")
    
# --------------------------------------------------------------------------

# model = MarketModel(100)
# for i in range(1000):
#     print (i)
#     model.step()


print("")
print("END RESULT")
