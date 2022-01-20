from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import pandas as pd
from tornado.autoreload import _reload_on_update
from agents import ModelAgent, MarketAgent
import random

def getNumberOfTransactions(model) :
        return model.numOfTransactions
        # return random.randint(0, 27)

class MarketModel(Model):
    def __init__(self, num_agents = 10):
        self.round = 0 # what round we are at in the simulation
        
        self.num_agents = num_agents
        self.numOfTransactions = 0

        self.schedule = RandomActivation(self)
        self.datacollector = DataCollector(
            model_reporters = {"num_of_transactions" : getNumberOfTransactions}
        )

        self.sellers = None
        self.buyers = None

        self.currencyMarket = CurrencyMarket(self)

        self.createAgents(num_agents)
    
        self.running = True

        self.datacollector.collect(self)

    def createAgents(self, num_agents):
        for i in range(self.num_agents): 
            a = MarketAgent(i, self, self.currencyMarket) # does nothing for now... 
            self.schedule.add(a)

    def step(self):
        self.round += 1

        self.currencyMarket.getCurrentPrices(self.round)

        self.sellers = [x for x in self.schedule.agents if x.currentObjective == "SELL"]
        self.buyers = [x for x in self.schedule.agents if x.currentObjective == "BUY"]

        self.schedule.step() # runs the step method for all Agents

        for potentialBuyer in self.buyers:

            if len(self.sellers) > 0:

                chosenSeller = self.sellers[:len(self.sellers)][0]
                potentialBuyer.amountOfGoods -= 1
                # potentialBuyer.wallet -= 1

                chosenSeller.amountOfGoods += 1
                # chosenSeller.wallet += 1
                self.sellers = self.sellers[1:]

                self.numOfTransactions += 1

        self.datacollector.collect(self)
        print ("-------- A step has happened -------------")

# --------------------------------------------------------------------------

euthereum = pd.read_csv('cleanedEuthereumData.csv')
tether = pd.read_csv('cleanedTetherData.csv')

class CurrencyMarket:

    def __init__(self, model):
        self.model = model
        
        self.currency1 = Currency("ethereum", "crypto", 100, euthereum)
        self.currency2 = Currency("tether", "fiat-backed", 100, tether)
        
        self.currencies = []
        self.currencies.append(self.getCurrency1())
        self.currencies.append(self.getCurrency2())
    
    def getAvailableCurrencies(self):
        return self.currencies

    def getCurrency1(self):
        return self.currency1

    def getCurrency2(self):
        return self.currency2

    def calculateCurrencyFluctuations(self, currency, timeFrame):
        return 1.01
    
    def getCurrentRound(self):
        return self.model.round

    def getCurrentPrices(self, round):
        prices = {}
        prices['ethereum'] = euthereum['USD/ETH'].values[round]
        prices['tether'] = tether['USD/USDT'].values[round]

        print (prices)
        return prices

class Currency:

    def __init__(self, name, type, amountInCirculation, data):
        self.name = name
        self.type = type
        self.amountInCirculation = amountInCirculation
        self.data = data
    
    def getCurrentPriceInUSD(self, round):
        return self.data[round]    
    
    def totalValueOfCirulatingAmount(self, round):
        return self.amountInCirculation * self.getCurrentPriceInUSD(round)

    def getData(self):
        return self.data
    
    def getName(self):
        return self.name

# currencyMarket = CurrencyMarket(MarketModel)
# print(currencyMarket.getCurrency1().getData())
# print(currencyMarket.getCurrency2().getData())


model = MarketModel(3)
for i in range(2):
    model.step()