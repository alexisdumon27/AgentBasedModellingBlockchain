marketIndicators = {
                "ethereum" : { 'moving_average_1' : 10, 'moving_average_5' : 5, 'moving_average_10' : 2 },
            }

currencyPairs = {
    "ethereum" : { # if you have ethereum to tether then you are buying eth and selling usdt
        "tether": {"exchange_symbol": "ETH/USDT", "direction" : "buy"}
    },
    "tether": {  # you are buying tether with ethereum
        "ethereum" : {"exchange_symbol": "ETH/USDT", "direction": "sell"}
    }
}

inverseCurrencyPair = {
    "ETH/USDT" : ["ethereum", "tether"],
    "USDT/ETH" : ["tether", "ethereum"]
}