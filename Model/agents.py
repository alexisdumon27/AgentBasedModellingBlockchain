from cmath import inf
import random
from mesa import Agent


class MarketAgent(Agent):
    """
        This class defines agents for the simulation. It aims to make the agents emulate real-life investors agents.
        It extends MESA's Agent class
    """
    def __init__(self, unique_id, model, strategy, risk_level, currency_market):
        self.unique_id = unique_id
        self.model = model
        self.round = model.round
        self.currency_market = currency_market
        self.risk_level = risk_level
        self.strategy = strategy

        # possible states of the agent
        self.has_made_open_order = False
        self.has_made_closing_order = False
        self.open_transaction_was_successfull = False
        self.closing_transaction_was_successfull = False

        self.current_investment = {"amount": 0, "bought_currency": None, "sold_currency": None} # a dictionary holding info about current Investment Object
        self.current_order = None

        self.wallet = {}
        if self.strategy.name == "random":
            self.createWalletRandom()
        else:
            self.createWallet()
            self.initialUSDValueOfWallet = self.getUSDWalletValue()
            self.currentUSDValueOfWallet = self.getUSDWalletValue()
            self.currentUSDValueOfGains = 0
            self.open_orders = []
            self.close_orders = []
    
    # creates the wallet for strategy following agents
    def createWallet(self):
        # choose 2 currencies and put $100 worth for each
        starting_amount_based_on_risk_level = {"averse": 100, "neutral": 270, "taker": 500}
        i = 0
        for currency in random.sample(self.currency_market.getAvailableCurrencies(), len(self.currency_market.getAvailableCurrencies())):
            if i == 0 or i == 1:
            # give 100 $ worth to 2 out of all currencies
                price_curr = currency.getPriceAtRound(self.round)
                self.wallet[currency] = starting_amount_based_on_risk_level[self.risk_level] / price_curr # start with 100 of both currencies
            else: self.wallet[currency] = 0
            i += 1

    # creates the wallet for random agents
    def createWalletRandom(self):
        for currency in self.currency_market.getAvailableCurrencies():
            self.wallet[currency] = float(inf)

    # extends step method from Agents parent class
    def step(self):
        self.round = self.model.round
        if self.strategy.name == "random":
            self.randomAgentStep()
        else:
            self.strategyAgentStep()
    
    # what a random agent should do in a step depending on its state
    def randomAgentStep(self):
        if self.current_order == None:
            if random.random() < 0.5:
                self.makeOrder("OPEN")
                self.has_made_open_order = True
        elif self.has_made_open_order and not self.open_transaction_was_successfull:
            if self.current_order.expiration_time > 0:
                self.current_order.expiration_time -= 1
            else:
                self.currency_market.order_book.removeAgentOrder(self)
                self.has_made_open_order = False
                self.current_order = None
        elif self.has_made_open_order and self.open_transaction_was_successfull:
            self.initialiseParameters()

    # what a strategy following agent should do in a step depending on its state
    def strategyAgentStep(self):
        if not self.has_made_open_order and not self.has_made_closing_order and not self.has_made_closing_order and not self.closing_transaction_was_successfull:
            # check if it should make an order
            # Following their strategy should it make an order?
            self.makeOrder("OPEN") # current_order is also updated
            if self.hasACurrentOrder():
                self.has_made_open_order = True
        elif self.has_made_open_order and not self.open_transaction_was_successfull and not self.has_made_closing_order and not self.closing_transaction_was_successfull:
            # wait for open order to be successful (Open order not fulfilled yet ... )
            if self.current_order.expiration_time > 0:
                self.current_order.expiration_time -= 1
            else: 
                if self.strategy.name == "random":
                    # re-initialise try another order
                    # remove previous order from order book
                    self.currency_market.order_book.removeAgentOrder(self)
                    self.has_made_open_order = False
                    self.current_order = None
                else:
                    # UPDATE the limit_price of the order
                    self.updateCurrentOrderLimitPrice() # updates for agent
                    self.currency_market.order_book.updateAgentOrderLimitPriceInOrderBook(self, self.current_order.limit_price) # updates the orderbook with the agent's new limit price
        elif self.has_made_open_order and self.open_transaction_was_successfull and not self.has_made_closing_order and not self.closing_transaction_was_successfull:
            if self.strategy.closingConditionMet(self, self.round):
                self.makeOrder("CLOSE") # current_order is also updated 
                self.has_made_closing_order = True
        elif self.has_made_open_order and self.open_transaction_was_successfull and self.has_made_closing_order and not self.closing_transaction_was_successfull:
            # wait for it for open order to be successful
            if self.current_order.expiration_time > 0:
                self.current_order.expiration_time -= 1
            else: 
                # UPDATE the limit_price of the order
                self.updateCurrentOrderLimitPrice() # updates for agent
                self.currency_market.order_book.updateAgentOrderLimitPriceInOrderBook(self, self.current_order.limit_price) # updates the orderbook with agents new limit price
        elif self.has_made_open_order and self.open_transaction_was_successfull and self.has_made_closing_order and self.closing_transaction_was_successfull:
            # if agent has openned order, done open transac, closed order, and done closing transac
            self.initialiseParameters()
        
        self.currentUSDValueOfWallet = self.getUSDWalletValue() # gets updated every round
        self.currentUSDValueOfGains = self.currentUSDValueOfWallet - self.initialUSDValueOfWallet

    # checks if it has a current investment
    def hasACurrentInvestment(self):
        if self.current_investment == {"amount": 0, "bought_currency": None, "sold_currency": None}:
            return False
        else: True

    # checks if it has a current order
    def hasACurrentOrder(self):
        return self.current_order != None

    # initialises the parameters for when strategy following agents go back to initial state
    def initialiseParameters(self):
        self.has_made_open_order = False
        self.has_made_closing_order = False
        self.open_transaction_was_successfull = False
        self.closing_transaction_was_successfull = False
        self.current_order = None
        self.current_investment = {"amount": 0, "bought_currency": None, "sold_currency":None}

    # makes an order
    def makeOrder(self, order_type):
        possible_order = None
        if order_type == "OPEN":
            possible_order = self.strategy.tryToMakeOpenOrder(self, self.round)
        elif order_type == "CLOSE":
            possible_order = self.strategy.makeCloseOrder(self, self.round)
        
        # was it a good time to make an order?
        if possible_order != None:

            self.current_order = possible_order
            self.currency_market.getOrderBook().addOrder(self.current_order)
            if self.strategy.name != "random":
                buy_currency = self.current_order.buy_currency
                sell_currency = self.current_order.sell_currency
                symbol = buy_currency.symbol + "/" + sell_currency.symbol

                self.currency_market.num_of_orders_by_currency_pairs[symbol][-1] += 1
                self.currency_market.num_of_orders_dict_by_strategy_by_currency[self.strategy.name][symbol][-1] += 1

                if order_type == "OPEN":
                    self.open_orders.append([self.round, buy_currency.symbol, sell_currency.symbol, self.current_order.amount_of_buying_currency])
                else:  
                    self.close_orders.append([self.round, buy_currency.symbol, sell_currency.symbol, self.current_order.amount_of_buying_currency])

    # returns the currencies in agent's wallet with a positive balance
    def getCurrenciesInWalletWithPositiveBalance(self):
        currency_balance_above_zero = []
        for currency_key in self.wallet.keys():
            if self.wallet[currency_key] > 0:
                currency_balance_above_zero.append(currency_key)
        return random.sample(currency_balance_above_zero, len(currency_balance_above_zero))

    # update the wallets content after doing a transaction
    def updateWallet(self, bought_currency, sold_currency, bought_currency_amount, sold_currency_amount):
        self.wallet[bought_currency] += bought_currency_amount
        self.wallet[sold_currency] -= sold_currency_amount
    
    # update the amount left for the current order after doing a transaction
    def updateCurrentOrderAmount(self, amount):
        self.current_order.amount_of_buying_currency -= amount

    # changes the limit_price of an order if the experiration time has run out
    def updateCurrentOrderLimitPrice(self):
        buy_currency = self.current_order.buy_currency
        sell_currency = self.current_order.sell_currency
        symbol = buy_currency.symbol + "/" + sell_currency.symbol
        current_exchange_rate = self.currency_market.getCurrenciesExchangeRate(symbol, self.model.round)
        self.current_order.limit_price = self.strategy.getLimitPrice(current_exchange_rate) # update the limit_price !!!!

    # updates the content of the current investment
    def updateCurrentInvestment(self, amount_sold, order):
        self.current_investment["amount"] += amount_sold # amount of currency it sold to buy desired currency
        self.current_investment["bought_currency"] = order[1][1]
        self.current_investment["sold_currency"] = order[1][2]

    # updates the state of the agent based on the type of order it has put forward
    def updateOrderStatus(self, type):
        if type == "OPEN":
            self.open_transaction_was_successfull = True
        else: 
            self.closing_transaction_was_successfull = True

    # returns USD value of wallet
    def getUSDWalletValue(self):
        total = 0
        for currency in self.wallet:
            amount_of_curr = self.wallet[currency]
            price_curr = currency.getPriceAtRound(self.round)
            total += amount_of_curr * price_curr
        return total

    # updates the current state of the agent
    def updateCurrentState(self, order, bought_currency_amount, sold_currency_amount, order_status = None, current_order_amount = None):
        bought_currency = order[1][1]
        sold_currency = order[1][2]

        self.updateWallet(bought_currency, sold_currency, bought_currency_amount, sold_currency_amount)
        self.updateCurrentInvestment(sold_currency_amount, order) # adds amount it had to sell to buy == amount bought by other_agent

        if order_status != None: self.updateOrderStatus(order_status)
        if current_order_amount != None: self.updateCurrentOrderAmount(bought_currency_amount)