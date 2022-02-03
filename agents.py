# from re import S
from mesa import Agent
import random
import copy
import pandas as pd

# should be updated at every turn
marketIndicators = {
                "ethereum" : { 'moving_average_1' : 10, 'moving_average_5' : 5, 'moving_average_10' : 2 },
            }

currencyPairs = {
    "ethereum" : {
        "tether": "ETH/USDT",
        "direction": "buy" # if you have ethereum to tether then you are buying eth and selling usdt
    },
    "tether": {
        "ethereum" : "ETH/USDT",
        "direction": "sell" # you are buying tether with ethereum
    }
}

inverseCurrencyPair = {
    "ETH/USDT" : ["ethereum", "tether"]
}


class CurrencyMarket:
    """
        Object that contains information necessary for AGENTS to make orders and transact with one another
    """
    def __init__(self, listOfCurrencies):
        self.marketIndicators = marketIndicators # hard coded as fuck 
        self.currencies = listOfCurrencies
        self.exchange_rates = {"ETH/USDT" : 0}
        self.orderBook = OrderBook()
        
    def getAvailableCurrencies(self):
        return self.currencies
    
    def updateMarketIndicators(self, currency):
        self.findMovingAverages(currency)
    
    def getMarketIndicators(self):
        return self.marketIndicators
    
    def getOrderBook(self):
        return self.orderBook

    # HARD REFACTOR NEEDED --> this is awful
    def updateExchangeRates(self, round):
        # for all possible combinations of currencies what is the exchange rate
        for symbols in inverseCurrencyPair:
            currencies = inverseCurrencyPair[symbols]
            currency1 = currencies[0]
            currency2 = currencies[1]
            
            for currency in self.currencies:
                if currency.getName() == currency1:
                    currency1 = currency
                elif currency.getName() == currency2:
                    currency2 = currency

            self.exchange_rates[symbols] = self.getExchangeRate(currency1, currency2, round)

        return "27"
    
    def getAllExchangeRates(self):
        return self.exchange_rates

    def getExchangeRate(self, currency1, currency2, round):
        """ 1 currency1 == X currency2 at round X"""
        price_currency1 = currency1.getPriceAtRound(round)
        price_currency2 = currency2.getPriceAtRound(round)
        exchange_rate = price_currency1 / price_currency2 # 1 USD in both currencies, then 1 USD worth of curr 1 equal to 1 USD worth of curr 2
        return exchange_rate

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
        orderbook = self.getOrderBook()
        for currencyPairs in orderbook.getOrders():
            orders = orderbook.getOrders()[currencyPairs]
            buyOrders = orders["buy"]
            sellOrders = orders["sell"]
            
            primaryKeysToDelete = [] # lists of the keys of the orders to delete
            secondaryKeysToDelete = []
            orders_checked = [] # list of order_id of orders already checked for a match

            # see if there is a match in the order Book
            # a match is two Orders with same currency pair where the amount that can exchaged is the same
            for order in buyOrders.items():
                agentKey = order[0]
                value = order[1]

                amount = value[0]
                order_id = value[1]
                currency_wanted = value[2]
                currency_selling = value[3]
                order_type = value[4]
                exchangeRate = value[5]

                for otherOrder in sellOrders.items():
                    otherAgentKey = otherOrder[0]
                    otherValue = otherOrder[1]

                    otherAmount = otherValue[0]
                    otherId = otherValue[1]
                    other_currency_wanted = otherValue[3]
                    other_currency_selling = otherValue[2]
                    other_order_type = otherValue[4]
                    other_exchange_rate = otherValue[5]
                    
                    print ("currency wanted: ", currency_wanted, ", currency_selling: ", currency_selling)
                    print ("OTHER, currency wanted: ", other_currency_wanted, ", currency_selling: ", other_currency_selling)
                    # PROBLEM WITH IF condition amount == other_amount
                    if (currency_wanted == other_currency_selling and currency_selling == other_currency_wanted
                            and other_exchange_rate == exchangeRate 
                            and order_id not in orders_checked and otherId not in orders_checked):
                        orders_checked.append(order_id)
                        orders_checked.append(otherId)
                        primaryKeysToDelete.append(agentKey)
                        secondaryKeysToDelete.append(otherAgentKey)

                        # update the wallets of the respective agents !!!
                        # this is where exchange rate should come into play ... 
                        # exchangeRate = 2
                        
                        # at the moment amount and other_amount always equal 10
                        agentKey.wallet[currency_wanted] += 10
                        agentKey.wallet[currency_selling] -= 10 * exchangeRate 
                        
                        otherAgentKey.wallet[other_currency_selling] -= 10
                        otherAgentKey.wallet[other_currency_wanted] += 10 * exchangeRate

                        # make successfultransaction true
                        if order_type == "OPEN":
                            agentKey.openTransactionWasSuccessfull = True
                        else: agentKey.closingTransactionWasSuccessfull = True
                        if other_order_type == "OPEN":
                            otherAgentKey.openTransactionWasSuccessfull = True
                        else: otherAgentKey.closingTransactionWasSuccessfull = True

            for i in primaryKeysToDelete:
                del buyOrders[i]

            for i in secondaryKeysToDelete:
                del sellOrders[i]
                    


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
        
        currenciesInWallet = list(agentWallet.keys())
        sellCurrency = random.choice(currenciesInWallet) # currency agent has in its wallet that he wants to exchange (selling this to buy)

        currencies = agent.currencyMarket.getAvailableCurrencies() # list of available currencies in the market
        buyCurrency = None
        while buyCurrency == None:
            potentialCurrency = random.choice(currencies)
            if potentialCurrency != sellCurrency:
                buyCurrency = potentialCurrency
        
        self.order_id += 1

        symbol = currencyPairs[buyCurrency][sellCurrency]
        exchange_rate = agent.currencyMarket.getAllExchangeRates()[symbol]

        amountOfSellingCurrency = 10 # How much does it need to sell in order to get 10 of other currency
        amountOfBuyingCurrency = 10 # AGENT WANTS TO BUY 10 of currency

        expiration_time = random.choice([2,3,4,5])

        return Order("OPEN", buyCurrency, sellCurrency, amountOfBuyingCurrency, amountOfSellingCurrency, round, agent, exchange_rate, expiration_time, self.order_id) # creates an ORDER


    def closingConditionMet(self, agent, round):
        """" Agent's strategy for when to close the position """
        return True

    def makeCloseOrder(self, agent, round):
        """ wishes to exchange Y for X """
        self.order_id += 1

        investmentToClose = agent.currentInvestment.getOrder() # close current investment // investment is an Order object
        
        buyCurrency = investmentToClose[2]
        sellCurrency = investmentToClose[1]
        amountOfSellingCurrency = investmentToClose[2] # 
        amountOfBuyingCurrency = investmentToClose[3] #
        
        symbol = currencyPairs[buyCurrency][sellCurrency]
        exchange_rate = agent.currencyMarket.getAllExchangeRates()[symbol]

        expiration_time = random.choice([2,3,4,5])
        return Order("CLOSE", buyCurrency, sellCurrency, amountOfBuyingCurrency, amountOfSellingCurrency, round, agent, exchange_rate, expiration_time, self.order_id)

