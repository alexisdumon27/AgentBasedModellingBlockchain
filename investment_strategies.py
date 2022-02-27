import random
import numpy
import pandas as pd
from currency_pairs import currencyPairs


class Order:
    """
        a data structure containing all the relevant information for the order request of an agent
    """
    def __init__(self, orderType, buyCurrency, sellCurrency, amountOfBuyingCurrency, round, agent, limit_price, expiration_time):
        self.order_type = orderType
        self.buyCurrency = buyCurrency # currency agent wants to buy
        self.sellCurrency = sellCurrency # currency agent will sell in order to buy
        self.amountOfBuyingCurrency = amountOfBuyingCurrency # amount of buy currency agent wants to own :: DEPEND ON EXCHANGE_RATE
        self.timestep = round # 
        self.agent = agent #
        self.expiration_time = expiration_time
        self.limit_price = limit_price

class Strategy:
    """
        this will eventually be a superclass whose children have different implementations of the four methods
        each children will therefore represent a different type of strategy
    """
    def __init__(self, strategy_name, exchange_rates_data):
        self.name = strategy_name
        self.exchange_rates = exchange_rates_data
        # agent_risk_level

        self.order_id = 0
        pass

    def getAmountOfBuyingCurrency(self, exchange_rate, direction, max_amount_to_sell):
        # should buy amount proportional to exchange_rate and it should not exceed the max amount of the currency it is selling
        amount = 0.00 # go through all the numbers until you reach the max amount that they can sell
        while amount < 1000000:
            amount += 0.01
            if direction == "buy" and exchange_rate > 1:
                if amount * exchange_rate > max_amount_to_sell:
                    amount -= 0.01
                    return amount
            else:
                if amount > max_amount_to_sell:
                    amount -= 0.01
                    return amount

    def getLimitPrice(self, direction, exchange_rate):
        random_gauss_factor = self.getRandomDrawFromGaussian(direction) # to add randomness in limit_prices
        limit_price = 0
        while limit_price <= 0:
            limit_price = exchange_rate * random_gauss_factor
        return limit_price # agent willing to buy at a slightly higher price

    # https://arxiv.org/pdf/cond-mat/0103600.pdf
    def getRandomDrawFromGaussian(self, direction):
        # For orders: μ = current_exchange_rate * 1.01, σmin = 0.01 and σmax = 0.003.
        mean = 0.98
        if direction == "buy":
            mean *= 1.02
        return numpy.random.normal(loc = mean, scale = random.uniform(0.003, 0.01))

    # always the same disregarding what the investement strategy is -- it closes the initial investment
    def makeCloseOrder(self, agent, round):
        """ wishes to exchange Y for X """

        investmentToClose = agent.currentInvestment # close current investment // investment is a dictionary object

        buyCurrency = investmentToClose["soldCurrency"] # currency you used to invest
        sellCurrency = investmentToClose["boughtCurrency"] # currency you invested in
        amountOfBuyingCurrency = investmentToClose["amount"] #
        
        symbol = currencyPairs[buyCurrency.getName()][sellCurrency.getName()]["exchange_symbol"]
        direction = currencyPairs[buyCurrency.getName()][sellCurrency.getName()]["direction"]
        exchange_rate = agent.currencyMarket.getCurrenciesExchangeRate(symbol, agent.round)
        limit_price = self.getLimitPrice(direction, exchange_rate)

        expiration_time = random.choice(range(2,5))
        return Order("CLOSE", buyCurrency, sellCurrency, amountOfBuyingCurrency, round, agent, limit_price, expiration_time)

class RandomStrategy(Strategy):

    """
        Randomly decides to invest in a currency using a random currency
        Represents people that are in the market without any knowledge (Zero-Intelligence Traders) whose aim is not 
        profit maximisation
    """
    def __init__(self, strategy_name, exchange_rates_data):
        super().__init__(strategy_name, exchange_rates_data)

    def closingConditionMet(self, agent, round):
        """" Agent's strategy for when to close the position """
        number = random.choice([0,1])
        return 1 == number

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
        
        symbol = currencyPairs[buyCurrency.getName()][sellCurrency.getName()]["exchange_symbol"]
        direction = currencyPairs[buyCurrency.getName()][sellCurrency.getName()]["direction"]
        exchange_rate = agent.currencyMarket.getCurrenciesExchangeRate(symbol, agent.round)

        limit_price = self.getLimitPrice(direction, exchange_rate)
        
        amountOfBuyingCurrency = self.getAmountOfBuyingCurrency(exchange_rate, direction, agent.wallet[sellCurrency]) # AGENT WANTS TO BUY 10 of currency

        expiration_time = random.choice(range(2,5))

        # AMOUNTOFSELLINGCURRENCY is useless here
        return Order("OPEN", buyCurrency, sellCurrency, amountOfBuyingCurrency, round, agent, limit_price, expiration_time) # creates an ORDER

