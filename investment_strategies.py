import random
import numpy

from currency_pairs import currencyPairs

class Strategy:
    """
        this will eventually be a superclass whose children have different implementations of the four methods
        each children will therefore represent a different type of strategy
    """
    def __init__(self):
        self.order_id = 0
        pass
    
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
        exchange_rate = agent.currencyMarket.getAllExchangeRates()[symbol]

        limit_price = self.getLimitPrice(direction, exchange_rate)
        
        amountOfBuyingCurrency = random.choice(range(2,10)) # AGENT WANTS TO BUY 10 of currency

        expiration_time = random.choice([2,3,4,5])

        # AMOUNTOFSELLINGCURRENCY is useless here
        return Order("OPEN", buyCurrency, sellCurrency, amountOfBuyingCurrency, round, agent, limit_price, expiration_time, self.order_id) # creates an ORDER

    def closingConditionMet(self, agent, round):
        """" Agent's strategy for when to close the position """
        return True

    def getLimitPrice(self, direction, exchange_rate):
        random_gauss_factor = self.getRandomDrawFromGaussian(exchange_rate, direction) # to add randomness
        return exchange_rate * random_gauss_factor # agent willing to buy at a slightly higher price

    # https://arxiv.org/pdf/cond-mat/0103600.pdf
    def getRandomDrawFromGaussian(self, exchange_rate, direction):
        # For orders: μ = current_exchange_rate * 1.01, σmin = 0.01 and σmax = 0.003.
        mean = 0.98
        if direction == "buy":
            mean *= 1.02
        return numpy.random.normal(loc = mean, scale = random.uniform(0.003, 0.01))

    def makeCloseOrder(self, agent, round):
        """ wishes to exchange Y for X """
        self.order_id += 1

        investmentToClose = agent.currentInvestment # close current investment // investment is an Order object
        
        buyCurrency = investmentToClose["soldCurrency"] # currency you used to invest
        sellCurrency = investmentToClose["boughtCurrency"] # currency you invested in
        amountOfBuyingCurrency = investmentToClose["amount"] #
        
        symbol = currencyPairs[buyCurrency.getName()][sellCurrency.getName()]["exchange_symbol"]
        exchange_rate = agent.currencyMarket.getAllExchangeRates()[symbol]

        expiration_time = random.choice([2,3,4,5])
        return Order("CLOSE", buyCurrency, sellCurrency, amountOfBuyingCurrency, round, agent, exchange_rate, expiration_time, self.order_id)

class Order:
    """
        a data structure containing all the relevant information for the order request of an agent
    """
    def __init__(self, orderType, buyCurrency, sellCurrency, amountOfBuyingCurrency, round, agent, limit_price, expiration_time, order_id):
        self.order_type = orderType
        self.buyCurrency = buyCurrency # currency agent wants to buy
        self.sellCurrency = sellCurrency # currency agent will sell in order to buy
        self.amountOfBuyingCurrency = amountOfBuyingCurrency # amount of buy currency agent wants to own :: DEPEND ON EXCHANGE_RATE
        self.timestep = round # 
        self.agent = agent #
        self.expiration_time = expiration_time
        self.order_id = order_id
        self.limit_price = limit_price
