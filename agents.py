from re import S
from mesa import Agent
import random
import copy
import pandas as pd

# from model import MarketModel

# ethereumData = pd.read_csv('cleanedEuthereumData.csv')
# tetherData = pd.read_csv('cleanedTetherData.csv')

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

    # NEEDS HEAVVVYYYY REFACTORING !!!!!!!!!!!!! 
    # this is the worst function ever written
    def overseeTransactions(self):
        """ matches oldest open orders with oldest close orders with the same currency """
        print("enters the function")
        orders = self.getOrderBook().getOrders()
        
        for i in range(len(orders)):
            if (len(orders) == 0): break

            order1 = orders[i].getOrder()
            order1Object = orders[i]
            agent1 = order1[6] 
            order1Buying = order1[1]
            order1Selling = order1[2]   
            order1AmountBuying = order1[3]
            order1AmountSelling = order1[4]

            for j in range(len(orders)):
                if (i == j): continue
                order2 = orders[j].getOrder()
                order2Object = orders[j]

                order2Buying = order2[1]
                order2Selling = order2[2]
                order2AmountBuying = order2[3]
                order2AmountSelling = order2[4]
                if (order1Buying == order2Selling and order1Selling == order2Buying and order1AmountBuying == order2AmountSelling 
                    and order1AmountSelling == order2AmountBuying):
                    agent2 = order2[6]
                    
                    # add / remove from the wallets
                    agent1.wallet[order1Buying] += order1AmountBuying
                    agent1.wallet[order1Selling] -= order1AmountSelling

                    agent2.wallet[order2Buying] += order2AmountBuying
                    agent2.wallet[order2Selling] -= order2AmountSelling

                    # remove both orders from orderbook
                    self.getOrderBook().getOrders().remove(order1Object)
                    self.getOrderBook().getOrders().remove(order2Object)

                    # make successfultransaction true
                    if order1[0] == "OPEN":
                        agent1.openTransactionWasSuccessfull = True
                    else: agent1.closingTransactionWasSuccessfull = True
                    if order2[0] == "OPEN":
                        agent2.openTransactionWasSuccessfull = True
                    else: agent2.closingTransactionWasSuccessfull = True

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

    # HARD refactor needed later :)  
    def makeOpenOrder(self, agent, round):
        """ wishes to exchange X for Y """
        agentWallet = agent.wallet
        currencies = copy.copy(agent.currencyMarket.getAvailableCurrencies())
        randomCurrency = random.choice(currencies)

        buyCurrency =  randomCurrency # currency agent uses to invest
        currencies.remove(randomCurrency)

        sellCurrency = random.choice(currencies) # currency agent invests in

        self.order_id += 1

        exchangeRate = 1
        amountOfSellingCurrency = 10 # will need to be calculated
        amountOfBuyingCurrency = 10 * exchangeRate # will need to be calculated
        expiration_time = random.choice([2,3,4,5])
        return Order("OPEN", buyCurrency, sellCurrency, amountOfBuyingCurrency, amountOfSellingCurrency, round, agent, expiration_time, self.order_id) # creates an ORDER


    def closingConditionMet(self, agent, round):
        """" Agent's strategy for when to close the position"""
        return True

    def makeCloseOrder(self, agent, round):
        """ wishes to exchange Y for X """
        self.order_id += 1

        investmentToClose = agent.currentInvestment.getOrder() # close current investment // investment is an Order object
        
        exchangeRate = 1 # will be given by a function exchange(currency1, currency2)

        buyCurrency = investmentToClose[1]
        sellCurrency = investmentToClose[0]
        amountOfSellingCurrency = investmentToClose[2]
        amountOfBuyingCurrency = investmentToClose[3] * exchangeRate
        
        expiration_time = random.choice([2,3,4,5])
        return Order("CLOSE", buyCurrency, sellCurrency, amountOfBuyingCurrency, amountOfSellingCurrency, round, agent, expiration_time, self.order_id)

