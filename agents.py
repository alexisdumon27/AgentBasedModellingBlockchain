from mesa import Agent
import random
from numpy import random
import numpy
import pandas as pd
from currency_pairs import currencyPairs, inverseCurrencyPair

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


