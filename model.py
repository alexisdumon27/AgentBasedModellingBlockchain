from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import pandas as pd
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

        self.currencies = Currencies(self)

        for i in range(self.num_agents): 
            a = MarketAgent(i, self)
            self.schedule.add(a)
        
        self.running = True

        self.datacollector.collect(self)

    

    def step(self):
        self.round += 1 # next round of simulation -- price of ETH needs to be updated
        # print ("ETH: ", self.currencies.getEuthereumPrice())
        # print ("USDT: ", self.currencies.getTetherPrice())

        self.sellers = [x for x in self.schedule.agents if x.currentObjective == "SELL"]
        self.buyers = [x for x in self.schedule.agents if x.currentObjective == "BUY"]

        self.schedule.step() # runs the step method for all Agents

        for potentialBuyer in self.buyers:

            if len(self.sellers) > 0:

                chosenSeller = self.sellers[:len(self.sellers)][0]
                potentialBuyer.amountOfGoods -= 1
                potentialBuyer.wallet -= 1

                chosenSeller.amountOfGoods += 1
                chosenSeller.wallet += 1
                self.sellers = self.sellers[1:]

                self.numOfTransactions += 1

        self.datacollector.collect(self)
        print ("-------- A step has happened -------------")

# class that defines the currency market
# has methods to get information about the different currencies in the market
# like: how much they have changed by, their value compared to the fiat-currency
class Currencies:
    
    def __init__(self, model : MarketModel) -> None:
        self.model = model
        self.euthereumPrice = pd.read_csv('cleanedEuthereumData.csv')['USD/ETH'].values
        self.tetherPrice = pd.read_csv('cleanedTetherData.csv')['USD/USDT'].values
        pass
    
    def getEuthereumPrice(self):
        return self.euthereumPrice[self.model.round]

    def getTetherPrice(self):
        return self.tetherPrice[self.model.round]

    def refreshPrices():
        return {a:1, b:2, c:3} 



model = MarketModel(20)
for i in range(10):
    model.step()
    getNumberOfTransactions(model)