class Order:
    """
        a data structure containing all the relevant information for the order request of an agent
    """
    def __init__(self, orderType, buyCurrency, sellCurrency, amountOfBuyingCurrency, amountOfSellingCurrency, round, agent, expiration_time, order_id):
        self.order_type = orderType
        self.buyCurrency = buyCurrency # currency agent wants to buy
        self.sellCurrency = sellCurrency # currency agent will sell in order to buy
        # self.buyPrice = buyPrice # current price of buy currency
        self.amountOfBuyingCurrency = amountOfBuyingCurrency # amount of buy currency agent wants to own :: DEPEND ON EXCHANGE_RATE
        self.amountOfSellingCurrency = amountOfSellingCurrency # amount of sell currency agents needs to sell
        self.timestep = round # 
        self.agent = agent #
        self.expiration_time = expiration_time
        self.order_id = order_id
        self.order = [self.order_type, self.buyCurrency, self.sellCurrency, self.amountOfBuyingCurrency, self.amountOfSellingCurrency, self.timestep, self.agent, self.expiration_time, self.order_id]

    def getOrder(self):
        return self.order
    
    def getExpirationTime(self):
        return self.order[8]

currencyPairs = {
    "ethereum" : {
        "tether": "ETH/USDT", "direction": "buy" # if you have ethereum to tether then you are buying eth and selling usdt
    },
    "tether": {
        "ethereum" : "ETH/USDT", "direction": "sell" # you are buying tether with ethereum
    }
}

class OrderBook:
    """ 
        data structure which assembles order objects into a useful dictionary
        orderbook = { 
            "ETH/USDT" : 
                {
                    "buy": { "agent1": [10, 1027], "agent2": [12, 1027] },
                    "sell" : { "agent3": [10, 1027], "agent4": [12, 1027] }
                },
            "BTC/ETH" :
                {
                    "buy": { "agent1": [10, 1027], "agent2": [12, 1027]},
                    "sell" : { "agent3": [10, 1027], "agent4": [12, 1027] }
                },
        }
    """

    def __init__(self) -> None:
        self.orders = {"ETH/USDT" : {"buy":{}, "sell":{}}} # all possible currency pairs

    def addOrder(self, order):
        """
            adds an order object into self.orders {}
        """
        order = order.getOrder()
        # find what currency pair the order is for ie. X/Y
        buyCurrency = order[1]
        sellCurrency = order[2]
        amount = order[3]
        agent = order[6]
        order_id = order[-1]

        currencyPair = currencyPairs[buyCurrency][sellCurrency]
        exchangeSymbol = currencyPair # what is the exchange symbol "ETH/USDT"
        exchangeDirection = currencyPairs[buyCurrency]["direction"] # is it a buy or sell with respect to first currency

        # append it as a key-value pair
        self.orders[exchangeSymbol][exchangeDirection][agent] = [amount, order_id] # later will add price
        # self.orders.append(order)

    def getOrders(self):
        return self.orders
    
    def printOrderBook(self):
        """ visual representation of order book """
        print(self.orders.items())


orderbook = OrderBook()

orderbook.addOrder(Order("CLOSE", "ethereum", "tether", 10, 10, 1, "agent1", 2, 1))
orderbook.addOrder(Order("CLOSE", "tether", "ethereum", 10, 10, 1, "agent2", 2, 2))
orderbook.addOrder(Order("OPEN", "ethereum", "tether", 10, 10, 1, "agent3", 2, 3))
orderbook.addOrder(Order("OPEN", "tether", "ethereum", 10, 10, 1, "agent4", 2, 4))
orderbook.addOrder(Order("OPEN", "ethereum", "tether", 10, 10, 1, "agent5", 2, 5))
orderbook.addOrder(Order("OPEN", "ethereum", "tether", 10, 10, 1, "agent6", 2, 6))

orderbook.printOrderBook()





