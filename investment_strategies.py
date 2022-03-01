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
        # https://arxiv.org/pdf/cond-mat/0103600.pdf
        random_gauss_factor = self.getRandomDrawFromGaussian(direction) # to add randomness in limit_prices
        limit_price = 0
        while limit_price <= 0:
            limit_price = exchange_rate * random_gauss_factor
        return limit_price # agent willing to buy at a slightly higher price
    
    def getRandomDrawFromGaussian(self, direction):
        # For orders: μ = current_exchange_rate * 1.01, σmin = 0.01 and σmax = 0.003.
        mean = 0.98
        if direction == "buy":
            mean *= 1.02
        return numpy.random.normal(loc = mean, scale = random.uniform(0.003, 0.01))

    def makeOpenOrder(self, agent, round):
        """ wishes to exchange X for Y """
        currencies_in_wallet = random.sample(list(agent.wallet.keys()), len(list(agent.wallet.keys())))
        currencies_in_market = random.sample(agent.currencyMarket.getAvailableCurrencies(), len(agent.currencyMarket.getAvailableCurrencies()))
        currencyPair = self.findCurrencyPairToInvest(currencies_in_market, currencies_in_wallet, round) 
        if self.name == "MACD Strategy": "PPPPPPPPPPPPP"
        if currencyPair == None: 
            return None
        else:
            # creates an ORDER
            buyCurrency = currencyPair[0]
            sellCurrency = currencyPair[1]
            if self.name == "MACD Strategy": "PPPPPPPPPPPPP"
            return self.sendOrderRequest(agent, buyCurrency, sellCurrency)

    def findCurrencyPairToInvest(self, currencies_in_market, currencies_in_wallet, round):
        for possible_selling_currency in currencies_in_wallet:
            possible_selling_currency_symbol = possible_selling_currency.symbol

            for possible_buying_currency in currencies_in_market:
                possible_buying_currency_symbol = possible_buying_currency.symbol
                
                if possible_selling_currency_symbol == possible_buying_currency_symbol: continue

                exchange_rate_symbol = possible_buying_currency_symbol + "/" + possible_selling_currency_symbol # is this the right way around ?
                
                exchange_rate_data = self.exchange_rates[exchange_rate_symbol]
                current_exchange_rate_price = exchange_rate_data[round]
                if self.evaluateIndicators(round, current_exchange_rate_price, exchange_rate_data): # this method is subclass specific !!!
                    return [possible_buying_currency, possible_selling_currency]
        return None

    def sendOrderRequest(self, agent, buyCurrency, sellCurrency):
        exchange_rate_symbol = buyCurrency.symbol + "/" + sellCurrency.symbol

        exchange_rate = agent.currencyMarket.getCurrenciesExchangeRate(exchange_rate_symbol, agent.round)
        direction = currencyPairs[buyCurrency.getName()][sellCurrency.getName()]["direction"]
        limit_price = self.getLimitPrice(direction, exchange_rate)
        amountOfBuyingCurrency = self.getAmountOfBuyingCurrency(exchange_rate, direction, agent.wallet[sellCurrency]) # AGENT WANTS TO BUY 10 of currency
        
        expiration_time = random.choice(range(2,5))

        return Order("OPEN", buyCurrency, sellCurrency, amountOfBuyingCurrency, round, agent, limit_price, expiration_time)
    
    def closingConditionMet(self, agent, round):
        """" Agent's strategy for when to close the position """
        """
            if support is broken and the market is in downward trend
        """
        investmentToClose = agent.currentInvestment

        buyCurrency = investmentToClose["soldCurrency"] # currency you used to invest
        sellCurrency = investmentToClose["boughtCurrency"] # currency you invested in

        exchange_rate_symbol = buyCurrency.symbol + "/" + sellCurrency.symbol
                
        exchange_rate_data = self.exchange_rates[exchange_rate_symbol]
        exchange_rate = agent.currencyMarket.getCurrenciesExchangeRate(exchange_rate_symbol, agent.round)

        return self.haveStrategySpecificClosingConditionsBeenMet(round, exchange_rate, exchange_rate_data)

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
    
    def haveStrategySpecificClosingConditionsBeenMet(self, round, exchange_rate, exchange_rate_data):
        """" Agent's strategy for when to close the position """
        # get support and the pivot points
        important_points = self.getImportantPoints(exchange_rate_data, round)
        low = important_points[2]
        high = important_points[1]
        pivot_point = important_points[0]
        support = self.calculateSupport(high, pivot_point)

        if self.isMarketTrendDown(pivot_point, exchange_rate):
            if self.hasBrokenSupportLevel(support, exchange_rate):
                return True
                
        return False

    def evaluateIndicators(self, round, current_exchange_rate_price, exchange_rate_data):
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
                return True

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

