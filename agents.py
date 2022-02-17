from mesa import Agent
import random
from numpy import random
import numpy
import pandas as pd
from currency_pairs import currencyPairs, inverseCurrencyPair
# from investment_strategies import Strategy, Order

class CurrencyMarket:
    """
        Object that contains information necessary for AGENTS to make orders and transact with one another
    """
    def __init__(self, listOfCurrencies):
        self.currencies = listOfCurrencies
        self.exchange_rates = {"ETH/USDT" : 0, "USDT/ETH" : 0}
        self.orderBook = OrderBook()
        
    def getAvailableCurrencies(self):
        return self.currencies
    
    def updateMarketIndicators(self, currency):
        self.findMovingAverages(currency)
    
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

            buy_side_currency = value[2]
            selling_side_currency = value[3]

            currency_wanted = value[2] # you know that currency_wanted has to equal buy_side_currency
            currency_selling = value[3]

            order_type = value[4]
            limit_price = value[5]

            for otherOrder in sellOrders.items():
                otherAgentKey = otherOrder[0]
                otherValue = otherOrder[1]

                otherAmount = otherValue[0]
                otherId = otherValue[1]
                if otherId in orders_checked: continue

                # selling_side_currency = selling_side_currency
                # buy_side_currency = buy_side_currency

                other_order_type = otherValue[4]
                other_limit_price = otherValue[5]

                # if they agree on the exchange rate and they have not engaged in the transaction yet
                # other_limit_price == seller (more like minimum price it is willing to go to ) || limit_price == buyer (highest price it is willing to go too)
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
                        otherAgentKey.updateWallet(selling_side_currency, buy_side_currency, otherAmount, otherAmountOfOtherCurrencyRequiredToSell)
                        
                        agentKey.updateOrderStatus(order_type) # Makes open/closing transaction successful TRUE
                        otherAgentKey.updateOrderStatus(other_order_type)

                        agentKey.updateCurrentInvestment(amount, currency_wanted, currency_selling) # Makes currentInvestment take amount as values
                        otherAgentKey.updateCurrentInvestment(otherAmount, selling_side_currency, buy_side_currency)

                        # both will not be checked anymore
                        orders_checked.append(order_id)
                        orders_checked.append(otherId)
                        # will be removed from dictionary
                        primaryKeysToDelete.append(agentKey)
                        secondaryKeysToDelete.append(otherAgentKey)

                    # agentKey -- wants a bigger exchange; otherAgentKey satisfied but not AgentKey
                    elif (amount > otherAmountOfOtherCurrencyRequiredToSell and amountOfOtherCurrencyRequiredToSell > otherAmount): 
                        agentKey.updateWallet(currency_wanted, currency_selling, otherAmountOfOtherCurrencyRequiredToSell, otherAmount)
                        otherAgentKey.updateWallet(selling_side_currency, buy_side_currency, otherAmount, otherAmountOfOtherCurrencyRequiredToSell)
                        
                        self.orderBook.updateOrder(order, otherAmountOfOtherCurrencyRequiredToSell)
                        
                        agentKey.updateCurrentInvestment(otherAmountOfOtherCurrencyRequiredToSell, order)
                        otherAgentKey.updateCurrentInvestment(otherAmount, otherOrder)

                        agentKey.updateCurrentOrderAmount(otherAmountOfOtherCurrencyRequiredToSell)

                        orders_checked.append(otherId)
                        secondaryKeysToDelete.append(otherAgentKey) # deletes order by the key it is attached too

                        otherAgentKey.updateOrderStatus(other_order_type) # 

                    # otherAgentKey -- wants a bigger exchange; agentKey satisfied but not otherAgentKey
                    elif (amount < otherAmountOfOtherCurrencyRequiredToSell and amountOfOtherCurrencyRequiredToSell < otherAmount):
                        agentKey.updateWallet(currency_wanted, currency_selling, amount, amountOfOtherCurrencyRequiredToSell)
                        otherAgentKey.updateWallet(selling_side_currency, buy_side_currency, amountOfOtherCurrencyRequiredToSell, amount)

                        self.orderBook.updateOrder(otherOrder, amountOfOtherCurrencyRequiredToSell)
   
                        agentKey.updateCurrentInvestment(amount, order)
                        otherAgentKey.updateCurrentInvestment(amountOfOtherCurrencyRequiredToSell, otherOrder)
                        
                        otherAgentKey.updateCurrentOrderAmount(amountOfOtherCurrencyRequiredToSell)

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
        orderbook = self.getOrderBook().getOrders()
        for possible_currency_exchanges in orderbook:
            orders = orderbook[possible_currency_exchanges]
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

