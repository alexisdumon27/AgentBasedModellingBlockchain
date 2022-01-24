from enum import unique
from mesa import Agent, Model, agent
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from numpy import Infinity
import pandas as pd
from pandas.io.formats.format import TextAdjustment
from tornado.autoreload import _reload_on_update
from agents import ModelAgent, MarketAgent
import random
import copy

def getNumberOfTetherTransactions(model) :
    return model.listOfCurrencies[1].getNumOfTransactions()

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

ethereumData = pd.read_csv('cleanedEuthereumData.csv')
tetherData = pd.read_csv('cleanedTetherData.csv')

listOfDataOfCurrencies = []
listOfDataOfCurrencies.append(ethereumData)
listOfDataOfCurrencies.append(tetherData)

class MarketModel(Model):
    def __init__(self, num_agents = 10):
        self.round = 0 # what round we are at in the simulation

        ethereum = Currency("ethereum", "USD/ETH", "crypto", 100, ethereumData)
        tether = Currency("tether", "USD/USDT", "fiat-backed", 100, tetherData)

        self.listOfCurrencies = []
        self.listOfCurrencies.append(ethereum)
        self.listOfCurrencies.append(tether)

        self.currencyMarket = CurrencyMarket(self, self.listOfCurrencies)

        self.schedule = RandomActivation(self)

        self.num_agents = num_agents

        self.datacollector = DataCollector(
            model_reporters = {
                                "num_of_transactions" : totalTransactions,
                                "num_of_tether_transactions": getNumberOfTetherTransactions,
                                "num_of_ethereum_transactions": getNumberOfEthereumTransactions,
                                "tether_price": getTetherPrice,
                                "ethereum_price": getEthereumPrice,
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

        self.sellers = [x for x in self.agents if x.currentObjective == "SELL"]
        self.buyers = [x for x in self.agents if x.currentObjective == "BUY"]
        self.currencyMarket.findLeastFluctuatingCurrency(self.round)
        
        self.schedule.step() # runs the step method for all Agents

        self.datacollector.collect(self)
        print ("-------- A step has happened -------------")

# --------------------------------------------------------------------------


class CurrencyMarket:

    def __init__(self, model, listOfCurrencies):
        self.model = model
        self.currencies = listOfCurrencies
        self.leastFluctuatingCurrency = None
        self.findLeastFluctuatingCurrency(0)

    def getAvailableCurrencies(self):
        return self.currencies
    
    # will need to be refactored AF (does two things )
    def getLeastFluctuatingCurrency(self):
        """ returns currency object """
        return self.leastFluctuatingCurrency

    # REFACTOR
    def getProbabilisticCurrencyChoice(self, currency):
        indices = []
        index = self.currencies.index(currency)
        for i in range(len(self.currencies)):
            if (index == i):
                indices.append(i)
                indices.append(i)
            indices.append(i)
        randomIndex = random.choice(indices)
        return self.currencies[randomIndex]


    def findLeastFluctuatingCurrency(self, round):
        smallestDiff = Infinity
        for currency in self.currencies:
            initPrice = currency.getPriceAtRound(0)
            currPrice = currency.getPriceAtRound(round)
            diff = abs(currPrice - initPrice)
            if (diff < smallestDiff):
                self.leastFluctuatingCurrency = currency
                smallestDiff = diff
        
    def getCurrentRound(self):
        return self.model.round

class Currency:

    def __init__(self, name, conversionSymbol, type, amountInCirculation, data):
        self.name = name
        self.conversionSymbol = conversionSymbol
        self.type = type
        self.amountInCirculation = amountInCirculation
        self.data = data
        self.transactions = 0

    def getPriceAtRound(self, round):
        return self.data[self.conversionSymbol].values[round]

    def getData(self):
        return self.data
    
    def getName(self):
        return self.name
    
    def getType(self):
        return self.type
    
    def getNumOfTransactions(self):
        return self.transactions
    
    def addTransaction(self):
        self.transactions += 1


model = MarketModel(10)
for i in range(5):
    model.step()