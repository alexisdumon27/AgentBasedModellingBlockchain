from numpy import random
import pandas as pd
from currency_pairs import currencyPairs, inverseCurrencyPair


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

            order_type = value[4]
            limit_price = value[5]

            for otherOrder in sellOrders.items():
                otherAgentKey = otherOrder[0]
                otherValue = otherOrder[1]

                otherAmount = otherValue[0]
                otherId = otherValue[1]
                if otherId in orders_checked: continue

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
                        agentKey.updateWallet(buy_side_currency, selling_side_currency, amount, amountOfOtherCurrencyRequiredToSell)
                        otherAgentKey.updateWallet(selling_side_currency, buy_side_currency, otherAmount, otherAmountOfOtherCurrencyRequiredToSell)
                        
                        agentKey.updateOrderStatus(order_type) # Makes open/closing transaction successful TRUE
                        otherAgentKey.updateOrderStatus(other_order_type)

                        agentKey.updateCurrentInvestment(amount, buy_side_currency, selling_side_currency) # Makes currentInvestment take amount as values
                        otherAgentKey.updateCurrentInvestment(otherAmount, selling_side_currency, buy_side_currency)

                        # both will not be checked anymore
                        orders_checked.append(order_id)
                        orders_checked.append(otherId)
                        # will be removed from dictionary
                        primaryKeysToDelete.append(agentKey)
                        secondaryKeysToDelete.append(otherAgentKey)
                        break # do not look at other possible selling agents

                    # agentKey -- wants a bigger exchange; otherAgentKey satisfied but not AgentKey
                    elif (amount > otherAmountOfOtherCurrencyRequiredToSell and amountOfOtherCurrencyRequiredToSell > otherAmount): 
                        agentKey.updateWallet(buy_side_currency, selling_side_currency, otherAmountOfOtherCurrencyRequiredToSell, otherAmount)
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
                        agentKey.updateWallet(buy_side_currency, selling_side_currency, amount, amountOfOtherCurrencyRequiredToSell)
                        otherAgentKey.updateWallet(selling_side_currency, buy_side_currency, amountOfOtherCurrencyRequiredToSell, amount)

                        self.orderBook.updateOrder(otherOrder, amountOfOtherCurrencyRequiredToSell)
   
                        agentKey.updateCurrentInvestment(amount, order)
                        otherAgentKey.updateCurrentInvestment(amountOfOtherCurrencyRequiredToSell, otherOrder)
                        
                        otherAgentKey.updateCurrentOrderAmount(amountOfOtherCurrencyRequiredToSell)

                        orders_checked.append(order_id)
                        primaryKeysToDelete.append(agentKey) # deletes order by the key it is attached too

                        agentKey.updateOrderStatus(order_type)
                        break # exit the loop to match buying agent with a selling agent -- buying agent is satisfied!
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
        print ("Amount before updating: ", order[1][0])
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