class OrderBook:
    """ 
        data structure which assembles order objects into a useful dictionary
        orderbook = { 
            "ETH/USDT" : <-- this is ultimately what I want
                {
                    "buy": { "agent1": [ 'amount', 'limit_price'], "agent2": [12, 1027] },
                    "sell" : { "agent3": [10, 1027], "agent4": [12, 1027] }
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
        orderType = order.order_type
        buyCurrency = order.buyCurrency
        sellCurrency = order.sellCurrency
        amount = order.amountOfBuyingCurrency
        agent = order.agent
        limit_price = order.limit_price
        order_id = order.order_id

        exchangeSymbol = currencyPairs[buyCurrency.getName()][sellCurrency.getName()]["exchange_symbol"] # what is the exchange symbol e.g. "ETH/USDT"
        exchangeDirection = currencyPairs[buyCurrency.getName()][sellCurrency.getName()]["direction"] # is it a buy or sell with respect to first currency

        # append it as a key-value pair
        self.orders[exchangeSymbol][exchangeDirection][agent] = [amount, order_id, buyCurrency, sellCurrency, orderType, limit_price] # later will add price
        
        self.sortNewOrder(exchangeSymbol, exchangeDirection, orderType) # sorts based on limit_price and exchange_direction

    # BUY --> ascending and SELL --> ascending
    def sortNewOrder(self, exchangeSymbol, exchangeDirection, orderType):
        ordering = orderType == "buy"
        orders_of_type = self.orders[exchangeSymbol][exchangeDirection]
        {k: v for k, v in sorted(orders_of_type.items(), key=lambda item: item[1][-1], reverse = ordering)}

    def getOrders(self):
        return self.orders
    
    def updateOrder(self, order, amount):
        print ("WHat Is OrDEr: ", order)
        order[1][0] -= amount
    
    def updateAgentOrderLimitPrice(self, agent, new_limit_price):
        buyCurrency = agent.currentOrder.buyCurrency.getName()
        sellCurrency = agent.currentOrder.sellCurrency.getName()
        exchangeSymbol = currencyPairs[buyCurrency][sellCurrency]["exchange_symbol"]
        exchangeDirection = currencyPairs[buyCurrency][sellCurrency]["direction"]
        self.orders[exchangeSymbol][exchangeDirection][agent][-1] = new_limit_price

    def printOrderBook(self):
        """ visual representation of order book """
        print(self.orders.items())

class MarketAgent(Agent):

    def __init__(self, unique_id, model, strategy, currencyMarket):
        self.unique_id = unique_id
        self.model = model
        self.round = model.round
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

        self.round = self.model.round
        
        if not self.hasMadeOpenOrder and not self.hasMadeClosingOrder and not self.hasMadeClosingOrder and not self.closingTransactionWasSuccessfull:
            self.makeOrder("OPEN") # currentOrder is also updated
            self.hasMadeOpenOrder = True
        elif self.hasMadeOpenOrder and not self.openTransactionWasSuccessfull and not self.hasMadeClosingOrder and not self.closingTransactionWasSuccessfull:
            # wait for open order to be successful (Open order not fulfilled yet ... )
            print ("open order not fullfilled yet: ", self)
            if self.currentOrder.expiration_time > 0:
                self.currentOrder.expiration_time -= 1
            else: 
                # UPDATE the limit_price of the order (could be too low or too high)
                self.updateCurrentOrderLimitPrice() # updates for agent
                # updateOrderBook
                self.currencyMarket.orderBook.updateAgentOrderLimitPrice(self, self.currentOrder.limit_price)
                self.currentOrder
        elif self.hasMadeOpenOrder and self.openTransactionWasSuccessfull and not self.hasMadeClosingOrder and not self.closingTransactionWasSuccessfull:
            if self.strategy.closingConditionMet(self, self.round): # obsolete atm (always TRUE)
                self.makeOrder("CLOSE") # currentOrder is also updated 
                self.hasMadeClosingOrder = True
        elif self.hasMadeOpenOrder and self.openTransactionWasSuccessfull and self.hasMadeClosingOrder and not self.closingTransactionWasSuccessfull:
            # wait for it for open order to be successful
            print ("wait for however long to close the position (for now // may change later")
        elif self.hasMadeOpenOrder and self.openTransactionWasSuccessfull and self.hasMadeClosingOrder and self.closingTransactionWasSuccessfull:
            # if agent has openned order, done open transac, closed order, and done closing transac
            self.initialiseParameters()
        
    def hasACurrentInvestment(self):
        if self.currentInvestment == {"amount": 0, "boughtCurrency": None, "soldCurrency": None, "init_order_number" : None}:
            return False
        else: True

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
            self.currentOrder = self.strategy.makeOpenOrder(self, self.round)
        elif orderType == "CLOSE":
            self.currentOrder = self.strategy.makeCloseOrder(self, self.round)

        print (self.currentOrder)
        self.currencyMarket.getOrderBook().addOrder(self.currentOrder)

    def updateWallet(self, bought_currency, sold_currency, bought_currency_amount, sold_currency_amount):
        self.wallet[bought_currency] += bought_currency_amount
        self.wallet[sold_currency] -= sold_currency_amount
    
    def updateCurrentOrderAmount(self, amount):
        self.currentOrder.amountOfBuyingCurrency -= amount

    def updateCurrentOrderLimitPrice(self):
        buyCurrency = self.currentOrder.buyCurrency.getName()
        sellCurrency = self.currentOrder.sellCurrency.getName()
        direction = currencyPairs[buyCurrency][sellCurrency]["direction"]

        if direction == "buy":
            self.currentOrder.limit_price *= 1.02 # increase the limit_price by 2% (limit_price was too low)
        else: self.currentOrder.limit_price *= 0.98 # decrease by 2% (limit_price was too high)

    def updateCurrentInvestment(self, amountInvested, order):
        self.currentInvestment["amount"] += amountInvested
        self.currentInvestment["boughtCurrency"] = order[1][2]
        self.currentInvestment["soldCurrency"] = order[1][3]
        self.currentInvestment["init_order_number"] = order[1][1]

    def updateOrderStatus(self, type):
        if type == "OPEN":
            self.openTransactionWasSuccessfull = True
        else: 
            self.closingTransactionWasSuccessfull = True


