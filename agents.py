from mesa import Agent
import random
import pandas as pd

# from model import MarketModel

ethereumData = pd.read_csv('cleanedEuthereumData.csv')

# should be updated at every turn
marketIndicators = {
                "ethereum" : { 'moving_average_1' : 10, 'moving_average_5' : 5, 'moving_average_10' : 2 },
            }

class CurrencyMarket:

    def __init__(self, listOfCurrencies):
        self.marketIndicators = marketIndicators # hard coded as fuck 
        self.currencies = listOfCurrencies
        self.orderBook = OrderBook()
        
    def getAvailableCurrencies(self):
        return self.currencies
    
    def updateMarketIndicators(self, currency):
        self.findMovingAverages(currency)
    
    def getMarketIndicators(self):
        return self.marketIndicators

    def getCurrentRound(self):
        return self.model.round
    
    def getOrderBook(self):
        return self.orderBook

    # INDICATORS
    def calcMovingAverage(self, currency, currentRound, spread):
        """ spread: how many steps back do you want to calculate the moving average for """
        total = 0
        startRound = currentRound - spread
        for round in range(startRound, currentRound):
            total += currency.getPriceAtRound(round)
        moving_average = total / spread
        return moving_average

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

class Strategy:
    def __init__(self):
        self.order_id = 0
        pass
        
    def getOrder(self, agent, round, availableCurrencies, amountOfCurrency):
        """ returns a random order with random currency for a specific agent """
        if not agent.hasMadeOrder:
            self.order_id += 1
            orderType = random.choice(['OPEN', 'CLOSE'])
            chosenCurrency = random.choice(availableCurrencies)
            return [orderType, chosenCurrency, round, self.order_id, agent.unique_id, amountOfCurrency] # creates an ORDER
        else: return None

class Order:
    """ 
        data structure defining order objects 
        {   
            "OPEN" :  {ethereum : { 1 : { agent_id : 1, amountOfCurrency : 2, timestep : 1 }, 2 : { agent_id : 1, amountOfCurrency : 2, timestep : 1 } }
            "CLOSE" :  {ethereum : { 3 :  { agent_id : 1, amountOfCurrency : 2, timestep : 1 } } }
        }
    """
    def __init__(self, orderType, currency, round, order_id, agent_id, amount ) -> None:
        self.orderType = orderType
        self.currency = currency
        self.timestep = round
        self.order_id = order_id
        self.agent_id = agent_id
        self.order = [self.orderType, self.currency, self.timestep, self.order_id, self.agent_id]

    def getOrder(self):
        return self.order
        
class OrderBook:
    """ 
        an order book is a data structure that aims to facilitate matching SELLERS and BUYERS of the different currencies
        Orderbook holds multiple Order objects
    """
    def __init__(self) -> None:
        self.orders = {"OPEN" : {}, "CLOSE" : {}}

    """" wtf am i trying to do ???? """
    def appendOrderBook(self, order):
        if order[0] == "OPEN":
            if order[1] in self.orders["OPEN"].keys():
                self.orders["OPEN"][order[1]][order.order_id] = order
            else:
                self.orders["OPEN"][order[1]] = {order.order_id}
                self.orders["OPEN"][order[1]][order.order_id] = order 

    def getOrders(self):
        return self.orders


class MarketAgent:

    def __init__(self, unique_id, strategy, model, currencyMarket, wallet):
        self.unique_id = unique_id
        self.model = model
        self.currencyMarket = currencyMarket

        # randomly initialised fields
        self.strategy = strategy
        self.hasMadeOrder = False    # this one can remain unrandomised for a bit    
        self.wallet = wallet
    
    def createWallet(self):
        wallet = {}
        for currency in self.currencyMarket.getAvailableCurrencies().getName():
            wallet[currency] = 2.7 # for now fixed amount of both currencies!!!
        return wallet

    # what happens during one round of the simulation for one agent
    ## a limited amount of agents get to perform their step actions per turn 
    def step(self):
        """ if it was chosen as a trading agent this turn; then it adds an order to the order book list """

        newOrder = self.strategy.getOrder(self, self.model.round, list(self.wallet.keys()), 27)

        self.hasMadeOrder = True
        self.currencyMarket.getOrderBook().appendOrderBook(newOrder)
        

# listOfDataCurrencies = []
# ethereum = Currency('ethereum', "USD/ETH", "crypto", 100, ethereumData)
# listOfDataCurrencies.append(ethereum)
# currencyMarket = CurrencyMarket(listOfDataCurrencies)

# agent1 = MarketAgent(1, Strategy(), MarketModel, currencyMarket, {'ethereum' : 27})
# agent2 = MarketAgent(2, Strategy(), MarketModel, currencyMarket, {'ethereum' : 27})
# agent1.step()
# agent2.step()