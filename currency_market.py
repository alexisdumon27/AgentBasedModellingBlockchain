from unicodedata import name
from numpy import random
import pandas as pd

class CurrencyMarket:
    """
        Object that contains information necessary for AGENTS to make orders and transact with one another
    """
    def __init__(self, exchange_rates):

        ethereum = Currency("Ethereum", "ETH", "crypto", 100, exchange_rates['ETH/USD'])
        tether = Currency('Tether', "USDT", "fiat-backed", 100, exchange_rates['USDT/USD'])
        binance = Currency('Binance', "BNB", "crypto", 100, exchange_rates['BNB/USD'])
        bitcoin = Currency('Bitcoin', "BTC", "crypto", 100, exchange_rates['BTC/USD'])
        
        self.currencies = []
        self.currencies.append(ethereum)
        self.currencies.append(tether)
        self.currencies.append(binance)
        self.currencies.append(bitcoin)

        self.exchange_rates = exchange_rates
        self.order_book = OrderBook()
        self.num_of_transactions_dict = { # for data collection !!!
            "total" : [],
            "ETH/USDT:USDT/ETH" : [],
            "ETH/BNB:BNB/ETH" : [],
            "ETH/BTC:BTC/ETH" : [],
            "BNB/BTC:BTC/BNB" : [],
            "BNB/USDT:USDT/BNB" : [],
            "BTC/USDT:USDT/BTC" : []
        }

        
    def getAvailableCurrencies(self):
        return self.currencies
    
    def getOrderBook(self):
        return self.order_book

    def getCurrenciesExchangeRate(self, symbol, round):
        return self.exchange_rates[symbol][round]

    def matchBuyAndSellOrders(self, buy_orders, sell_orders, possible_currency_exchange):
        # which is buy_orders and sell_orders is arbitrary -- does not make a difference

        buying_orders_keys_to_delete = [] # lists of the keys of the orders to delete
        selling_orders_keys_to_delete = []

        # Match buying orders with selling orders based on limit_price and amount
        for order in buy_orders.items():
            agent_key = order[0]
            buy_order_values = order[1]

            amount = buy_order_values[0]
            order_type = buy_order_values[3]
            limit_price = buy_order_values[4]

            for other_order in sell_orders.items():
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
                    # calculate the exchange
                    avg_price = (other_limit_price + limit_price) / 2
                    buy_order_amount_selling_other_currency = amount * avg_price 
                    sell_order_amount_selling_other_currency = other_amount / avg_price

                    self.num_of_transactions_dict['total'][-1] += 1 # add one to the last entry in the cumulative total array
                    self.num_of_transactions_dict[possible_currency_exchange][-1] += 1 # add one to the respective total array

                    # agent_key -- wants a bigger exchange; other_agent_key satisfied but not AgentKey
                    if self.isBuyOrderBiggerThanSellOrder(buy_order_values, sell_order_values, buy_order_amount_selling_other_currency, sell_order_amount_selling_other_currency): 
                        agent_key.updateCurrentState(order, sell_order_amount_selling_other_currency, other_amount, current_order_amount = 1)
                        other_agent_key.updateCurrentState(other_order, other_amount, sell_order_amount_selling_other_currency, order_status = other_order_type)

                        # update agent_key's order in the order_book -- removes amount sold by other_agent_key
                        self.order_book.updateOrder(order, sell_order_amount_selling_other_currency) # will be left with smaller amount remaining
                        amount -= sell_order_amount_selling_other_currency
                        # adds other_order in the list of checked orders and to the list of keys to delete 
                        selling_orders_keys_to_delete.append(other_agent_key)

                    # other_agent_key -- wants a bigger or equal exchange; agent_key satisfied but not (neccessarily) other_agent_key
                    else:
                        agent_key.updateCurrentState(order, amount, buy_order_amount_selling_other_currency, order_status = order_type)
                        other_agent_key.updateCurrentState(other_order, buy_order_amount_selling_other_currency, amount, current_order_amount = 1)

                        # update agent_key's order in the order_book -- removes amount sold by other_agent_key
                        self.order_book.updateOrder(other_order, buy_order_amount_selling_other_currency) # will be left with smallet amount remaining

                        # agent_key's order has been fulfilled completely // it is added to the list of keys to delete
                        buying_orders_keys_to_delete.append(agent_key)
                        
                        if amount == sell_order_amount_selling_other_currency:
                            selling_orders_keys_to_delete.append(other_agent_key)
                            other_agent_key.updateOrderStatus(other_order_type)
                        break # exit the loop to match buying agent with a selling agent -- buying agent is satisfied!
                
        # delete keys from orderbook
        for i in buying_orders_keys_to_delete:
            del buy_orders[i]

        for i in selling_orders_keys_to_delete:
            del sell_orders[i]

    # https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0164603&type=printable <- for reordering orderbook
    def priceClearingMechanism(self):
        """ ............ """
        orderbook = self.getOrderBook().getOrders()
        self.num_of_transactions_this_round = 0
        self.addNewRoundToNumOfTransactionsDict()
        for possible_currency_exchange in orderbook:
            orders = orderbook[possible_currency_exchange] # returns dictionary  { 'ETH/USDT' : {agent 1 : [] ... }, 'USDT/ETH': { agent 2: [] ... }}
            exchange_symbol_keys = list(orders.keys())
            exchange_direction_0_orders = orders[exchange_symbol_keys[0]]
            exchange_direction_1_orders = orders[exchange_symbol_keys[1]]
            
            self.matchBuyAndSellOrders(exchange_direction_0_orders, exchange_direction_1_orders, possible_currency_exchange)

    def addNewRoundToNumOfTransactionsDict(self):
        for item in self.num_of_transactions_dict:
            array_of_transactions = self.num_of_transactions_dict[item]
            if len(array_of_transactions) == 0: array_of_transactions.append(0)
            else: array_of_transactions.append(array_of_transactions[-1])

    def isBuyOrderBiggerThanSellOrder(self, buy_order_values, sell_order_values, buy_order_amount_selling, sell_order_amount_amount_selling):
        amount = buy_order_values[0]
        other_amount = sell_order_values[0]
        if (amount > sell_order_amount_amount_selling and buy_order_amount_selling > other_amount):
            return True
        else:
            return False

