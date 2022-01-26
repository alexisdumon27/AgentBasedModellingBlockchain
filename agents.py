from mesa import Agent
import random
import pandas as pd

# from model import MarketModel

# from model import MarketModel

ethereumData = pd.read_csv('cleanedEuthereumData.csv')

# should be updated at every turn
marketIndicators = {
                "ethereum" : { 'moving_average_1' : 10, 'moving_average_5' : 5, 'moving_average_10' : 2 },
            }

class CurrencyMarket:
    """
        Object that contains information necessary for AGENTS to make orders and transact with one another
    """
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

    # very HARDCODED FOR NOW !!!! 
    def overseeTransaction(self):
        openOrders = self.orderBook.getOpenOrders()
        closeOrders = self.orderBook.getCloseOrders()

        if 'ethereum' in list(closeOrders.keys()) and 'ethereum' in list(openOrders.keys()):
            ethereumOpenOrders = openOrders["ethereum"]
            for openOrder in ethereumOpenOrders:
                if len(closeOrders['ethereum']) > 0:
                    closingOrder = closeOrders["ethereum"][0]
                    amount = openOrder["amount"]
                    openOrderAgent = openOrder["agent"]
                    closeOrderAgent = closingOrder["agent"] # will always get earliest closing order
                    openOrderAgent.wallet['ethereum'] += amount
                    closeOrderAgent.wallet['ethereum'] -= amount

                    openOrders['ethereum'].remove(openOrder)
                    closeOrders["ethereum"].remove(closingOrder)

                    openOrderAgent.hasMadeOrder = False
                    closeOrderAgent.hasMadeOrder = False

        return 27

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
        if agent.hasMadeOrder == False:
            self.order_id += 1
            orderType = random.choice(['OPEN', 'CLOSE'])
            chosenCurrency = random.choice(availableCurrencies)
            return Order(orderType, chosenCurrency, round, self.order_id, agent, amountOfCurrency) # creates an ORDER
        else: None

class Order:
    """
        a data structure containing all the relevant information for the order request of an agent
    """
    def __init__(self, orderType, currency, round, order_id, agent, amount ):
        self.orderType = orderType
        self.currency = currency
        self.timestep = round
        self.order_id = order_id
        self.agent = agent
        self.amount = amount
        self.order = [self.orderType, self.currency, self.timestep, self.agent, amount, self.order_id]

    def getOrder(self):
        return self.order

class OrderBook:
    """ 
        data structure which assembles order objects into a useful dictionary
        dict = { 
            "OPEN" :  {"ethereum" : 
                [ 
                    { "timestep" : 1, "agent" : MarketAgent, "amount" : 2, "order_id" : 1 },
                    { "timestep" : 1, "agent" : MarketAgent, "amount" : 2, "order_id" : 2 },
                    { "timestep" : 2, "agent" : MarketAgent, "amount" : 2, "order_id" : 3 }
                ]
            },
            "CLOSE" :  {"ethereum" : 
                [ 
                    { "timestep" : 1, "agent" : MarketAgent, "amount" : 2, "order_id" : 4 },
                    { "timestep" : 1, "agent" : MarketAgent, "amount" : 2, "order_id" : 5 },
                    { "timestep" : 2, "agent" : MarketAgent, "amount" : 2, "order_id" : 6 }
                ]
            }
        }
    """
    def __init__(self) -> None:
        self.orders = {"OPEN" : {}, "CLOSE" : {}}

    def addOrder(self, order):
        """
            adds an order object into the dictionary (['CLOSE', 'ethereum', 1, 2, 1, 2])
        """
        type = order.orderType
        currency = order.currency
        timestep = order.timestep
        order_id = order.order_id
        agent = order.agent
        amount = order.amount

        if currency in self.orders[type].keys():
            self.orders[type][currency].append({"timestep" : timestep, "agent" : agent, "amount" : amount, "order_id": order_id})
        else:
            self.orders[type][currency] = []
            self.orders[type][currency].append({"timestep" : timestep, "agent" : agent, "amount" : amount, "order_id": order_id})

    def removeOrder(self, order):
        return 27

    def getOrders(self):
        return self.orders
    
    def getOpenOrders(self):
        return self.orders["OPEN"]

    def getCloseOrders(self):
        return self.orders["CLOSE"]


class MarketAgent:

    def __init__(self, unique_id, strategy, currencyMarket):
        self.unique_id = unique_id
        # self.model = model
        self.currencyMarket = currencyMarket

        # randomly initialised fields
        self.strategy = strategy
        self.hasMadeOrder = False    # this one can remain unrandomised for a bit
        self.currentOrder = None    
        self.wallet = {'ethereum' : 27}
    
    def createWallet(self):
        wallet = {}
        for currency in self.currencyMarket.getAvailableCurrencies().getName():
            wallet[currency] = 2.7 # for now fixed amount of both currencies!!!
        return wallet

    # what happens during one round of the simulation for one agent
    ## a limited amount of agents get to perform their step actions per turn 
    def step(self):
        """ if it was chosen as a trading agent this turn; then it adds an order to the order book list """

        newOrder = self.strategy.getOrder(self, 1, list(self.wallet.keys()), 27)
        if not newOrder == None:
            self.hasMadeOrder = True
            self.currentOrder = newOrder.orderType
            self.currencyMarket.getOrderBook().addOrder(newOrder)
        

strategy = Strategy()

listOfDataCurrencies = []
ethereum = Currency('ethereum', "USD/ETH", "crypto", 100, ethereumData)
listOfDataCurrencies.append(ethereum)
currencyMarket = CurrencyMarket(listOfDataCurrencies)

agent1 = MarketAgent(1, strategy, currencyMarket)
agent2 = MarketAgent(2, strategy, currencyMarket)
agent3 = MarketAgent(3, strategy, currencyMarket)
agent4 = MarketAgent(4, strategy, currencyMarket)

agent1.step()
agent2.step()
agent3.step()

print ("First ROUND: ")
print("OPEN: ", currencyMarket.getOrderBook().getOpenOrders())
print("CLOSE: ", currencyMarket.getOrderBook().getCloseOrders())

currencyMarket.overseeTransaction()
currencyMarket.overseeTransaction()

# agent1.step()
# agent2.step()
# agent3.step()

print ("Second ROUND: ")

print("OPEN: ", currencyMarket.getOrderBook().getOpenOrders())
print("CLOSE: ", currencyMarket.getOrderBook().getCloseOrders())