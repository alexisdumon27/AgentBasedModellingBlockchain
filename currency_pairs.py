currencyPairs = {
    "ethereum" : { # if you have ethereum to tether then you are buying eth and selling usdt/bnb/btc
        "tether": {"exchange_symbol": "ETH/USDT", "direction" : "buy"},
        "binance": {"exchange_symbol": "ETH/BNB", "direction": "buy"},
        "bitcoin": {"exchange_symbol": "ETH/BTC", "direction": "buy"}
    },
    "tether": {  # you are buying tether with ethereum
        "ethereum" : {"exchange_symbol": "ETH/USDT", "direction": "sell"}
    }
}