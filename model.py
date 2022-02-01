from enum import unique
from mesa import Agent, Model, agent
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from numpy import Infinity
import pandas as pd
from agents import MarketAgent, Currency, CurrencyMarket, Strategy
import random
import copy

from agents import Strategy

# def getNumberOfTetherTransactions(model) :
#     return model.listOfCurrencies[1].getNumOfTransactions()

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

class MarketModel(Model):
    def __init__(self, num_agents = 10):
        self.round = 0 # what round we are at in the simulation

        ethereum = Currency("ethereum", "USD/ETH", "crypto", 100, ethereumData)
        tether = Currency('tether', "USD/USDT", "fiat-backed", 100, tetherData)
        self.listOfCurrencies = []
        self.listOfCurrencies.append(ethereum)
        self.listOfCurrencies.append(tether)

        self.currencyMarket = CurrencyMarket(self.listOfCurrencies)

        self.schedule = RandomActivation(self)

        self.num_agents = num_agents

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

        self.agents = {}

        self.createAgents(num_agents)
    
        self.running = True

        self.datacollector.collect(self)

    def createAgents(self, num_agents):
        strategy = Strategy()
        for i in range(self.num_agents): 
            a = MarketAgent(i, self, strategy, self.currencyMarket) # does nothing for now... 

            self.schedule.add(a)
            self.agents[i] = a

    def step(self):
        self.round += 1
        
        self.schedule.step() # runs the step method for all Agents
        self.currencyMarket.getOrderBook().printOrderBook()
        self.currencyMarket.overseeTransactions()
        for i in self.schedule.agents:
            print(i.wallet)

        self.datacollector.collect(self)
        print ("-------- A step has happened -------------")

# --------------------------------------------------------------------------


model = MarketModel(5)
for i in range(3):
    model.step()

print("")
print("END RESULT:")
