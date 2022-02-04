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
    "ETH/USDT" : ["ethereum", "tether"],
    "USDT/ETH" : ["tether", "ethereum"]
}


class CurrencyMarket:
    """
        Object that contains information necessary for AGENTS to make orders and transact with one another
    """
    def __init__(self, listOfCurrencies):
        self.marketIndicators = marketIndicators # hard coded as fuck 
        self.currencies = listOfCurrencies
        self.exchange_rates = {"ETH/USDT" : 0, "USDT/ETH" : 0}
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
    # this is the worst function ever written in the history of programming :(((((((
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

                    # PROBLEM WITH IF condition amount == other_amount
                    if ( other_exchange_rate == exchangeRate and order_id not in orders_checked and otherId not in orders_checked):
                        
                        """
                            they have agreed on a price to exchange --> they now have to agree on an amount of exchange ...
                            both agents have a desired amount of the currency they want to buy
                            agentKey: wants 10 ETH --> 7730 USDT
                            otherAgentKey: wants 10 USDT --> 0.12 ETH
                            Will not match agentKey will need to sell more Tethers to fulfill their order // wait for other agents
                        """
                        # NEED TO CHECK IF THESE ARE TRUE
                        amountOfOtherCurrencyRequiredToSell = amount * exchangeRate 
                        otherAmountOfOtherCurrencyRequiredToSell = otherAmount / other_exchange_rate

                        # agentKey buys == otherAgent required to sell and agentKey required to sell == otheragent buys
                        if amount == otherAmountOfOtherCurrencyRequiredToSell and amountOfOtherCurrencyRequiredToSell == otherAmount:
                            # everything matched -- perfect exchange
                            agentKey.wallet[currency_wanted] += amount
                            agentKey.wallet[currency_selling] -= amountOfOtherCurrencyRequiredToSell

                            otherAgentKey.wallet[other_currency_wanted] += otherAmount
                            otherAgentKey.wallet[other_currency_selling] -= otherAmountOfOtherCurrencyRequiredToSell
                            
                            orders_checked.append(order_id)
                            orders_checked.append(otherId)
                            primaryKeysToDelete.append(agentKey)
                            secondaryKeysToDelete.append(otherAgentKey)
                            
                            if order_type == "OPEN":
                                agentKey.openTransactionWasSuccessfull = True
                            else: agentKey.closingTransactionWasSuccessfull = True
                            if other_order_type == "OPEN":
                                otherAgentKey.openTransactionWasSuccessfull = True
                            else: otherAgentKey.closingTransactionWasSuccessfull = True

                        # agentKey -- wants a bigger exchange; otherAgentKey satisfied but not AgentKey
                        elif amount > otherAmountOfOtherCurrencyRequiredToSell and amountOfOtherCurrencyRequiredToSell > otherAmount: 
                            agentKey.wallet[currency_wanted] += otherAmountOfOtherCurrencyRequiredToSell
                            agentKey.wallet[currency_selling] -= otherAmount

                            otherAgentKey.wallet[other_currency_wanted] += otherAmount
                            otherAgentKey.wallet[other_currency_selling] -= otherAmountOfOtherCurrencyRequiredToSell
                            
                            amount -= otherAmountOfOtherCurrencyRequiredToSell
                            order[1][0] -= otherAmountOfOtherCurrencyRequiredToSell
                            currentOrderAgentKey = agentKey.currentOrder.getOrder()
                            currentOrderAgentKey[3] = amount - otherAmountOfOtherCurrencyRequiredToSell

                            orders_checked.append(otherId)
                            secondaryKeysToDelete.append(otherAgentKey)
                            if other_order_type == "OPEN":
                                otherAgentKey.openTransactionWasSuccessfull = True
                            else: otherAgentKey.closingTransactionWasSuccessfull = True


                        # otherAgentKey -- wants a bigger exchange; agentKey satisfied but not otherAgentKey
                        elif amount < otherAmountOfOtherCurrencyRequiredToSell and amountOfOtherCurrencyRequiredToSell < otherAmount:
                            agentKey.wallet[currency_wanted] += amount
                            agentKey.wallet[currency_selling] -= amountOfOtherCurrencyRequiredToSell

                            otherAgentKey.wallet[other_currency_wanted] += amountOfOtherCurrencyRequiredToSell
                            otherAgentKey.wallet[other_currency_selling] -= amount

                            otherAmount -= amountOfOtherCurrencyRequiredToSell
                            otherOrder[1][0] -= amountOfOtherCurrencyRequiredToSell
                            otherAgentKeyCurrentOrder = otherAgentKey.currentOrder.getOrder()
                            otherAgentKeyCurrentOrder[3] = otherAmount - amountOfOtherCurrencyRequiredToSell

                            orders_checked.append(order_id)
                            primaryKeysToDelete.append(agentKey)
                            if order_type == "OPEN":
                                agentKey.openTransactionWasSuccessfull = True
                            else: agentKey.closingTransactionWasSuccessfull = True

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
    """
        this will eventually be a superclass whose children have different implementations of the four methods
        each children will therefore represent a different type of strategy
    """
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

        symbol = currencyPairs[buyCurrency.getName()][sellCurrency.getName()]
        exchange_rate = agent.currencyMarket.getAllExchangeRates()[symbol]
        amountOfSellingCurrency = exchange_rate  # How much does it need to sell in order to get 10 of other currency
        amountOfBuyingCurrency = random.choice(range(2,10)) # AGENT WANTS TO BUY 10 of currency

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
        
        symbol = currencyPairs[buyCurrency.getName()][sellCurrency.getName()]
        exchange_rate = agent.currencyMarket.getAllExchangeRates()[symbol]

        expiration_time = random.choice([2,3,4,5])
        return Order("CLOSE", buyCurrency, sellCurrency, amountOfBuyingCurrency, amountOfSellingCurrency, round, agent, exchange_rate, expiration_time, self.order_id)

    """ agent will have to change the desired exchange_rate of their order if it did not go through """
    def updateOrder(self, order):
        order = order.getOrder()
        # find what currency pair the order is for ie. X/Y
        buyCurrency = order[1]
        sellCurrency = order[2]
        agent = order[6]

        exchange_rate = agent.currencyMarket.getExchangeRate(buyCurrency, sellCurrency, agent.model.round)

        currencyPair = currencyPairs[buyCurrency.getName()][sellCurrency.getName()]
        exchangeSymbol = currencyPair # what is the exchange symbol e.g. "ETH/USDT"
        exchangeDirection = currencyPairs[buyCurrency.getName()]["direction"] # is it a buy or sell with respect to first currency

        # append it as a key-value pair
        self.orders[exchangeSymbol][exchangeDirection][agent][5] = exchange_rate 

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
            if self.currentOrder.expiration_time > 0:
                self.currentOrder.expiration_time -= 1
                # self.currencyMarket.getOrderBook().updateOrder(self.currentOrder)
            else:
                self.initialiseParameters()
        elif self.hasMadeOpenOrder and self.openTransactionWasSuccessfull:
            self.currentInvestment = self.currentOrder # the order was fullfilled it has become an investment (agents wallet updated)
            if not self.hasMadeClosingOrder: # if you have still not made an order to close your investment
                if self.strategy.closingConditionMet(self, self.model.round): # check if conditions to close are met (enough time has elapse / price is right / stop loss etc...)
                    self.makeOrder("CLOSE") # make the order (should be selling exact amount bought)
            elif self.closingTransactionWasSuccessfull: # if you have made a closing order and it was successful (ie. transaction happened)
                    self.initialiseParameters()
        elif self.hasMadeOpenOrder and not self.openTransactionWasSuccessfull:            
            if self.currentOrder.expiration_time > 0:
                self.currentOrder.expiration_time -= 1
                # self.currencyMarket.getOrderBook().updateOrder(self.currentOrder)
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
        elif orderType == "CLOSE":
            self.currentOrder = self.strategy.makeCloseOrder(self, 1)
        
        self.currencyMarket.getOrderBook().addOrder(self.currentOrder)
