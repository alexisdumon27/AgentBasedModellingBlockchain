import unittest
import pandas as pd
import agents
import model

class test_OrderBook(unittest.TestCase):

    def setUp(self) -> None:
        ethereumData = pd.read_csv('cleanedEuthereumData.csv')
        tetherData = pd.read_csv('cleanedTetherData.csv')
        self.currency1 = agents.Currency("ethereum", "USD/ETH", "crypto", 100, ethereumData)
        self.currency2 = agents.Currency("tether", "USD/USDT", "crypto", 100, tetherData)
        model1 = model.MarketModel()

        self.agent1 = agents.MarketAgent(1, model1, agents.Strategy, model1.currencyMarket)
        self.agent2 = agents.MarketAgent(1, model1, agents.Strategy, model1.currencyMarket)
        self.agent3 = agents.MarketAgent(1, model1, agents.Strategy, model1.currencyMarket)
        return super().setUp()

    def test_order_params(self):
        
        order = agents.Order('OPEN', self.currency1, self.currency2, 10, 2, self.agent, 1000, 1, 1)

        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")


if __name__ == '__main__':
    unittest.main()