class PivotPointStrategy(Strategy):
    """
        Follows Relative Strength Index indicator
    """
    def __init__(self, strategy_name, exchange_rates_data):
        super().__init__(strategy_name, exchange_rates_data)
        self.exchange_rates = exchange_rates_data
    
    def closingConditionMet(self, agent, round):
        """" Agent's strategy for when to close the position """
        """
            if support is broken and the market is in downward trend
        """
        investmentToClose = agent.currentInvestment

        buyCurrency = investmentToClose["soldCurrency"] # currency you used to invest
        sellCurrency = investmentToClose["boughtCurrency"] # currency you invested in

        exchange_rate_symbol = buyCurrency.symbol + "/" + sellCurrency.symbol # is this the right way around ?
                
        exchange_rate_data = self.exchange_rates[exchange_rate_symbol]
        # get support and the pivot points
        exchange_rate = agent.currencyMarket.getCurrenciesExchangeRate(exchange_rate_symbol, agent.round)
        important_points = self.getImportantPoints(exchange_rate_data, round)
        low = important_points[2]
        high = important_points[1]
        pivot_point = important_points[0]
        resistance = self.calculateResistance(low, pivot_point)
        support = self.calculateSupport(high, pivot_point)

        if self.isMarketTrendDown(pivot_point, exchange_rate):
            if self.hasBrokenSupportLevel(support, exchange_rate):
                return True
                
        return False

        # HARD refactor needed later :)  
   
    def makeOpenOrder(self, agent, round):
        """ wishes to exchange X for Y """

        """
            pseudo-code algorithm:

            step 1: seeing what the agent has and what it could do

            getCurrenciesInAgentsWallet : the ones that agent can sell to purchase / invest in another

            getCurrenciesAvailableInTheMarket : the ones that the agent can invest in

            step 2: choosing the currency to invest in and with

            for all possible currency pairs made from
            [ curr in market / curr in wallet ] or [ curr in wallet / curr in market ]

                find the first pair for which both: 
                    market trend is UP (pivot point passed going up) and if it has BROKEN a resistance level
                    ^ MUST BE CALCULATED FOR EVERY PAIR
            
            choose to invest in that one
            if none -- not a good time to invest <- do nothing

            step 3: make the order

            how much to buy
            what limit_price
            expiration_time

            return ORDER : ) 
        """
        
        print ("AGENT IS TRYING TO MAKE AN OPEN ORDER")

        currencies_in_wallet = random.sample(list(agent.wallet.keys()), len(list(agent.wallet.keys())))
        currencies_in_market = random.sample(agent.currencyMarket.getAvailableCurrencies(), len(agent.currencyMarket.getAvailableCurrencies()))

        print (currencies_in_market)
        print (currencies_in_wallet)

        currencyPair = self.findCurrencyPairToInvest(currencies_in_market, currencies_in_wallet, round)

        if currencyPair == None: return None

        buyCurrency = currencyPair[0]
        sellCurrency = currencyPair[1]
        exchange_rate_symbol = buyCurrency.symbol + "/" + sellCurrency.symbol

        exchange_rate = agent.currencyMarket.getCurrenciesExchangeRate(exchange_rate_symbol, agent.round)
        direction = currencyPairs[buyCurrency.getName()][sellCurrency.getName()]["direction"]
        limit_price = self.getLimitPrice(direction, exchange_rate)
        amountOfBuyingCurrency = self.getAmountOfBuyingCurrency(exchange_rate, direction, agent.wallet[sellCurrency]) # AGENT WANTS TO BUY 10 of currency
        
        expiration_time = random.choice(range(2,5))

        return Order("OPEN", buyCurrency, sellCurrency, amountOfBuyingCurrency, round, agent, limit_price, expiration_time) # creates an ORDER

    def findCurrencyPairToInvest(self, currencies_in_market, currencies_in_wallet, round):
        for possible_selling_currency in currencies_in_wallet:
            possible_selling_currency_symbol = possible_selling_currency.symbol

            for possible_buying_currency in currencies_in_market:
                possible_buying_currency_symbol = possible_buying_currency.symbol
                
                if possible_selling_currency_symbol == possible_buying_currency_symbol: continue

                exchange_rate_symbol = possible_buying_currency_symbol + "/" + possible_selling_currency_symbol # is this the right way around ?
                
                exchange_rate_data = self.exchange_rates[exchange_rate_symbol]
                current_exchange_rate_price = exchange_rate_data[round]
                
                # find pivot point resistance support etc ... 

                important_points = self.getImportantPoints(exchange_rate_data, round)
                low = important_points[2]
                high = important_points[1]
                pivot_point = important_points[0]
                resistance = self.calculateResistance(low, pivot_point)
                support = self.calculateSupport(high, pivot_point)
                
                # is market trend up?
                # has it just broken a resistance level ?
                if self.isMarketTrendUp(pivot_point, current_exchange_rate_price):
                    if self.hasBrokenResistanceLevel(resistance, current_exchange_rate_price):
                        return [possible_buying_currency, possible_selling_currency]
        return None

    def getImportantPoints(self, exchange_rate_data, round):
        """ formula: pivot_point = (prev_high + prev_low + prev_close) / 3 """
        window = round - 7 # 
        exchange_rate_data_past_7_days = exchange_rate_data.iloc[range(window, round)]
        max = exchange_rate_data_past_7_days.max()
        min = exchange_rate_data_past_7_days.min()
        close = exchange_rate_data_past_7_days.iloc[-1] # last value

        pivot_point = (max + min + close) / 3
        return [pivot_point, max, min, close]

    def calculateResistance(self, low, pivot_point):
        """ formula: resistance = 2 * P - L """
        return 2 * pivot_point - low
    
    def calculateSupport(self, high, pivot_point):
        """ formula: resistance = 2*P - H """
        return 2 * pivot_point - high

    def isMarketTrendUp(self, pivot_point, current_exchange):
        if current_exchange > pivot_point:
            return True
        return False

    def isMarketTrendDown(self, pivot_point, current_exchange):
        if current_exchange < pivot_point:
            return True
        return False

    def hasBrokenResistanceLevel(self, resistance, current_exchange):
        print (current_exchange, " > ", resistance)
        if current_exchange > resistance:
            return True
        return False

    def hasBrokenSupportLevel(self, support, current_exchange):
        if current_exchange < support:
            return True
        return False

    def currenciesAsSymbols(self, currencies):
        symbols_list = []
        for currency in currencies:
            symbols_list.append(currency.symbol)
        
        return symbols_list

    def makeCloseOrder(self, agent, round):
        """ wishes to exchange Y for X """

        investmentToClose = agent.currentInvestment # close current investment // investment is a dictionary object

        buyCurrency = investmentToClose["soldCurrency"] # currency you used to invest
        sellCurrency = investmentToClose["boughtCurrency"] # currency you invested in
        amountOfBuyingCurrency = investmentToClose["amount"] #
        
        symbol = currencyPairs[buyCurrency.getName()][sellCurrency.getName()]["exchange_symbol"]
        direction = currencyPairs[buyCurrency.getName()][sellCurrency.getName()]["direction"]
        exchange_rate = agent.currencyMarket.getCurrenciesExchangeRate(symbol, agent.round)
        limit_price = self.getLimitPrice(direction, exchange_rate)

        expiration_time = random.choice(range(2,5))
        return Order("CLOSE", buyCurrency, sellCurrency, amountOfBuyingCurrency, round, agent, limit_price, expiration_time)


class MarketIndicators:

    def __init__(self, exchange_rates) -> None:
        self.exchange_rates = exchange_rates

    # exponential moving average
    # https://www.investopedia.com/terms/e/ema.asp
    # https://towardsdatascience.com/trading-toolbox-02-wma-ema-62c22205e2a9
    def getEMA(self, round, window, symbol):
        ema10 = self.exchange_rates[symbol].ewm(span = window, adjust= False).mean()
        df = pd.DataFrame()
        df["ema"] = numpy.round(ema10, decimals = 3)
        return df["ema"].values[round]

    # Moving average Convergence Divergence
    # https://www.investopedia.com/terms/m/macd.asp
    def getMACD(self, round):
        return self.getEMA(round, 12) - self.getEMA(round, 26)

    def get_X_day_moving_average(self, symbol, round, window):
        if round < window:
            return None
        else:
            total = 0
            for i in range(window):
                total += self.exchange_rates[symbol][round - i]
            return total / window

    def getExchangeRate(self, symbol, round):
        return self.exchange_rates[symbol][round]
