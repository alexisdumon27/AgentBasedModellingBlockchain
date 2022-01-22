from enum import unique
from mesa import Agent, Model, agent
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from numpy import Infinity
import pandas as pd
from tornado.autoreload import _reload_on_update
from agents import ModelAgent, MarketAgent
import random

def getNumberOfTransactions(model) :
    return model.numOfTransactions

def getNumberOfTetherTransactions(model):
    return model.numOfTetherTransactions

def getNumberOfEthereumTransactions(model):
    return model.numOfEthereumTransactions

def getTetherPrice(model):
    return model.tetherPrice

def getEthereumPrice(model):
    return model.ethereumPrice

class MarketModel(Model):
    def __init__(self, num_agents = 10):
        self.round = 0 # what round we are at in the simulation
        
        self.currencyMarket = CurrencyMarket(self)
        self.schedule = RandomActivation(self)

        self.num_agents = num_agents
        self.numOfTransactions = 0
        self.numOfTetherTransactions = 0
        self.numOfEthereumTransactions = 0
        self.tetherPrice = self.currencyMarket.getTetherPrice(self.round)
        self.ethereumPrice = self.currencyMarket.getEthereumPrice(self.round)

        
        self.datacollector = DataCollector(
            model_reporters = {"num_of_transactions" : getNumberOfTransactions,
                                "num_of_tether_transactions": getNumberOfTetherTransactions,
                                "num_of_ethereum_transactions": getNumberOfEthereumTransactions,
                                "tether_price": getTetherPrice,
                                "ethereum_price": getEthereumPrice
                            },
            agent_reporters= {
                "Wallets" : "wallet"
            }
        )

        self.sellers = None
        self.buyers = None

        self.agents = []

        self.createAgents(num_agents)
    
        self.running = True

        self.datacollector.collect(self)

    def createAgents(self, num_agents):
        for i in range(self.num_agents): 
            a = MarketAgent(i, self, self.currencyMarket) # does nothing for now... 

            self.schedule.add(a)
            self.agents.append(a)

    def step(self):
        self.round += 1

        self.sellers = [x for x in self.schedule.agents if x.currentObjective == "SELL"]
        self.buyers = [x for x in self.schedule.agents if x.currentObjective == "BUY"]

        self.schedule.step() # runs the step method for all Agents
        
        # will need to refactor
        self.tetherPrice = self.currencyMarket.getTetherPrice(self.round)
        self.ethereumPrice = self.currencyMarket.getEthereumPrice(self.round)
        print ("tether: ", self.tetherPrice)
        print ("ethereum: ", self.ethereumPrice)

        self.datacollector.collect(self)
        print ("-------- A step has happened -------------")

    def addTetherTransaction(self):
        self.numOfTetherTransactions += 1
        return self.numOfTetherTransactions

    def addEthereumTransaction(self):
        self.numOfEthereumTransactions += 1
        return self.numOfEthereumTransactions
    
    def addTransaction(self):
        self.numOfTransactions += 1
        return self.numOfTransactions

# --------------------------------------------------------------------------

ethereumData = pd.read_csv('cleanedEuthereumData.csv')
tetherData = pd.read_csv('cleanedTetherData.csv')

class CurrencyMarket:

    def __init__(self, model):
        self.model = model
        
        self.ethereum = Currency("ethereum", "crypto", 100, ethereumData)
        self.tether = Currency("tether", "fiat-backed", 100, tetherData)
        
        self.currencies = []
        self.currencies.append(self.ethereum)
        self.currencies.append(self.tether)
    
    def getAvailableCurrencies(self):
        return self.currencies

    def getTetherPrice(self, round):
        return self.tether.data['USD/USDT'].values[round]

    def getEthereumPrice(self, round):
        return self.ethereum.data['USD/ETH'].values[round]

    def calculateCurrencyFluctuations(self, currency, timeFrame):
        return 1.01
    
    # will need to be refactored AF
    def leastFluctuatingCurrency(self, round):

        initTetherPrice = self.getTetherPrice(0)
        currTetherPrice = self.getTetherPrice(round)
        tetherDiff = abs(currTetherPrice - initTetherPrice)

        initEthereumPrice = self.getEthereumPrice(0)
        currEthereumPrice = self.getEthereumPrice(round)
        ethereumDiff = abs(currEthereumPrice - initEthereumPrice)

        if tetherDiff < ethereumDiff:
            return self.tether.getName()
        else: return self.ethereum.getName()


    def getCurrentRound(self):
        return self.model.round

    def getCurrentPrices(self, round):
        prices = {}
        # prices['ethereum'] = self.ethereum['USD/ETH'].values[round]
        # prices['tether'] = self.tether['USD/USDT'].values[round]
        return prices

class Currency:

    def __init__(self, name, type, amountInCirculation, data):
        self.name = name
        self.type = type
        self.amountInCirculation = amountInCirculation
        self.data = data
    
    # def getCurrentPriceInUSD(self, round):
        # return self.data['USD/'][round]    
    
    # def totalValueOfCirulatingAmount(self, round):
    #     return self.amountInCirculation * self.getCurrentPriceInUSD(round)

    def getData(self):
        return self.data
    
    def getName(self):
        return self.name
    
    def getType(self):
        return self.type

# market = CurrencyMarket(MarketModel)

model = MarketModel(3)
for i in range(5):
    model.step()