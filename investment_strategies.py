import random
import numpy
import pandas as pd
from currency_pairs import currencyPairs

class Strategy:
    """
        this will eventually be a superclass whose children have different implementations of the four methods
        each children will therefore represent a different type of strategy
    """
    def __init__(self, strategy_name):
        self.name = strategy_name
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
                    amount -= 0.1
                    return amount
            else:
                if amount > max_amount_to_sell:
                    amount -= 0.1
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




class RandomStrategy(Strategy):

    """
        Randomly decides to invest in a currency using a random currency
        Represents people that are in the market without any knowledge (Zero-Intelligence Traders) whose aim is not 
        profit maximisation
    """
    def __init__(self, strategy_name):
        super().__init__(strategy_name)

    def closingConditionMet(self, agent, round):
        """" Agent's strategy for when to close the position """
        return True

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
        
        symbol = currencyPairs[buyCurrency.getName()][sellCurrency.getName()]["exchange_symbol"]
        direction = currencyPairs[buyCurrency.getName()][sellCurrency.getName()]["direction"]
        exchange_rate = agent.currencyMarket.getCurrenciesExchangeRate(symbol, agent.round)

        limit_price = self.getLimitPrice(direction, exchange_rate)
        
        amountOfBuyingCurrency = self.getAmountOfBuyingCurrency(exchange_rate, direction, agent.wallet[sellCurrency]) # AGENT WANTS TO BUY 10 of currency

        expiration_time = random.choice(range(2,5))

        # AMOUNTOFSELLINGCURRENCY is useless here
        return Order("OPEN", buyCurrency, sellCurrency, amountOfBuyingCurrency, round, agent, limit_price, expiration_time) # creates an ORDER

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


class EMAStrategy(Strategy):
    """
        Follows Exponential Moving Average indicator
    """
    def __init__(self, strategy_name):
        super().__init__(strategy_name)
    
    def closingConditionMet(self, agent, round):
        """" Agent's strategy for when to close the position """
        return True

    def getEMA(self, currency_data):
        df = pd.DataFrame()
        df["ema"] = numpy.round(["ema10"], decimals = 3)
        return df["ema"].values[round]

        # HARD refactor needed later :)  
    def makeOpenOrder(self, agent, round):
        """ 
            If there is no current open position, then a long position is generated only if the close price is higher than EMA(n) and 
            a short position is generated only if the close price is lower than EMA(n). If a position is currently open, then this rule is ignored 
        """

        """
        pseudo-code
        Find the currency-pair with the most positive difference between their currentExchangeRate and EMA

        biggestPositiveDiff = 0
        currencyPairBiggestDiff = None
        For each currencyPairSymbol:
            getCurrentExchangeRate
            getEMA for that period and

        inverseCurrencyPair <- 
        make order with these two currencies 
        """
        # biggestPositiveDifference = 0
        # currencyPairBiggestDiff = None # symbol like ['USDT/ETH'] for example
        # listOfSymbols = 
        

        # AMOUNTOFSELLINGCURRENCY is useless here
        return Order("OPEN", buyCurrency, sellCurrency, amountOfBuyingCurrency, round, agent, limit_price, expiration_time) # creates an ORDER

    def makeCloseOrder(self, agent, round):
        """ wishes to exchange Y for X """

        return Order("CLOSE", buyCurrency, sellCurrency, amountOfBuyingCurrency, round, agent, limit_price, expiration_time)
        
class MACDStrategy(Strategy):
    """
        Follows Moving Average Convergence Divergence indicator
    """
    def __init__(self, strategy_name):
        super().__init__(strategy_name)

class RSIStrategy(Strategy):
    """
        Follows Relative Strength Index indicator
    """
    def __init__(self, strategy_name):
        super().__init__(strategy_name)

class TrendFollowerStrategy(Strategy):
    """
        Bases which and when to buy based on which currency_pair is the most bought
    """
    def __init__(self, strategy_name):
        super().__init__(strategy_name)


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
