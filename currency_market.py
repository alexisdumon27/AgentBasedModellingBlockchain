from numpy import random
import pandas as pd
from currency_pairs import currencyPairs, inverseCurrencyPair

class CurrencyMarket:
    """
        Object that contains information necessary for AGENTS to make orders and transact with one another
    """
    def __init__(self, listOfCurrencies, exchange_rates):
        self.currencies = listOfCurrencies
        self.exchange_rates = exchange_rates
        self.orderBook = OrderBook()
        
    def getAvailableCurrencies(self):
        return self.currencies
    
    def getOrderBook(self):
        return self.orderBook

    def getCurrenciesExchangeRate(self, symbol, round):
        return self.exchange_rates[symbol][round]

    def matchBuyAndSellOrders(self, buyOrders, sellOrders):
        buying_orders_keys_to_delete = [] # lists of the keys of the orders to delete
        selling_orders_keys_to_delete = []

        number_of_transactions = 0
        # see if there is a match in the order Book
        # a match is two Orders with same currency pair where the amount that can exchaged is the same
        for order in buyOrders.items():
            agent_key = order[0]
            buy_order_values = order[1]

            amount = buy_order_values[0]
            order_type = buy_order_values[3]
            limit_price = buy_order_values[4]

            for other_order in sellOrders.items():
                other_agent_key = other_order[0]
                sell_order_values = other_order[1]

                other_amount = sell_order_values[0]
                other_order_type = sell_order_values[3]
                other_limit_price = sell_order_values[4]

                # if they agree on the exchange rate and they have not engaged in the transaction yet
                # other_limit_price == seller (more like minimum price it is willing to go to ) || limit_price == buyer (highest price it is willing to go too)
                if ( other_limit_price <= limit_price and agent_key not in buying_orders_keys_to_delete and other_agent_key not in selling_orders_keys_to_delete):
                    """
                        A sell order of index j matches a buy order of index i, and
                        vice versa, only if other_limit_price ≤ limit_price, or if one of the two limit prices, or both, are equal to zero
                    """
                    number_of_transactions += 1

                    # calculate the exchange
                    avg_price = (other_limit_price + limit_price) / 2
                    buy_order_amount_selling_other_currency = amount * avg_price 
                    sell_order_amount_selling_other_currency = other_amount / avg_price

                    print ("amount needed to sell in order to buy: ", buy_order_amount_selling_other_currency)
                    print ("amount needed to sell in order to buy for selling side", sell_order_amount_selling_other_currency)
                    # print ("A transaction is happening")
                    # print ("BUYING AGENT before")
                    # print ("wallet: ", agent_key.wallet)
                    # print ("current investment: ", agent_key.currentInvestment)
                    
                    # print ("ORDER before")
                    # print (amount)
                    # print ("Other Order before")
                    # print (other_amount)

                    # agent_key -- wants a bigger exchange; other_agent_key satisfied but not AgentKey
                    if self.isBuyOrderBiggerThanSellOrder(buy_order_values, sell_order_values, buy_order_amount_selling_other_currency, sell_order_amount_selling_other_currency): 
                        agent_key.updateCurrentState(order, sell_order_amount_selling_other_currency, other_amount, current_order_amount = 1)
                        other_agent_key.updateCurrentState(other_order, other_amount, sell_order_amount_selling_other_currency, order_status = other_order_type)

                        # update agent_key's order in the orderBook -- removes amount sold by other_agent_key
                        self.orderBook.updateOrder(order, sell_order_amount_selling_other_currency) # will be left with smaller amount remaining
                        
                        # adds other_order in the list of checked orders and to the list of keys to delete 
                        selling_orders_keys_to_delete.append(other_agent_key)

                    # other_agent_key -- wants a bigger or equal exchange; agent_key satisfied but not (neccessarily) other_agent_key
                    else:
                        agent_key.updateCurrentState(order, amount, buy_order_amount_selling_other_currency, order_status = order_type)
                        other_agent_key.updateCurrentState(other_order, buy_order_amount_selling_other_currency, amount, current_order_amount = 1)

                        # update agent_key's order in the orderBook -- removes amount sold by other_agent_key
                        self.orderBook.updateOrder(other_order, buy_order_amount_selling_other_currency) # will be left with smallet amount remaining

                        # agent_key's order has been fulfilled completely // it is added to the list of keys to delete
                        buying_orders_keys_to_delete.append(agent_key)
                        
                        if amount == sell_order_amount_selling_other_currency:
                            selling_orders_keys_to_delete.append(other_agent_key)
                            other_agent_key.updateOrderStatus(other_order_type)
                        break # exit the loop to match buying agent with a selling agent -- buying agent is satisfied!

                    # print ("BUYING AGENT after")
                    # print ("wallet: ", agent_key.wallet)
                    # print ("current investment: ", agent_key.currentInvestment)
                    # print ("ORDER after")
                    # print (amount)
                    # print ("Other Order after")
                    # print (other_amount)
        
        print ("In this round there were: ", number_of_transactions, " transactions")
        # delete keys from orderbook
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

    def isBuyOrderBiggerThanSellOrder(self, buy_order_values, sell_order_values, buy_order_amount_selling, sell_order_amount_amount_selling):
        amount = buy_order_values[0]
        other_amount = sell_order_values[0]
        if (amount > sell_order_amount_amount_selling and buy_order_amount_selling > other_amount):
            return True
        else:
            return False

class Currency:

    def __init__(self, name, conversionSymbol, type, amountInCirculation, data):
        self.name = name
        self.symbol = conversionSymbol
        self.type = type
        self.amountInCirculation = amountInCirculation
        self.data = data
        self.transactions = 0

    # necessary to find the price in USD
    # maybe better if I do not pass the data as a parameter ... 
    def getPriceAtRound(self, round):
        conversionSymbol = "USD/" + self.symbol
        return self.data[conversionSymbol].values[round]

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

class Exchange_Rates:
    def __init__(self, exchange_rates_data):
        
        self.data =  exchange_rates_data

    def getPriceAtRound(self, round, symbol):
        return self.data[symbol].values[round]
    
    def getType(self):
        return self.type


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

        exchangeSymbol = currencyPairs[buyCurrency.getName()][sellCurrency.getName()]["exchange_symbol"] # what is the exchange symbol e.g. "ETH/USDT"
        exchangeDirection = currencyPairs[buyCurrency.getName()][sellCurrency.getName()]["direction"] # is it a buy or sell with respect to first currency

        # append it as a key-value pair
        self.orders[exchangeSymbol][exchangeDirection][agent] = [amount, buyCurrency, sellCurrency, orderType, limit_price] # later will add price
        
        self.sortNewOrder(exchangeSymbol, exchangeDirection, orderType) # sorts based on limit_price and exchange_direction


    # BUY --> ascending and SELL --> ascending
    def sortNewOrder(self, exchangeSymbol, exchangeDirection, orderType):
        ordering = orderType == "buy"
        orders_of_type = self.orders[exchangeSymbol][exchangeDirection]
        {k: v for k, v in sorted(orders_of_type.items(), key=lambda item: item[1][-1], reverse = ordering)}

    def getOrders(self):
        return self.orders
    
    def updateOrder(self, order, amount):
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