class Order:
    """
        a data structure containing all the relevant information for the order request of an agent
    """
    def __init__(self, orderType, buyCurrency, sellCurrency, amountOfBuyingCurrency, amountOfSellingCurrency, round, agent, exchange_rate, expiration_time, order_id):
        self.order_type = orderType
        self.buyCurrency = buyCurrency # currency agent wants to buy
        self.sellCurrency = sellCurrency # currency agent will sell in order to buy
        self.amountOfBuyingCurrency = amountOfBuyingCurrency # amount of buy currency agent wants to own :: DEPEND ON EXCHANGE_RATE
        self.amountOfSellingCurrency = amountOfSellingCurrency # amount of sell currency agents needs to sell
        self.timestep = round # 
        self.agent = agent #
        self.expiration_time = expiration_time
        self.order_id = order_id
        self.exchange_rate = exchange_rate
        self.order = [self.order_type, self.buyCurrency, self.sellCurrency, self.amountOfBuyingCurrency, self.amountOfSellingCurrency, self.timestep, self.agent, self.exchange_rate, self.expiration_time, self.order_id]

    def getOrder(self):
        return self.order
    
    def getExpirationTime(self):
        return self.order[8]

class OrderBook:
    """ 
        data structure which assembles order objects into a useful dictionary
        orderbook = { 
            "ETH/USDT" : 
                {
                    "buy": { "agent1": [10, 1027, ethereum], "agent2": [12, 1027, ethereum] },
                    "sell" : { "agent3": [10, 1027, tether], "agent4": [12, 1027, tether] }
                },
            "BTC/ETH" :
                {
                    "buy": { "agent1": [10, 1027, bitcoin], "agent2": [12, 1027, bitcoin]},
                    "sell" : { "agent3": [10, 1027, ethereum], "agent4": [12, 1027, ethereum] }
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
        orderType = order[0]
        buyCurrency = order[1]
        sellCurrency = order[2]
        amount = order[3]
        agent = order[6]
        exchange_rate = order[7]
        order_id = order[-1]

        currencyPair = currencyPairs[buyCurrency.getName()][sellCurrency.getName()]
        exchangeSymbol = currencyPair # what is the exchange symbol e.g. "ETH/USDT"
        exchangeDirection = currencyPairs[buyCurrency.getName()]["direction"] # is it a buy or sell with respect to first currency

        # append it as a key-value pair
        self.orders[exchangeSymbol][exchangeDirection][agent] = [amount, order_id, buyCurrency, sellCurrency, orderType, exchange_rate] # later will add price

    def getOrders(self):
        return self.orders
    
    def printOrderBook(self):
        """ visual representation of order book """
        print(self.orders.items())

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
            self.wallet[currency] = 100000 # start with 100 000 of both currencies

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
                    self.makeOrder("CLOSE") # make the order (should be selling exact amount bought)
            elif self.closingTransactionWasSuccessfull: # if you have made a closing order and it was successful (ie. transaction happened)
                    self.initialiseParameters()
                    # ^ reinitialise all parameters -- restart loop
        elif self.hasMadeOpenOrder and not self.openTransactionWasSuccessfull:
            timeLeft = self.currentOrder.getExpirationTime()
            print("time left: ", timeLeft)
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

# ethereumData = pd.read_csv('cleanedEuthereumData.csv')
# tetherData = pd.read_csv('cleanedTetherData.csv')
# ethereum = Currency("ethereum", "USD/ETH", "crypto", 100, ethereumData)
# tether = Currency('tether', "USD/USDT", "fiat-backed", 100, tetherData)
# listOfCurrencies = []
# listOfCurrencies.append(ethereum)
# listOfCurrencies.append(tether)

# currencyMarket = CurrencyMarket(listOfCurrencies)
# print("exchange rate at round 1: ",currencyMarket.getExchangeRate(ethereum, tether, 1))
# print("exchange rate at round 33: ",currencyMarket.getExchangeRate(ethereum, tether, 33))
# print("exchange rate at round 227: ",currencyMarket.getExchangeRate(ethereum, tether, 227))
# print ("oops")