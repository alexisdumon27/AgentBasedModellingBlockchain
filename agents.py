from mesa import Agent, agent
import random
from numpy import random
import numpy
import pandas as pd

# from model import MarketModel

#######
# self.currentOrder.getOrder()[3] -= amount <-- error :(
########

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

    def matchBuyAndSellOrders(self, buyOrders, sellOrders):
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

            # buy_side_currency = value[2]
            # selling_side_currency = value[3]

            currency_wanted = value[2] # you know that currency_wanted has to equal other_currency_selling
            currency_selling = value[3]

            order_type = value[4]
            limit_price = value[5]

            for otherOrder in sellOrders.items():
                otherAgentKey = otherOrder[0]
                otherValue = otherOrder[1]

                otherAmount = otherValue[0]
                otherId = otherValue[1]
                if otherId in orders_checked: continue

                other_currency_wanted = otherValue[2]
                other_currency_selling = otherValue[3]

                other_order_type = otherValue[4]
                other_limit_price = otherValue[5]

                # if they agree on the exchange rate and they have not engaged in the transaction yet
                if ( other_limit_price <= limit_price and order_id not in orders_checked and otherId not in orders_checked ):
                    """
                        A sell order of index j matches a buy order of index i, and
                        vice versa, only if other_limit_price ≤ limit_price, or if one of the two limit prices, or both, are equal to zero
                    """
                    # calculate the exchange
                    avg_price = (other_limit_price + limit_price) / 2
                    amountOfOtherCurrencyRequiredToSell = amount * avg_price 
                    otherAmountOfOtherCurrencyRequiredToSell = otherAmount / avg_price

                    # agentKey buys == otherAgent required to sell and agentKey required to sell == otheragent buys
                    if (amount == otherAmountOfOtherCurrencyRequiredToSell and amountOfOtherCurrencyRequiredToSell == otherAmount):
                        # everything matched -- perfect exchange
                        agentKey.updateWallet(currency_wanted, currency_selling, amount, amountOfOtherCurrencyRequiredToSell)
                        otherAgentKey.updateWallet(other_currency_wanted, other_currency_selling, otherAmount, otherAmountOfOtherCurrencyRequiredToSell)
                        
                        agentKey.updateOrderStatus(order_type) # Makes open/closing transaction successful TRUE
                        otherAgentKey.updateOrderStatus(other_order_type)

                        agentKey.updateCurrentInvestment(amount, currency_wanted, currency_selling) # Makes currentInvestment take amount as values
                        otherAgentKey.updateCurrentInvestment(otherAmount, other_currency_wanted, other_currency_selling)

                        # both will not be checked anymore
                        orders_checked.append(order_id)
                        orders_checked.append(otherId)
                        # will be removed from dictionary
                        primaryKeysToDelete.append(agentKey)
                        secondaryKeysToDelete.append(otherAgentKey)

                    # agentKey -- wants a bigger exchange; otherAgentKey satisfied but not AgentKey
                    elif (amount > otherAmountOfOtherCurrencyRequiredToSell and amountOfOtherCurrencyRequiredToSell > otherAmount): 
                        agentKey.updateWallet(currency_wanted, currency_selling, otherAmountOfOtherCurrencyRequiredToSell, otherAmount)
                        otherAgentKey.updateWallet(other_currency_wanted, other_currency_selling, otherAmount, otherAmountOfOtherCurrencyRequiredToSell)
                        
                        self.orderBook.updateOrder(order, otherAmountOfOtherCurrencyRequiredToSell)
                        
                        
                        agentKey.updateCurrentInvestment(otherAmountOfOtherCurrencyRequiredToSell, order)
                        otherAgentKey.updateCurrentInvestment(otherAmount, otherOrder)

                        agentKey.updateCurrentOrder(otherAmountOfOtherCurrencyRequiredToSell)

                        orders_checked.append(otherId)
                        secondaryKeysToDelete.append(otherAgentKey) # deletes order by the key it is attached too

                        otherAgentKey.updateOrderStatus(other_order_type) # 

                    # otherAgentKey -- wants a bigger exchange; agentKey satisfied but not otherAgentKey
                    elif (amount < otherAmountOfOtherCurrencyRequiredToSell and amountOfOtherCurrencyRequiredToSell < otherAmount):
                        agentKey.updateWallet(currency_wanted, currency_selling, amount, amountOfOtherCurrencyRequiredToSell)
                        otherAgentKey.updateWallet(other_currency_wanted, other_currency_selling, amountOfOtherCurrencyRequiredToSell, amount)

                        self.orderBook.updateOrder(otherOrder, amountOfOtherCurrencyRequiredToSell)
   
                        agentKey.updateCurrentInvestment(amount, order)
                        otherAgentKey.updateCurrentInvestment(amountOfOtherCurrencyRequiredToSell, otherOrder)
                        
                        otherAgentKey.updateCurrentOrder(amountOfOtherCurrencyRequiredToSell)

                        orders_checked.append(order_id)
                        primaryKeysToDelete.append(agentKey) # deletes order by the key it is attached too

                        agentKey.updateOrderStatus(order_type)
                    else:
                        return RuntimeError

        for i in primaryKeysToDelete:
            del buyOrders[i]

        for i in secondaryKeysToDelete:
            del sellOrders[i]

    # https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0164603&type=printable <- for reordering orderbook
    def price_clearing_mechanism(self):
        """ ............ """
        orderbook = self.getOrderBook()
        for currencyPairs in orderbook.getOrders():
            orders = orderbook.getOrders()[currencyPairs]
            buyOrders = orders["buy"]
            sellOrders = orders["sell"]
            
            self.matchBuyAndSellOrders(buyOrders, sellOrders)
                    
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
        self.order_id += 1

        agentWallet = agent.wallet
        currenciesInWallet = list(agentWallet.keys())
        sellCurrency = random.choice(currenciesInWallet) # currency agent has in its wallet that he wants to exchange (selling this to buy)

        currencies = agent.currencyMarket.getAvailableCurrencies() # list of available currencies in the market
        buyCurrency = None
        while buyCurrency == None:
            potentialCurrency = random.choice(currencies)
            if potentialCurrency != sellCurrency:
                buyCurrency = potentialCurrency
        
        symbol = currencyPairs[buyCurrency.getName()][sellCurrency.getName()]
        direction = currencyPairs[buyCurrency.getName()]["direction"]
        exchange_rate = agent.currencyMarket.getAllExchangeRates()[symbol]

        limit_price = self.getLimitPrice(direction, exchange_rate, buyCurrency, sellCurrency, agent.model.round)
        

        amountOfBuyingCurrency = random.choice(range(2,10)) # AGENT WANTS TO BUY 10 of currency

        expiration_time = random.choice([2,3,4,5])

        # AMOUNTOFSELLINGCURRENCY is useless here
        return Order("OPEN", buyCurrency, sellCurrency, amountOfBuyingCurrency, round, agent, limit_price, expiration_time, self.order_id) # creates an ORDER

    def closingConditionMet(self, agent, round):
        """" Agent's strategy for when to close the position """
        return True

    def getLimitPrice(self, direction, exchange_rate, currency1, currency2, round):
        deviation = random.choice([1, 1, 1, 1.01, 1.01, 1.02]) # to add randomness
        if direction == "buy":
            return exchange_rate * deviation # agent willing to buy at a slightly higher price
        else: 
            return exchange_rate / deviation # agent willing to sell at slightly lower price

    # https://arxiv.org/pdf/cond-mat/0103600.pdf
    def getRandomDrawFromGaussian(self, currency1, currency2, round):
        mean = 1.02
        constant = 2.5
        std_dev = self.getExchangeRateDeviation5Days(currency1, currency2, round)
        # For buy orders μ = 1.05, K = 2.5, σmin = 0.01 and σmax = 0.003.
        return numpy.random.normal(loc = mean, scale = std_dev)
    
    def getExchangeRateDeviation5Days(self, currency1, currency2, round):
        exchange_rates_list = []
        for i in range(5):
            if round - i < 0 : continue
            price_currency1 = currency1.getPriceAtRound(round - i)
            price_currency2 = currency2.getPriceAtRound(round - i)
            exchange_rate = price_currency1 / price_currency2 
            exchange_rates_list.append(exchange_rate)
        return numpy.std(exchange_rates_list)

    def makeCloseOrder(self, agent, round):
        """ wishes to exchange Y for X """
        self.order_id += 1

        investmentToClose = agent.currentInvestment # close current investment // investment is an Order object
        
        buyCurrency = investmentToClose["soldCurrency"] # currency you used to invest
        sellCurrency = investmentToClose["boughtCurrency"] # currency you invested in
        amountOfBuyingCurrency = investmentToClose["amount"] #
        
        symbol = currencyPairs[buyCurrency.getName()][sellCurrency.getName()]
        exchange_rate = agent.currencyMarket.getAllExchangeRates()[symbol]

        expiration_time = random.choice([2,3,4,5])
        return Order("CLOSE", buyCurrency, sellCurrency, amountOfBuyingCurrency, round, agent, exchange_rate, expiration_time, self.order_id)

