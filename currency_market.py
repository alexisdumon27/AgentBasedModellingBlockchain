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
        buying_orders_keys_to_delete = [] # lists of the keys of the orders to delete
        selling_orders_keys_to_delete = []
        completed_orders = [] # list of order_id of orders already checked for a match

        # see if there is a match in the order Book
        # a match is two Orders with same currency pair where the amount that can exchaged is the same
        for order in buyOrders.items():
            agent_key = order[0]
            value = order[1]

            amount = value[0]
            order_id = value[1]
            buy_side_currency = value[2]
            selling_side_currency = value[3]
            order_type = value[4]
            limit_price = value[5]

            for other_order in sellOrders.items():
                other_agent_key = other_order[0]
                other_value = other_order[1]

                other_amount = other_value[0]
                other_order_id = other_value[1]
                other_order_type = other_value[4]
                other_limit_price = other_value[5]

                # if they agree on the exchange rate and they have not engaged in the transaction yet
                # other_limit_price == seller (more like minimum price it is willing to go to ) || limit_price == buyer (highest price it is willing to go too)
                if ( other_limit_price <= limit_price and order_id not in completed_orders and other_order_id not in completed_orders and other_amount > 0):
                    """
                        A sell order of index j matches a buy order of index i, and
                        vice versa, only if other_limit_price ≤ limit_price, or if one of the two limit prices, or both, are equal to zero
                    """
                    # calculate the exchange
                    avg_price = (other_limit_price + limit_price) / 2
                    amountOfOtherCurrencyRequiredToSell = amount * avg_price 
                    otherAmountOfOtherCurrencyRequiredToSell = other_amount / avg_price

                    # agent_key -- wants a bigger exchange; other_agent_key satisfied but not AgentKey
                    if (amount > otherAmountOfOtherCurrencyRequiredToSell and amountOfOtherCurrencyRequiredToSell > other_amount): 
                        # both update their wallets <-- actual transaction (REFACTOR)
                        agent_key.updateWallet(buy_side_currency, selling_side_currency, otherAmountOfOtherCurrencyRequiredToSell, other_amount)
                        other_agent_key.updateWallet(selling_side_currency, buy_side_currency, other_amount, otherAmountOfOtherCurrencyRequiredToSell)
                        
                        # both update their current investments
                        agent_key.updateCurrentInvestment(other_amount, order) # adds amount it had to sell to buy == amount bought by other_agent
                        other_agent_key.updateCurrentInvestment(otherAmountOfOtherCurrencyRequiredToSell, other_order) # adds amount it had to sell to buy

                        # update agent_key's order in the orderBook -- removes amount sold by other_agent_key
                        self.orderBook.updateOrder(order, otherAmountOfOtherCurrencyRequiredToSell) # will be left with smaller amount remaining
                        
                        # update agent_keys's current order amount -- removes amount sold by other_agent_key
                        agent_key.updateCurrentOrderAmount(otherAmountOfOtherCurrencyRequiredToSell)     

                        # updates other_agent_key's order status -- it has successfully (completely) openned/closed an order
                        other_agent_key.updateOrderStatus(other_order_type)

                        # adds other_order in the list of checked orders and to the list of keys to delete 
                        completed_orders.append(other_order_id)
                        selling_orders_keys_to_delete.append(other_agent_key)

                    # other_agent_key -- wants a bigger or equal exchange; agent_key satisfied but not (neccessarily) other_agent_key
                    elif (amount <= amountOfOtherCurrencyRequiredToSell and amountOfOtherCurrencyRequiredToSell <= other_amount):
                        # both update their wallets <-- actual transaction (REFACTOR)
                        agent_key.updateWallet(buy_side_currency, selling_side_currency, amount, amountOfOtherCurrencyRequiredToSell)
                        other_agent_key.updateWallet(selling_side_currency, buy_side_currency, amountOfOtherCurrencyRequiredToSell, amount)

                        # both update their current investments
                        agent_key.updateCurrentInvestment(amountOfOtherCurrencyRequiredToSell, order) # agent_key's amount it had to sell
                        other_agent_key.updateCurrentInvestment(amount, other_order) # other_agent_key adds amount that agent_key has sold to it
                        
                        # update agent_key's order in the orderBook -- removes amount sold by other_agent_key
                        self.orderBook.updateOrder(other_order, amountOfOtherCurrencyRequiredToSell) # will be left with smallet amount remaining

                        # update other_agent_key's current order amount -- removes amount sold by agent_key (there will be some remaining)
                        other_agent_key.updateCurrentOrderAmount(amountOfOtherCurrencyRequiredToSell)

                        # updates agent_key's order status -- it has successfully (completely) openned/closed an order
                        agent_key.updateOrderStatus(order_type)

                        # agent_key's order has been fulfilled completely // it is added to the list of keys to delete
                        completed_orders.append(order_id)
                        buying_orders_keys_to_delete.append(agent_key)
                        
                        if amount == otherAmountOfOtherCurrencyRequiredToSell:
                            completed_orders.append(other_order_id)
                            selling_orders_keys_to_delete.append(other_agent_key)
                            other_agent_key.updateOrderStatus(other_order_type)
                        break # exit the loop to match buying agent with a selling agent -- buying agent is satisfied!
                    else:
                        return RuntimeError

        for i in buying_orders_keys_to_delete:
            del buyOrders[i]

        for i in selling_orders_keys_to_delete:
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