for currencyPairs in orderbook.getOrders():
    print ("currency pair: ", currencyPairs)
    orders = orderbook.getOrders()[currencyPairs]
    buyOrders = orders["buy"]
    sellOrders = orders["sell"]

    # see if there is a match ...
    primaryOrderList = buyOrders
    secondaryOrderList = sellOrders
    if len(buyOrders) <= len(sellOrders):
        primaryOrderList = sellOrders
        secondaryOrderList = buyOrders
    
    primaryKeysToDelete = []
    secondaryKeysToDelete = []

    orders_checked = []
    for order in primaryOrderList.items():
        key = order[0]
        value = order[1]

        amount = value[0]
        order_id = value[1]
        print ("WHAT: ", value)
        for otherOrder in secondaryOrderList.items():
            otherKey = otherOrder[0]
            otherValue = otherOrder[1]
            otherAmount = otherValue[0]
            otherId = otherValue[1]

            if amount == otherAmount and order_id not in orders_checked and otherId not in orders_checked:
                orders_checked.append(order_id)
                orders_checked.append(otherId)
                primaryKeysToDelete.append(key)
                secondaryKeysToDelete.append(otherKey)
                # how to keep which to delete
                

    print (primaryKeysToDelete)
    print (secondaryKeysToDelete)
    print("before: ", orderbook.getOrders())

    print (buyOrders.keys())
    for i in primaryKeysToDelete:
        del primaryOrderList[i]

    for i in secondaryKeysToDelete:
        del secondaryOrderList[i]

    print ("after: ", orderbook.getOrders())    

class MarketAgent:

    def __init__(self, unique_id, model, strategy, currencyMarket):
        self.unique_id = unique_id
        self.model = model
        self.currencyMarket = currencyMarket

        # randomly initialised fields
        self.strategy = strategy

        self.hasMadeOpenOrder = False
        self.hasMadeClosingOrder = False
        self.openTransactionWasSuccessfull = False
        self.closingTransactionWasSuccessfull = False

        self.currentInvestment = None
        self.currentOrder = None

        self.wallet = {}
        self.createWallet()
    
    def createWallet(self):
        for currency in self.currencyMarket.getAvailableCurrencies():
            self.wallet[currency] = 27 

    # what happens during one round of the simulation for one agent
    ## a limited amount of agents get to perform their step actions per turn 
    def step(self):
        """ if it was chosen as a trading agent this turn; then it adds an order to the order book list """
        
        if not self.hasMadeOpenOrder:
            self.makeOrder("OPEN")
            # currentOrder is also updated
            self.hasMadeOpenOrder = True
        elif self.hasMadeOpenOrder and self.openTransactionWasSuccessfull:
            self.currentInvestment = self.currentOrder # the order was fullfilled it has become an investment (agents wallet updated)
            if not self.hasMadeClosingOrder: # if you have still not made an order to close your investment
                if self.strategy.closingConditionMet(self, self.model.round): # check if conditions to close are met (enough time has elapse / price is right / stop loss etc...)
                    self.makeOrder(" CLOSE") # make the order (should be selling exact amount bought)
            elif self.closingTransactionWasSuccessfull: # if you have made a closing order and it was successful (ie. transaction happened)
                    self.initialiseParameters()
                    # ^ reinitialise all parameters -- restart loop
        elif self.hasMadeOpenOrder and not self.openTransactionWasSuccessfull:
            timeLeft = self.currentOrder.getExpirationTime()
            if timeLeft > 0:
                timeLeft -= 1
            else: # they made an order to close then stay ... 
                self.initialiseParameters()

    def initialiseParameters(self):
        self.hasMadeOpenOrder = False
        self.hasMadeClosingOrder = False
        self.openTransactionWasSuccessfull = False
        self.closingTransactionWasSuccessfull = False
        self.currentInvestment = None
        self.currentOrder = None

    def makeOrder(self, orderType):
        # looks at what strategy returns // will be abstracted by currencyMarket and strategy object
        if orderType == "OPEN":
            self.currentOrder = self.strategy.makeOpenOrder(self, 1)
        else:
            self.currentOrder = self.strategy.makeCloseOrder(self, 1)
        
        self.currencyMarket.getOrderBook().addOrder(self.currentOrder)
