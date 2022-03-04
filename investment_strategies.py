from cmath import nan
import random
import numpy


class Order:
    """
        a data structure containing all the relevant information for the order request of an agent
    """
    def __init__(self, orderType, buy_currency, sell_currency, amount_of_buying_currency, round, agent, limit_price, expiration_time):
        self.order_type = orderType # OPEN or CLOSE order
        self.buy_currency = buy_currency # currency agent wants to buy
        self.sell_currency = sell_currency # currency agent will sell in order to buy
        self.amount_of_buying_currency = amount_of_buying_currency # amount of buy currency agent wants to own :: DEPEND ON EXCHANGE_RATE
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
        self.exchange_rates_data = exchange_rates_data
        # agent_risk_level
        pass

    def getAmountOfBuyingCurrency(self, exchange_rate, max_amount_to_sell):
        # should buy amount proportional to exchange_rate and it should not exceed the max amount of the currency it is selling
        amount = 0.00 # go through all the numbers until you reach the max amount that they can sell
        while amount < 1000000:
            amount += 0.01
            if exchange_rate > 1:
                if amount * exchange_rate > max_amount_to_sell:
                    amount -= 0.01
                    return amount
            else:
                if amount > max_amount_to_sell:
                    amount -= 0.01
                    return amount

    def getLimitPrice(self, exchange_rate):
        # https://arxiv.org/pdf/cond-mat/0103600.pdf
        random_gauss_factor = self.getRandomDrawFromGaussian() # to add randomness in limit_prices
        limit_price = 0
        # WHAT AM I DOING HERE ???
        while limit_price <= 0:
            limit_price = exchange_rate * random_gauss_factor
        return limit_price # agent willing to buy at a slightly higher price
    
    def getRandomDrawFromGaussian(self):
        # For orders: μ = 0.98 / 1.02, σmin = 0.01 and σmax = 0.003.
        mean = 1
        return numpy.random.normal(loc = mean, scale = random.uniform(0.003, 0.01))

    def makeOpenOrder(self, agent, round):
        """ wishes to exchange X for Y """
        currencies_in_wallet = random.sample(list(agent.wallet.keys()), len(list(agent.wallet.keys())))
        currencies_in_market = random.sample(agent.currency_market.getAvailableCurrencies(), len(agent.currency_market.getAvailableCurrencies()))
        exchanging_currencies = self.findCurrencyPairToInvest(currencies_in_market, currencies_in_wallet, round) 
        if exchanging_currencies == None: 
            return None
        else:
            # creates an ORDER
            buy_currency = exchanging_currencies[0]
            sell_currency = exchanging_currencies[1]
            return self.sendOrderRequest(agent, buy_currency, sell_currency)

    def findCurrencyPairToInvest(self, currencies_in_market, currencies_in_wallet, round):
        for possible_selling_currency in currencies_in_wallet:
            possible_selling_currency_symbol = possible_selling_currency.symbol

            for possible_buying_currency in currencies_in_market:
                possible_buying_currency_symbol = possible_buying_currency.symbol
                
                if possible_selling_currency_symbol == possible_buying_currency_symbol: continue

                exchange_rate_symbol = possible_buying_currency_symbol + "/" + possible_selling_currency_symbol # is this the right way around ?
                
                if self.evaluateIndicators(round, exchange_rate_symbol): # this method is subclass specific !!!
                    return [possible_buying_currency, possible_selling_currency]
        return None

    def sendOrderRequest(self, agent, buy_currency, sell_currency):
        
        exchange_rate_symbol = buy_currency.symbol + "/" + sell_currency.symbol
        exchange_rate = agent.currency_market.getCurrenciesExchangeRate(exchange_rate_symbol, agent.round)

        limit_price = self.getLimitPrice(exchange_rate)
        amount_of_buying_currency = self.getAmountOfBuyingCurrency(limit_price, agent.wallet[sell_currency]) # AGENT WANTS TO BUY 10 of currency
        
        expiration_time = random.choice(range(2,5))

        return Order("OPEN", buy_currency, sell_currency, amount_of_buying_currency, agent.round, agent, limit_price, expiration_time)
    
    def closingConditionMet(self, agent, round):
        """" Agent's strategy for when to close the position """
        investmentToClose = agent.current_investment

        buy_currency = investmentToClose["sold_currency"] # currency you used to invest
        sell_currency = investmentToClose["bought_currency"] # currency you invested in

        exchange_rate_symbol = buy_currency.symbol + "/" + sell_currency.symbol

        return self.haveStrategySpecificClosingConditionsBeenMet(round, exchange_rate_symbol)
    
    def makeCloseOrder(self, agent, round):
        """ wishes to exchange Y for X """

        investment_to_close = agent.current_investment # close current investment // investment is a dictionary object
        buy_currency = investment_to_close["sold_currency"] # currency you used to invest
        sell_currency = investment_to_close["bought_currency"] # currency you invested in
        amount_of_buying_currency = investment_to_close["amount"]

        symbol = buy_currency.symbol + "/" + sell_currency.symbol
        exchange_rate = agent.currency_market.getCurrenciesExchangeRate(symbol, agent.round)
        limit_price = self.getLimitPrice(exchange_rate)

        expiration_time = random.choice(range(2,5))
        return Order("CLOSE", buy_currency, sell_currency, amount_of_buying_currency, round, agent, limit_price, expiration_time)

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

        agentWallet = agent.wallet
        currenciesInWallet = list(agentWallet.keys())
        sell_currency = random.choice(currenciesInWallet) # currency agent has in its wallet that he wants to exchange (selling this to buy)

        currencies = agent.currency_market.getAvailableCurrencies() # list of available currencies in the market
        buy_currency = None
        while buy_currency == None:
            potentialCurrency = random.choice(currencies)
            if potentialCurrency != sell_currency:
                buy_currency = potentialCurrency
        
        exchange_symbol = buy_currency.symbol + "/" + sell_currency.symbol
        exchange_rate = agent.currency_market.getCurrenciesExchangeRate(exchange_symbol, agent.round)

        limit_price = self.getLimitPrice(exchange_rate)
        
        amount_of_buying_currency = self.getAmountOfBuyingCurrency(exchange_rate, agent.wallet[sell_currency]) # AGENT WANTS TO BUY 10 of currency

        expiration_time = random.choice(range(2,5))

        return Order("OPEN", buy_currency, sell_currency, amount_of_buying_currency, round, agent, limit_price, expiration_time) # creates an ORDER