class MovingAverageStrategy(Strategy):
    """
        Follows Moving average indicators
    """
    def __init__(self, strategy_name, exchange_rates_data):
        super().__init__(strategy_name, exchange_rates_data)
        self.exchange_rates = exchange_rates_data
    
    def haveStrategySpecificClosingConditionsBeenMet(self, round, exchange_rate, exchange_rate_data):
        """" Agent's strategy for when to close the position """
        # get support and the pivot points
        if self.isPriceMovementShowingStrongSell(exchange_rate_data, round):
            return True

        if self.isComparingMovingAveragesShowingStrongSell(exchange_rate_data, round):
            return True
        
        return False

    def evaluateIndicators(self, round, current_exchange_rate_price, exchange_rate_data):
        
        if self.isPriceMovementShowingStrongBuy(exchange_rate_data, round):
            return True

        if self.isComparingMovingAveragesShowingStrongBuy(exchange_rate_data, round):
            return True
        
        return False
    
    def isPriceMovementShowingStrongBuy(self, exchange_rate_data, round):
        if self.isXDayMovingAverageRising(round, 5, exchange_rate_data) and self.hasPriceCrossedFromBelowXDayMovingAverage(round, 5, exchange_rate_data): 
            return True

    def hasPriceCrossedFromBelowXDayMovingAverage(self, round, range, exchange_rate_data):
        current_price = exchange_rate_data[round]
        previous_price = exchange_rate_data[round - 1]
        current_moving_average = self.getXDayMovingAverage(round, range, exchange_rate_data)
        previous_moving_average = self.getXDayMovingAverage(round - 1, range, exchange_rate_data)

        if previous_price < previous_moving_average and current_price > current_moving_average:
            return True
        return False

    def isXDayMovingAverageRising(self, round, range, exchange_rate_data):
        """ rising if current round moving avg higher than previous round """
        current_moving_average_X_day = self.getXDayMovingAverage(round, range, exchange_rate_data)
        previous_moving_average_X_day = self.getXDayMovingAverage(round - 1, range, exchange_rate_data)
        if current_moving_average_X_day > previous_moving_average_X_day:
            return True
        return False

    def isComparingMovingAveragesShowingStrongBuy(self, exchange_rate_data, round):
        shorter_period = 5
        longer_period = 20
        if (self.isXDayMovingAverageRising(round, shorter_period, exchange_rate_data) and self.isXDayMovingAverageRising(round, longer_period, exchange_rate_data)
            and self.hasShorterPeriodCrossedLongerPeriodFromBelow(round, shorter_period, longer_period, exchange_rate_data) ):
            return True

    def hasShorterPeriodCrossedLongerPeriodFromBelow(self, round, shorter_period, longer_period, exchange_rate_data):
        previous_short_period_day_moving_average = self.getXDayMovingAverage(round - 1, shorter_period, exchange_rate_data)
        current_short_period_day_moving_average = self.getXDayMovingAverage(round, shorter_period, exchange_rate_data)

        previous_long_period_day_moving_average = self.getXDayMovingAverage(round - 1, longer_period, exchange_rate_data)
        current_long_period_day_moving_average = self.getXDayMovingAverage(round, longer_period, exchange_rate_data)

        if previous_short_period_day_moving_average < previous_long_period_day_moving_average and current_short_period_day_moving_average > current_long_period_day_moving_average:
            return True
        return False

    def getXDayMovingAverage(self, round, period, exchange_rate_data):
        # exchange_rate_data is already currency specific
        if round < period:
            period = round
        total = 0
        for i in range(period):
            total += exchange_rate_data[round - i]
        return total / period

    def isPriceMovementShowingStrongSell(self, exchange_rate_data, round):
        if self.isXDayMovingAverageFalling(round, 5, exchange_rate_data) and self.hasPriceCrossedFromAboveXDayMovingAverage(round, 5, exchange_rate_data): 
            return True

    def isXDayMovingAverageFalling(self, round, range, exchange_rate_data):
        current_moving_average_X_day = self.getXDayMovingAverage(round, range, exchange_rate_data)
        previous_moving_average_X_day = self.getXDayMovingAverage(round - 1, range, exchange_rate_data)
        if current_moving_average_X_day < previous_moving_average_X_day:
            return True
        return False
    
    def hasPriceCrossedFromAboveXDayMovingAverage(self, round, range, exchange_rate_data):
        current_price = exchange_rate_data[round]
        previous_price = exchange_rate_data[round - 1]
        current_moving_average = self.getXDayMovingAverage(round, range, exchange_rate_data)
        previous_moving_average = self.getXDayMovingAverage(round - 1, range, exchange_rate_data)

        if previous_price > previous_moving_average and current_price < current_moving_average:
            return True
        return False

    def isComparingMovingAveragesShowingStrongSell(self, exchange_rate_data, round):
        shorter_period = 5
        longer_period = 20
        if (self.isXDayMovingAverageFalling(round, shorter_period, exchange_rate_data) and self.isXDayMovingAverageFalling(round, longer_period, exchange_rate_data)
            and self.hasShorterPeriodCrossedLongerPeriodFromAbove(round, shorter_period, longer_period, exchange_rate_data) ):
            return True
    
    def hasShorterPeriodCrossedLongerPeriodFromAbove(self, round, shorter_period, longer_period, exchange_rate_data):
        previous_short_period_day_moving_average = self.getXDayMovingAverage(round - 1, shorter_period, exchange_rate_data)
        current_short_period_day_moving_average = self.getXDayMovingAverage(round, shorter_period, exchange_rate_data)

        previous_long_period_day_moving_average = self.getXDayMovingAverage(round - 1, longer_period, exchange_rate_data)
        current_long_period_day_moving_average = self.getXDayMovingAverage(round, longer_period, exchange_rate_data)

        if previous_short_period_day_moving_average > previous_long_period_day_moving_average and current_short_period_day_moving_average < current_long_period_day_moving_average:
            return True
        return False

