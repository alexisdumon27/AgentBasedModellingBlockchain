def getNumberOfEthereumTransactions(model) :
    return model.list_of_currencies[0].getNumOfTransactions()

def totalTransactions(model):
    total = 0
    for currency in model.list_of_currencies:
        total += currency.getNumOfTransactions()
    return total

# Binance Coin

def getBNBtoUS(model):
    return model.bnb_usd

def getBNBtoUSDT(model):
    return model.bnb_usdt

def getBNBtoBTC(model):
    return model.bnb_btc

def getBNBtoETH(model):
    return model.bnb_eth

def getDesiredExchangeRate(model):
    print (model.desired_exchange_rate)
    return model.desired_exchange_rate

def getMostWealthy(model):
    return [1, 3, 3, 27]

def getMostTradedCurrPair(model):
    return "ETH/BTC"