class PivotPointStrategy(Strategy):
    """
        Follows Relative Strength Index indicator
    """
    def __init__(self, strategy_name, exchange_rates_data):
        super().__init__(strategy_name, exchange_rates_data)
        self.exchange_rates_data = exchange_rates_data
    
    def haveStrategySpecificClosingConditionsBeenMet(self, round, symbol):
        """" Agent's strategy for when to close the position """
        # get support and the pivot points
        symbol_exchange_rate_data = self.exchange_rates_data[symbol]
        important_points = self.getImportantPoints(symbol_exchange_rate_data, round)
        high = important_points[1]
        pivot_point = important_points[0]
        support = self.calculateSupport(high, pivot_point)

        if self.isMarketTrendDown(pivot_point, symbol_exchange_rate_data):
            if self.hasBrokenSupportLevel(support, symbol_exchange_rate_data):
                return True
                
        return False

    def evaluateIndicators(self, round, symbol):
        symbol_exchange_rate_data = self.exchange_rates_data[symbol]
        important_points = self.getImportantPoints(symbol_exchange_rate_data, round)
        low = important_points[2]
        pivot_point = important_points[0]
        resistance = self.calculateResistance(low, pivot_point)

        current_exchange_rate_price = symbol_exchange_rate_data[round]
        if self.isMarketTrendUp(pivot_point, current_exchange_rate_price):
            if self.hasBrokenResistanceLevel(resistance, current_exchange_rate_price):
                return True

    def getImportantPoints(self, exchange_rate_data, round):
        """ formula: pivot_point = (prev_high + prev_low + prev_close) / 3 """
        day_in_minutes = 7 * 24 * 60
        window = round - day_in_minutes # 
        exchange_rate_data_past_day = exchange_rate_data.iloc[range(window, round)]
        max = exchange_rate_data_past_day.max()
        min = exchange_rate_data_past_day.min()
        close = exchange_rate_data_past_day.iloc[-1] # last value

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
        self.exchange_rates_data = exchange_rates_data
    
    def haveStrategySpecificClosingConditionsBeenMet(self, round, symbol):
        """" Agent's strategy for when to close the position """
        # get support and the pivot points
        if self.isPriceMovementShowingStrongSell(symbol, round):
            return True

        if self.isComparingMovingAveragesShowingStrongSell(symbol, round):
            return True
        
        return False

    def evaluateIndicators(self, round, symbol):
        if self.isPriceMovementShowingStrongBuy(symbol, round):
            return True

        if self.isComparingMovingAveragesShowingStrongBuy(symbol, round):
            return True
        
        return False
    
    def isPriceMovementShowingStrongBuy(self, symbol, round):
        _5_days_in_min = 5 * 24 * 60
        if self.isXDayMovingAverageRising(round, _5_days_in_min, symbol) and self.hasPriceCrossedFromBelowXDayMovingAverage(round, _5_days_in_min, symbol): 
            return True

    def hasPriceCrossedFromBelowXDayMovingAverage(self, round, range, symbol):
        current_price = self.exchange_rates_data[symbol][round]
        previous_price = self.exchange_rates_data[symbol][round - 1]
        current_moving_average = self.getXDayMovingAverage(round, range, symbol)
        previous_moving_average = self.getXDayMovingAverage(round - 1, range, symbol)

        if previous_price < previous_moving_average and current_price > current_moving_average:
            return True
        return False

    def isXDayMovingAverageRising(self, round, range, symbol):
        """ rising if current round moving avg higher than previous round """
        current_moving_average_X_day = self.getXDayMovingAverage(round, range, symbol)
        previous_moving_average_X_day = self.getXDayMovingAverage(round - 1, range, symbol)
        if current_moving_average_X_day > previous_moving_average_X_day:
            return True
        return False

    def isComparingMovingAveragesShowingStrongBuy(self, symbol, round):
        shorter_period = 5 * 24 * 60
        longer_period = 20 * 24 * 60
        if (self.isXDayMovingAverageRising(round, shorter_period, symbol) and self.isXDayMovingAverageRising(round, longer_period, symbol)
            and self.hasShorterPeriodCrossedLongerPeriodFromBelow(round, shorter_period, longer_period, symbol) ):
            return True

    def hasShorterPeriodCrossedLongerPeriodFromBelow(self, round, shorter_period, longer_period, symbol):
        previous_short_period_day_moving_average = self.getXDayMovingAverage(round - 1, shorter_period, symbol)
        current_short_period_day_moving_average = self.getXDayMovingAverage(round, shorter_period, symbol)

        previous_long_period_day_moving_average = self.getXDayMovingAverage(round - 1, longer_period, symbol)
        current_long_period_day_moving_average = self.getXDayMovingAverage(round, longer_period, symbol)

        if previous_short_period_day_moving_average < previous_long_period_day_moving_average and current_short_period_day_moving_average > current_long_period_day_moving_average:
            return True
        return False

    def getXDayMovingAverage(self, round, period, symbol):
        # exchange_rate_data is already currency specific
        if round < period:
            period = round
        total = 0
        for i in range(period):
            total += self.exchange_rates_data[symbol][round - i]
        return total / period

    def isPriceMovementShowingStrongSell(self, symbol, round):
        _5_days_in_min = 5 * 24 * 60
        if self.isXDayMovingAverageFalling(round, _5_days_in_min, symbol) and self.hasPriceCrossedFromAboveXDayMovingAverage(round, _5_days_in_min, symbol): 
            return True

    def isXDayMovingAverageFalling(self, round, range, symbol):
        current_moving_average_X_day = self.getXDayMovingAverage(round, range, symbol)
        previous_moving_average_X_day = self.getXDayMovingAverage(round - 1, range, symbol)
        if current_moving_average_X_day < previous_moving_average_X_day:
            return True
        return False
    
    def hasPriceCrossedFromAboveXDayMovingAverage(self, round, range, symbol):
        current_price = self.exchange_rates_data[symbol][round]
        previous_price = self.exchange_rates_data[symbol][round - 1]
        current_moving_average = self.getXDayMovingAverage(round, range, symbol)
        previous_moving_average = self.getXDayMovingAverage(round - 1, range, symbol)

        if previous_price > previous_moving_average and current_price < current_moving_average:
            return True
        return False

    def isComparingMovingAveragesShowingStrongSell(self, symbol, round):
        shorter_period = 5 * 24 * 60
        longer_period = 20 * 24 * 60
        if (self.isXDayMovingAverageFalling(round, shorter_period, symbol) and self.isXDayMovingAverageFalling(round, longer_period, symbol)
            and self.hasShorterPeriodCrossedLongerPeriodFromAbove(round, shorter_period, longer_period, symbol) ):
            return True
    
    def hasShorterPeriodCrossedLongerPeriodFromAbove(self, round, shorter_period, longer_period, symbol):
        previous_short_period_day_moving_average = self.getXDayMovingAverage(round - 1, shorter_period, symbol)
        current_short_period_day_moving_average = self.getXDayMovingAverage(round, shorter_period, symbol)

        previous_long_period_day_moving_average = self.getXDayMovingAverage(round - 1, longer_period, symbol)
        current_long_period_day_moving_average = self.getXDayMovingAverage(round, longer_period, symbol)

        if previous_short_period_day_moving_average > previous_long_period_day_moving_average and current_short_period_day_moving_average < current_long_period_day_moving_average:
            return True
        return False

