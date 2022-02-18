from mesa import Model
from mesa.time import RandomActivation, BaseScheduler
from mesa.datacollection import DataCollector
import pandas as pd
from investment_strategies import Strategy
from agents import MarketAgent
from currency_market import CurrencyMarket, Currency

def getNumberOfEthereumTransactions(model) :
    return model.listOfCurrencies[0].getNumOfTransactions()

def totalTransactions(model):
    total = 0
    for currency in model.listOfCurrencies:
        total += currency.getNumOfTransactions()
    return total

def getTetherPrice(model):
    return model.listOfCurrencies[1].getPriceAtRound(model.round)

def getEthereumPrice(model):
    return model.listOfCurrencies[0].getPriceAtRound(model.round)

ethereumData = pd.read_csv('Data/cleanedEuthereumData.csv')
tetherData = pd.read_csv('Data/cleanedTetherData.csv')

class MarketModel(Model):
    def __init__(self, num_agents = 10):
        self.round = 0 # index keeping count of the round of simulation

        ethereum = Currency("ethereum", "USD/ETH", "crypto", 100, ethereumData)
        tether = Currency('tether', "USD/USDT", "fiat-backed", 100, tetherData)
        self.listOfCurrencies = []
        self.listOfCurrencies.append(ethereum)
        self.listOfCurrencies.append(tether)

        self.currencyMarket = CurrencyMarket(self.listOfCurrencies)

        self.schedule = RandomActivation(self) # changed from RandomActivation

        self.agents = [] # list that contains all MarketAgent objects
        self.createAgents(num_agents) #

        #### for DATA collection ### 
        self.datacollector = DataCollector(
            model_reporters = {
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
        strategy = Strategy()
        for i in range(num_agents): 
            a = MarketAgent(i, self, strategy, self.currencyMarket) # does nothing for now... 
            self.schedule.add(a)
            self.agents.append(a)

    def step(self):
        self.currencyMarket.updateExchangeRates(self.round) # makes sure all exchange rates are up to date (IMPORTANT)
        
        self.schedule.step() # runs the step method for all Agents
        
        print ("OrderBook BEFORE transactions: ")
        self.currencyMarket.getOrderBook().printOrderBook() # to know what the order book looks like before transactions
        self.currencyMarket.price_clearing_mechanism()
        print ("OrderBook AFTER transactions: ")
        self.currencyMarket.getOrderBook().printOrderBook()

        for i in self.agents:
            print(i, ", wallet: ", i.wallet)
            print (i.currentUSDValueOfWallet, ", diff: ", i.currentUSDValueOfWallet - i.initialUSDValueOfWallet)

        self.datacollector.collect(self)

        self.round += 1 # go to the next round

        print ("-------- A step has happened -------------")

    def getCurrRound(self):
        return self.round
    
    def getCurrencyMarket(self):
        return self.currencyMarket

# --------------------------------------------------------------------------

model = MarketModel(1)
for i in range(5):
    model.step()


print("")
print("END RESULT:")