class Currency:

    def __init__(self, name, conversion_symbol, type, amount_in_circulation, data):
        self.name = name
        self.symbol = conversion_symbol
        self.type = type
        self.amount_in_circulation = amount_in_circulation
        self.data = data # data = exchange_rates['symbol/USD']
        self.transactions = 0

    # necessary to find the price in USD
    # maybe better if I do not pass the data as a parameter ... 
    def getPriceAtRound(self, round):
        return self.data[round]
    
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
        {
            "ETH/USDT:USDT/ETH” : 
                {
                    'ETH/USDT': { buy orders …  },
                    'USDT/ETH' : { sell orders … }
                },
            "ETH/BNB:BNB/ETH" : 
                {
                    ‘ETH/BNB“ { buy orders …},
                    ‘BNB/ETH” : { sell orders
                }
                ...........
        }

    """

    def __init__(self) -> None:
        # self.orders = {"ETH/USDT" : {"buy":{}, "sell":{}}} # all possible currency pairs
        self.orders = {
            "ETH/USDT:USDT/ETH" : { 'ETH/USDT' : {}, 'USDT/ETH' : {} },
            "ETH/BNB:BNB/ETH" : { 'ETH/BNB' : {}, 'BNB/ETH' : {} },
            "ETH/BTC:BTC/ETH" : { 'ETH/BTC' : {}, 'BTC/ETH' : {} },
            "BNB/BTC:BTC/BNB" : { 'BNB/BTC' : {}, 'BTC/BNB' : {} },
            "BNB/USDT:USDT/BNB" :{ 'BNB/USDT' : {}, 'USDT/BNB' : {} },
            "BTC/USDT:USDT/BTC" : { 'BTC/USDT' : {}, 'USDT/BTC' : {} },
        }

    def addOrder(self, order):
        """
            adds an order object into self.orders {}
        """
        order_type = order.order_type
        buy_currency = order.buy_currency
        sell_currency = order.sell_currency
        amount = order.amount_of_buying_currency
        agent = order.agent
        limit_price = order.limit_price

        orderbook_key = self.getOrderBookKey(buy_currency, sell_currency)
        exchange_direction = self.getExchangeSymbol(buy_currency, sell_currency)

        self.orders[orderbook_key][exchange_direction][agent] = [amount, buy_currency, sell_currency, order_type, limit_price]

    def getOrderBookKey(self, buy_currency, sell_currency):
        buy_currency_symbol = buy_currency.symbol
        sell_currency_symbol = sell_currency.symbol
        exhange_symbol = buy_currency_symbol + "/" + sell_currency_symbol
        for key in self.orders.keys():
            symbols = key.split(":")
            if exhange_symbol in symbols:
                return key

    def getExchangeSymbol(self, buy_currency, sell_currency):
        return buy_currency.symbol + "/" + sell_currency.symbol

    def sortOrdersInOrderBook(self):
        # DOES NOT WORK YET
        # for exchange_symbols in self.orders.keys():
        #     currency_pair_orders = self.orders[exchange_symbols]
        #     currency_pair_orders["buy"] = {k: v for k, v in sorted(currency_pair_orders["buy"].items(), key=lambda item: item[1][-1], reverse = True)}
        #     currency_pair_orders["sell"] = {k: v for k, v in sorted(currency_pair_orders["sell"].items(), key=lambda item: item[1][-1], reverse = False)}
        return 27

    def getOrders(self):
        return self.orders
    
    def updateOrder(self, order, amount):
        # it receives an order array from the orderbook [amount, buy_currency, sell_currency, orderType, limit_price] ... 
        order[1][0] -= amount
    
    def updateAgentOrderLimitPriceInOrderBook(self, agent, new_limit_price):
        buy_currency = agent.current_order.buy_currency
        sell_currency = agent.current_order.sell_currency
        orderbook_key = self.getOrderBookKey(buy_currency, sell_currency)
        exchange_direction = self.getExchangeSymbol(buy_currency, sell_currency)
        self.orders[orderbook_key][exchange_direction][agent][-1] = new_limit_price

    def printOrderBook(self):
        """ visual representation of order book """
        print(self.orders.items())