class MACDStrategy(Strategy):
    """
        Follows MACD indicator
    """
    def __init__(self, strategy_name, exchange_rates_data):
        super().__init__(strategy_name, exchange_rates_data)
        self.exchange_rates_data = exchange_rates_data
    
    def haveStrategySpecificClosingConditionsBeenMet(self, round, symbol):
        """" Agent's strategy for when to close the position """
        # get support and the pivot points
        if self.hasCrossedSignalLineFromAbove(symbol, round):
            return True

        if self.hasCrossedOverXAxisFromAbove(symbol, round):
            return True
        
        if self.IsThereConvergenceBetweenMACDAndPriceDownward(symbol, round):
            return True
        
        return False

    def evaluateIndicators(self, round, symbol):        
        if self.hasCrossedSignalLineFromBelow(symbol, round):
            return True

        if self.hasCrossedOverXAxisFromBelow(symbol, round):
            return True
        
        if self.IsThereConvergenceBetweenMACDAndPriceUpward(symbol,round):
            return True
        
        return False
    
    def getXDayExponentialMovingAverage(self, round, period, symbol):
        """ using pandas ewm formula -- returns a pandas column """
        column_name = str(period) + "_ema_" + symbol
        return self.exchange_rates_data[column_name].iloc[round]

    def getMACDLine(self, symbol, round):
        EMA_12_days = self.getXDayExponentialMovingAverage(round, 12, symbol)
        EMA_26_days = self.getXDayExponentialMovingAverage(round, 26, symbol)
        return EMA_12_days - EMA_26_days

    def getSignalLine(self, symbol, round):
        return self.getXDayExponentialMovingAverage(round, 9, symbol)

    def IsThereConvergenceBetweenMACDAndPriceUpward(self, symbol, round):
        """ convergence upwards if both are rising """
        if self.isMACDLineRising(symbol, round) and self.isExchangeRateRising(symbol, round):
            return True
        return False    

    def IsThereConvergenceBetweenMACDAndPriceDownward(self, symbol, round):
        """ convergence upwards if both are rising """
        if self.isMACDLineFalling(symbol, round) and self.isExchangeRateFalling(symbol, round):
            return True
        return False    

    def isExchangeRateRising(self, symbol, round):
        previous_exchange_rate = self.exchange_rates_data[symbol].iloc[round - 1]
        current_exchange_rate = self.exchange_rates_data[symbol].iloc[round]
        if previous_exchange_rate < current_exchange_rate:
            return True
        return False
    
    def isExchangeRateFalling(self, symbol, round):
        previous_exchange_rate = self.exchange_rates_data[symbol].iloc[round - 1]
        current_exchange_rate = self.exchange_rates_data[symbol].iloc[round]
        if previous_exchange_rate > current_exchange_rate:
            return True
        return False

    def hasCrossedSignalLineFromBelow(self, symbol, round):
        if self.isMACDLineRising(symbol, round) and self.hasMACDLineHasCrossedSignalLineFromBelow(symbol, round):
            return True
        return False

    def hasCrossedSignalLineFromAbove(self, symbol, round):
        if self.isMACDLineFalling(symbol, round) and self.hasMACDLineHasCrossedSignalLineFromAbove(symbol, round):
            return True
        return False

    def isMACDLineRising(self, symbol, round):
        previous_MACD_line = self.getMACDLine(symbol, round - 1)
        current_MACD_line = self.getMACDLine(symbol, round)
        if current_MACD_line > previous_MACD_line:
            return True
        return False

    def isMACDLineFalling(self, symbol, round):
        previous_MACD_line = self.getMACDLine(symbol, round - 1)
        current_MACD_line = self.getMACDLine(symbol, round)
        if current_MACD_line < previous_MACD_line:
            return True
        return False

    def hasCrossedOverXAxisFromBelow(self, symbol, round):
        if self.isMACDLineRising(symbol, round) and self.hasMACDLineHasCrossedXAxisFromBelow(symbol, round):
            return True
        return False
    
    def hasCrossedOverXAxisFromAbove(self, symbol, round):
        if self.isMACDLineFalling(symbol, round) and self.hasMACDLineHasCrossedXAxisFromAbove(symbol, round):
            return True
        return False

    def hasMACDLineHasCrossedXAxisFromBelow(self, symbol, round):
        previous_MACD_line = self.getMACDLine(symbol, round - 1)
        current_MACD_line = self.getMACDLine(symbol, round)

        if previous_MACD_line < 0 and current_MACD_line > 0:
            return True
        return False

    def hasMACDLineHasCrossedXAxisFromAbove(self, symbol, round):
        previous_MACD_line = self.getMACDLine(symbol, round - 1)
        current_MACD_line = self.getMACDLine(symbol, round)

        if previous_MACD_line > 0 and current_MACD_line < 0:
            return True
        return False

    def hasMACDLineHasCrossedSignalLineFromBelow(self, symbol, round):
        previous_MACD_line = self.getMACDLine(symbol, round - 1)
        current_MACD_line = self.getMACDLine(symbol, round)
        previous_signal_line = self.getSignalLine(symbol, round - 1)
        current_signal_line = self.getSignalLine(symbol, round)

        if previous_MACD_line < previous_signal_line and current_MACD_line > current_signal_line:
            return True
        return False

    def hasMACDLineHasCrossedSignalLineFromAbove(self, symbol, round):
        previous_MACD_line = self.getMACDLine(symbol, round - 1)
        current_MACD_line = self.getMACDLine(symbol, round)
        previous_signal_line = self.getSignalLine(symbol, round - 1)
        current_signal_line = self.getSignalLine(symbol, round)

        if previous_MACD_line > previous_signal_line and current_MACD_line < current_signal_line:
            return True
        return False