class MACDStrategy(Strategy):
    """
        Follows MACD indicator
    """
    def __init__(self, strategy_name, exchange_rates_data):
        super().__init__(strategy_name, exchange_rates_data)
        self.exchange_rates = exchange_rates_data
    
    def haveStrategySpecificClosingConditionsBeenMet(self, round, exchange_rate, exchange_rate_data):
        """" Agent's strategy for when to close the position """
        # get support and the pivot points
        if self.hasCrossedSignalLineFromAbove(exchange_rate_data, round):
            return True

        if self.hasCrossedOverXAxisFromAbove(exchange_rate_data, round):
            return True
        
        if self.IsThereConvergenceBetweenMACDAndPriceDownward(exchange_rate_data, round):
            return True
        
        return False

    def evaluateIndicators(self, round, current_exchange_rate_price, exchange_rate_data):
        print ("hello")
        if self.hasCrossedSignalLineFromBelow(exchange_rate_data, round):
            print ("condition 1")
            return True

        if self.hasCrossedOverXAxisFromBelow(exchange_rate_data, round):
            print ("condition 2")
            return True
        
        if self.IsThereConvergenceBetweenMACDAndPriceUpward(exchange_rate_data, round):
            print ("condition 3")
            return True
        
        return False
    
    def getXDayExponentialMovingAverage(self, round, period, exchange_rate_data):
        """ using pandas ewm formula -- returns a pandas column """
        temp_df = exchange_rate_data.ewm(span = period, adjust = False).mean()
        return temp_df.iloc[round]

    def getMACDLine(self, exchange_rate_data, round):
        EMA_12_days = self.getXDayExponentialMovingAverage(round, 12, exchange_rate_data)
        EMA_26_days = self.getXDayExponentialMovingAverage(round, 26, exchange_rate_data)
        return EMA_12_days - EMA_26_days

    def getSignalLine(self, exchange_rate_data, round):
        return self.getXDayExponentialMovingAverage(round, 9, exchange_rate_data)

    def IsThereConvergenceBetweenMACDAndPriceUpward(self, exchange_rate_data, round):
        """ convergence upwards if both are rising """
        if self.isMACDLineRising(exchange_rate_data, round) and self.isExchangeRateRising(exchange_rate_data, round):
            return True
        return False    

    def IsThereConvergenceBetweenMACDAndPriceDownward(self, exchange_rate_data, round):
        """ convergence upwards if both are rising """
        if self.isMACDLineFalling(exchange_rate_data, round) and self.isExchangeRateFalling(exchange_rate_data, round):
            return True
        return False    

    def isExchangeRateRising(self, exchange_rate_data, round):
        previous_exchange_rate = exchange_rate_data.iloc[round - 1]
        current_exchange_rate = exchange_rate_data.iloc[round]
        if previous_exchange_rate < current_exchange_rate:
            return True
        return False
    
    def isExchangeRateFalling(self, exchange_rate_data, round):
        previous_exchange_rate = exchange_rate_data.iloc[round - 1]
        current_exchange_rate = exchange_rate_data.iloc[round]
        if previous_exchange_rate > current_exchange_rate:
            return True
        return False

    def hasCrossedSignalLineFromBelow(self, exchange_rate_data, round):
        if self.isMACDLineRising(exchange_rate_data, round) and self.hasMACDLineHasCrossedSignalLineFromBelow(exchange_rate_data, round):
            return True
        return False

    def hasCrossedSignalLineFromAbove(self, exchange_rate_data, round):
        if self.isMACDLineFalling(exchange_rate_data, round) and self.hasMACDLineHasCrossedSignalLineFromAbove(exchange_rate_data, round):
            return True
        return False

    def isMACDLineRising(self, exchange_rate_data, round):
        previous_MACD_line = self.getMACDLine(exchange_rate_data, round - 1)
        current_MACD_line = self.getMACDLine(exchange_rate_data, round)
        if current_MACD_line > previous_MACD_line:
            return True
        return False

    def isMACDLineFalling(self, exchange_rate_data, round):
        previous_MACD_line = self.getMACDLine(exchange_rate_data, round - 1)
        current_MACD_line = self.getMACDLine(exchange_rate_data, round)
        if current_MACD_line < previous_MACD_line:
            return True
        return False

    def hasCrossedOverXAxisFromBelow(self, exchange_rate_data, round):
        if self.isMACDLineRising(exchange_rate_data, round) and self.hasMACDLineHasCrossedXAxisFromBelow(exchange_rate_data, round):
            return True
        return False
    
    def hasCrossedOverXAxisFromAbove(self, exchange_rate_data, round):
        if self.isMACDLineFalling(exchange_rate_data, round) and self.hasMACDLineHasCrossedXAxisFromAbove(exchange_rate_data, round):
            return True
        return False

    def hasMACDLineHasCrossedXAxisFromBelow(self, exchange_rate_data, round):
        previous_MACD_line = self.getMACDLine(exchange_rate_data, round - 1)
        current_MACD_line = self.getMACDLine(exchange_rate_data, round)

        if previous_MACD_line < 0 and current_MACD_line > 0:
            return True
        return False

    def hasMACDLineHasCrossedXAxisFromAbove(self, exchange_rate_data, round):
        previous_MACD_line = self.getMACDLine(exchange_rate_data, round - 1)
        current_MACD_line = self.getMACDLine(exchange_rate_data, round)

        if previous_MACD_line > 0 and current_MACD_line < 0:
            return True
        return False

    def hasMACDLineHasCrossedSignalLineFromBelow(self, exchange_rate_data, round):
        previous_MACD_line = self.getMACDLine(exchange_rate_data, round - 1)
        current_MACD_line = self.getMACDLine(exchange_rate_data, round)
        previous_signal_line = self.getSignalLine(exchange_rate_data, round - 1)
        current_signal_line = self.getSignalLine(exchange_rate_data, round)

        if previous_MACD_line < previous_signal_line and current_MACD_line > current_signal_line:
            return True
        return False

    def hasMACDLineHasCrossedSignalLineFromAbove(self, exchange_rate_data, round):
        previous_MACD_line = self.getMACDLine(exchange_rate_data, round - 1)
        current_MACD_line = self.getMACDLine(exchange_rate_data, round)
        previous_signal_line = self.getSignalLine(exchange_rate_data, round - 1)
        current_signal_line = self.getSignalLine(exchange_rate_data, round)

        if previous_MACD_line > previous_signal_line and current_MACD_line < current_signal_line:
            return True
        return False



    