class Order:
    """
        a data structure containing all the relevant information for the order request of an agent
    """
    def __init__(self, orderType, buyCurrency, sellCurrency, amountOfBuyingCurrency, round, agent, limit_price, expiration_time, order_id):
        self.order_type = orderType
        self.buyCurrency = buyCurrency # currency agent wants to buy
        self.sellCurrency = sellCurrency # currency agent will sell in order to buy
        self.amountOfBuyingCurrency = amountOfBuyingCurrency # amount of buy currency agent wants to own :: DEPEND ON EXCHANGE_RATE
        self.timestep = round # 
        self.agent = agent #
        self.expiration_time = expiration_time
        self.order_id = order_id
        self.limit_price = limit_price
        self.order = [self.order_type, self.buyCurrency, self.sellCurrency, self.amountOfBuyingCurrency, self.timestep, self.agent, self.limit_price, self.expiration_time, self.order_id]

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
        agent = order[5]
        limit_price = order[6]
        order_id = order[-1]

        currencyPair = currencyPairs[buyCurrency.getName()][sellCurrency.getName()]
        exchangeSymbol = currencyPair # what is the exchange symbol e.g. "ETH/USDT"
        exchangeDirection = currencyPairs[buyCurrency.getName()]["direction"] # is it a buy or sell with respect to first currency

        # append it as a key-value pair
        self.orders[exchangeSymbol][exchangeDirection][agent] = [amount, order_id, buyCurrency, sellCurrency, orderType, limit_price] # later will add price
        
        self.sortNewOrder(exchangeSymbol, exchangeDirection, orderType) # sorts based on limit_price and exchange_direction

    # BUY --> ascending and SELL --> ascending
    def sortNewOrder(self, exchangeSymbol, exchangeDirection, orderType):
        order = orderType == "buy"
        x = self.orders[exchangeSymbol][exchangeDirection]
        {k: v for k, v in sorted(x.items(), key=lambda item: item[1][-1], reverse = order)}

    def getOrders(self):
        return self.orders
    
    def updateOrder(self, order, amount):
        order[1][0] -= amount

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

        self.currentInvestment = {"amount": 0, "boughtCurrency": None, "soldCurrency": None, "init_order_number" : None} # an dictionary holding info about current Investment Object
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
        if not self.hasMadeOpenOrder and not self.hasMadeClosingOrder and not self.hasMadeClosingOrder and not self.closingTransactionWasSuccessfull:
            self.makeOrder("OPEN") # currentOrder is also updated
            self.hasMadeOpenOrder = True
        elif self.hasMadeOpenOrder and not self.openTransactionWasSuccessfull and not self.hasMadeClosingOrder and not self.closingTransactionWasSuccessfull:
            # wait for it for open order to be successful
            print ("")
            if self.currentOrder.expiration_time > 0:
                self.currentOrder.expiration_time -= 1
            else:
                self.hasMadeOpenOrder = False # remake an offer ... 
        elif self.hasMadeOpenOrder and self.openTransactionWasSuccessfull and not self.hasMadeClosingOrder and not self.closingTransactionWasSuccessfull:
            self.makeOrder("CLOSE") # currentOrder is also updated 
            self.hasMadeClosingOrder = True
        elif self.hasMadeOpenOrder and self.openTransactionWasSuccessfull and self.hasMadeClosingOrder and not self.closingTransactionWasSuccessfull:
            # wait for it for open order to be successful
            print ("wait for however long to close the position (for now // may change later")
        elif self.hasMadeOpenOrder and self.openTransactionWasSuccessfull and self.hasMadeClosingOrder and self.closingTransactionWasSuccessfull:
            # if agent has openned order, done open transac, closed order, and done closing transac
            self.initialiseParameters()
        

    def initialiseParameters(self):
        self.hasMadeOpenOrder = False
        self.hasMadeClosingOrder = False
        self.openTransactionWasSuccessfull = False
        self.closingTransactionWasSuccessfull = False
        self.currentOrder = None
        self.currentInvestment = {"amount": 0, "boughtCurrency": None, "soldCurrency":None, "init_order_number" : None}

    def makeOrder(self, orderType):
        # looks at what strategy returns // will be abstracted by currencyMarket and strategy object
        if orderType == "OPEN":
            self.currentOrder = self.strategy.makeOpenOrder(self, self.model.round)
        elif orderType == "CLOSE":
            self.currentOrder = self.strategy.makeCloseOrder(self, self.model.round)

        self.currencyMarket.getOrderBook().addOrder(self.currentOrder)

    def updateWallet(self, bought_currency, sold_currency, bought_currency_amount, sold_currency_amount):
        self.wallet[bought_currency] += bought_currency_amount
        self.wallet[sold_currency] -= sold_currency_amount
    
    def updateCurrentOrder(self, amount):
        self.currentOrder.amountOfBuyingCurrency -= amount

    def updateCurrentInvestment(self, amountInvested, order):
        self.currentInvestment["amount"] += amountInvested
        self.currentInvestment["boughtCurrency"] = order[1][2]
        self.currentInvestment["soldCurrency"] = order[1][3]
        self.currentInvestment["init_order_number"] = order[1][-1]


    def updateOrderStatus(self, type):
        if type == "OPEN":
            self.openTransactionWasSuccessfull = True
        else: 
            self.closingTransactionWasSuccessfull = True