class RSIStrategy(Strategy):
    """
        This use the Relative strength index as the indicator for entry and exit of the market
    """
    
    def __init__(self, strategy_name, exchange_rates_data):
        super().__init__(strategy_name, exchange_rates_data)
        self.exchange_rates_data = exchange_rates_data
        
    def haveStrategySpecificClosingConditionsBeenMet(self, round, symbol):
        """" Agent's strategy for when to close the position """
        if self.hasRSICrossedOverboughtSignal(round, symbol):
            return True
        if self.hasUpwardWeakness(self, round, symbol):
            return True
        return False

    def evaluateIndicators(self, round, symbol):
        if self.hasRSICrossedOversoldSignal(round, symbol):
            return True
        if self.hasDownwardWeakness(round, symbol):
            return True
        return False
    
    def hasDownwardWeakness(self, round, symbol):
        """ 
            If exchange rate reaches 10 (X) day low but indicator does not 
            If the price falls to a new low, but the indicator does not, that may be a sign of the downtrend weakness.
        """
        current_exchange_rate = self.exchange_rates_data[symbol].iloc[round]
        min_exchange_rate_past_10_days = self.exchange_rates_data[symbol].iloc[round-9:round+1].min()
        if current_exchange_rate == min_exchange_rate_past_10_days:
            current_rsi = self.getRelativeStrengthIndex(round, symbol)
            column_name = "rsi_" + symbol
            min_rsi_past_10_days = self.exchange_rates_data[column_name].iloc[round-9:round+1].min()
            if current_rsi == min_rsi_past_10_days:
                return True
        return False

    def hasRSICrossedOversoldSignal(self, round, exchange_rate_data):
        previous_rsi = self.getRelativeStrengthIndex(round - 1, exchange_rate_data)
        current_rsi = self.getRelativeStrengthIndex(round, exchange_rate_data)
        if previous_rsi == None or current_rsi == None: return False
        if previous_rsi > current_rsi and current_rsi < 30:
            return True
        return False

    def hasUpwardWeakness(self, round, symbol):
        """ 
            If exchange rate reaches 10 (X) day low but indicator does not 
            If the price falls to a new low, but the indicator does not, that may be a sign of the downtrend weakness.
        """
        current_exchange_rate = self.exchange_rates_data[symbol].iloc[round]
        max_exchange_rate_past_10_days = self.exchange_rates_data[symbol].iloc[round-9:round+1].max()
        if current_exchange_rate == max_exchange_rate_past_10_days:
            current_rsi = self.getRelativeStrengthIndex(round, symbol)
            column_name = "rsi_" + symbol
            max_rsi_past_10_days = self.exchange_rates_data[column_name].iloc[round-9:round+1].max()
            if current_rsi == max_rsi_past_10_days:
                return True
        return False

    def hasRSICrossedOverboughtSignal(self, round, exchange_rate_data):
        previous_rsi = self.getRelativeStrengthIndex(round - 1, exchange_rate_data)
        current_rsi = self.getRelativeStrengthIndex(round, exchange_rate_data)
        if previous_rsi == None or current_rsi == None: return False
        if previous_rsi < current_rsi and current_rsi > 70:
            return True
        return False

    def getRelativeStrengthIndex(self, round, symbol):
        column_name = "rsi_" + symbol
        rsi = self.exchange_rates_data[column_name].iloc[round]
        if rsi != nan:
            return rsi
        return None