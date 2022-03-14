from locale import currency
import random
from mesa import Agent

class MarketAgent(Agent):

    def __init__(self, unique_id, model, strategy, currency_market):
        self.unique_id = unique_id
        self.model = model
        self.round = model.round
        self.currency_market = currency_market

        # randomly initialised fields
        self.strategy = strategy

        self.has_made_open_order = False
        self.has_made_closing_order = False
        self.open_transaction_was_successfull = False
        self.closing_transaction_was_successfull = False

        self.current_investment = {"amount": 0, "bought_currency": None, "sold_currency": None} # an dictionary holding info about current Investment Object
        self.current_order = None

        self.wallet = {}
        self.createWallet()

        self.initialUSDValueOfWallet = self.getUSDWalletValue()
        self.currentUSDValueOfWallet = self.getUSDWalletValue()
    
    # start with $100 worth of all possible currencies
    def createWallet(self):
        for currency in self.currency_market.getAvailableCurrencies():
            # give 100 $ worth of every currency
            self.wallet[currency] = 100 # start with 100 of both currencies

    # what happens during one round of the simulation for one agent
    ## a limited amount of agents get to perform their step actions per turn 
    def step(self):
        """ if it was chosen as a trading agent this turn; then it adds an order to the order book list """

        self.round = self.model.round
        
        if not self.has_made_open_order and not self.has_made_closing_order and not self.has_made_closing_order and not self.closing_transaction_was_successfull:
            self.makeOrder("OPEN") # current_order is also updated
            if self.hasACurrentOrder():
                self.has_made_open_order = True
        elif self.has_made_open_order and not self.open_transaction_was_successfull and not self.has_made_closing_order and not self.closing_transaction_was_successfull:
            # wait for open order to be successful (Open order not fulfilled yet ... )
            if self.current_order.expiration_time > 0:
                self.current_order.expiration_time -= 1
            else: 
                # UPDATE the limit_price of the order (could be too low or too high)
                self.updateCurrentOrderLimitPrice() # updates for agent
                self.currency_market.order_book.updateAgentOrderLimitPriceInOrderBook(self, self.current_order.limit_price) # updates the orderbook withe agents new limit price
        elif self.has_made_open_order and self.open_transaction_was_successfull and not self.has_made_closing_order and not self.closing_transaction_was_successfull:
            if self.strategy.closingConditionMet(self, self.round):
                self.makeOrder("CLOSE") # current_order is also updated 
                self.has_made_closing_order = True
        elif self.has_made_open_order and self.open_transaction_was_successfull and self.has_made_closing_order and not self.closing_transaction_was_successfull:
            # wait for it for open order to be successful
            if self.current_order.expiration_time > 0:
                self.current_order.expiration_time -= 1
            else: 
                # UPDATE the limit_price of the order (could be too low or too high)
                self.updateCurrentOrderLimitPrice() # updates for agent
                self.currency_market.order_book.updateAgentOrderLimitPriceInOrderBook(self, self.current_order.limit_price) # updates the orderbook with agents new limit price
        elif self.has_made_open_order and self.open_transaction_was_successfull and self.has_made_closing_order and self.closing_transaction_was_successfull:
            # if agent has openned order, done open transac, closed order, and done closing transac
            self.initialiseParameters()
        
        self.currentUSDValueOfWallet = self.getUSDWalletValue()
        
    def hasACurrentInvestment(self):
        if self.current_investment == {"amount": 0, "bought_currency": None, "sold_currency": None}:
            return False
        else: True

    def hasACurrentOrder(self):
        return self.current_order != None

    def initialiseParameters(self):
        self.has_made_open_order = False
        self.has_made_closing_order = False
        self.open_transaction_was_successfull = False
        self.closing_transaction_was_successfull = False
        self.current_order = None
        self.current_investment = {"amount": 0, "bought_currency": None, "sold_currency":None}

    def makeOrder(self, orderType):
        # looks at what strategy returns // will be abstracted by currency_market and strategy object
        if orderType == "OPEN":
            possibleOrder = self.strategy.makeOpenOrder(self, self.round)
        elif orderType == "CLOSE":
            possibleOrder = self.strategy.makeCloseOrder(self, self.round)

        if possibleOrder != None:
            self.current_order = possibleOrder
            self.currency_market.getOrderBook().addOrder(self.current_order)

    def getCurrenciesInWalletWithPositiveBalance(self):
        currency_balance_above_zero = []
        for currency_key in self.wallet.keys():
            if self.wallet[currency_key] > 0:
                currency_balance_above_zero.append(currency_key)
        return random.sample(currency_balance_above_zero, len(currency_balance_above_zero))

    def updateWallet(self, bought_currency, sold_currency, bought_currency_amount, sold_currency_amount):
        self.wallet[bought_currency] += bought_currency_amount
        self.wallet[sold_currency] -= sold_currency_amount
    
    def updateCurrentOrderAmount(self, amount):
        self.current_order.amount_of_buying_currency -= amount

    def updateCurrentOrderLimitPrice(self):
        """
            change to use the new limit price || remove order
        """
        buy_currency = self.current_order.buy_currency
        sell_currency = self.current_order.sell_currency
        symbol = buy_currency.symbol + "/" + sell_currency.symbol
        current_exchange_rate = self.currency_market.getCurrenciesExchangeRate(symbol, self.model.round)
        self.current_order.limit_price = self.strategy.getLimitPrice(current_exchange_rate) # update the limit_price !!!!

    def updateCurrentInvestment(self, amount_sold, order):
        self.current_investment["amount"] += amount_sold # amount of currency it sold to buy desired currency
        self.current_investment["bought_currency"] = order[1][1]
        self.current_investment["sold_currency"] = order[1][2]

    def updateOrderStatus(self, type):
        if type == "OPEN":
            self.open_transaction_was_successfull = True
        else: 
            self.closing_transaction_was_successfull = True

    def getUSDWalletValue(self):
        total = 0
        for currency in self.wallet:
            amount_of_curr = self.wallet[currency]
            price_curr = currency.getPriceAtRound(self.round)
            total += amount_of_curr * price_curr
        return total

    def updateCurrentState(self, order, bought_currency_amount, sold_currency_amount, order_status = None, current_order_amount = None):
        bought_currency = order[1][1]
        sold_currency = order[1][2]

        self.updateWallet(bought_currency, sold_currency, bought_currency_amount, sold_currency_amount)
        self.updateCurrentInvestment(sold_currency_amount, order) # adds amount it had to sell to buy == amount bought by other_agent

        if order_status != None: self.updateOrderStatus(order_status)
        if current_order_amount != None: self.updateCurrentOrderAmount(bought_currency_amount)