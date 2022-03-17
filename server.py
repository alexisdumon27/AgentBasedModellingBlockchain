from mesa import model
from mesa.visualization.ModularVisualization import ModularServer, VisualizationElement
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import CanvasGrid, ChartModule, PieChartModule, BarChartModule
from model import MarketModel

"""
Four types of modules:
1. Number of transactions chart
2. Top 10 Wealthiest agents chart
3. Relative Wealth Distribution per strategy
4. Orderbooks <-- most important !!!!
"""

class OrderBookModule(VisualizationElement):
    package_includes = []
    local_includes = ["/Users/alexisdumon/Desktop/PRJ/AgentBasedModellingBlockchain/OrderBookModule.js"]

    def __init__(self, exchange_symbol, height, width):
        self.height = height
        self.width = width
        self.exchange_symbol = "" + exchange_symbol + "" # "ETH/USDT:USDT/ETH"
        new_element = "new OrderBookModule({}, {}, {})"
        new_element = new_element.format(exchange_symbol, height, width)

        self.js_code = "elements.push(new OrderBookModule('ETH/USDT:USDT/ETH', 200, 500)););"
        print (self.js_code)

    def render(self, model):
        order_book_data = model.currency_market.getOrderBook().orders
        data = model.simplifyOrderBook(order_book_data)[self.exchange_symbol]
        # print (data)
        return data
        

orderbook_usdt_eth = OrderBookModule("ETH/USDT:USDT/ETH", 200, 500)
# print (orderbook_usdt_eth)

############# USER PARAMETERS ########
from datetime import date, timedelta

start_date = date(2020, 1, 1) 
end_date = date(2021, 12, 31)    # perhaps date.now()

delta = end_date - start_date   # returns timedelta
list_of_dates = []
for i in range(delta.days + 1):
    list_of_dates.append(str(start_date + timedelta(days=i)))

model_params = {
    "num_agents": UserSettableParameter(
        "slider", "Number of market agents", 50, 3, 100, 1, description= "Choose how many agents to include in model"
    ),
    "ratio_of_random_strategy_to_other": UserSettableParameter(
        "slider", "Ratio of Random Strategy agents", 0.5, 0.1, 1, 0.1, description= "Choose ratio of random strategy agents relative to the total number of agents"
    ),
    "ratio_of_agents_engaged_each_turn": UserSettableParameter(
        "slider", "Ratio of agents active per turn", 0.5, 0.1, 1, 0.1, description= "Choose ratio of agents relative active each turn relative to the total number of agents"
    ),
    "starting_date" : UserSettableParameter('choice', 'My Choice', value='Default choice',
                                          choices=list_of_dates)   
}


###### 1. Number of transactions chart ###########

transaction_chart = ChartModule(
    [
        {"Label": "num_transactions_total", "Color":"#00000"},
        {"Label": "num_transactions_ETH/USDT:USDT/ETH" , "Color":"#00000"},
        {"Label": "num_transactions_ETH/BNB:BNB/ETH" , "Color":"#00000"},
        {"Label": "num_transactions_ETH/BTC:BTC/ETH" , "Color":"#00000"},
        {"Label": "num_transactions_BNB/BTC:BTC/BNB", "Color":"#00000"},
        {"Label": "num_transactions_BNB/USDT:USDT/BNB" , "Color":"#00000"},
        {"Label": "num_transactions_BTC/USDT:USDT/BTC", "Color":"#00000"},
    ]
    , data_collector_name="datacollector") 

###### 2. Top 10 Wealthiest agents chart ############

top_10_wealthiest_chart = BarChartModule(
    [
        {"Label" : "Wealthy 0", "Color" : "#00000 "},
        {"Label" : "Wealthy 1", "Color" : "#00000 "},
        {"Label" : "Wealthy 2", "Color" : "#00000 "},
        {"Label" : "Wealthy 3", "Color" : "#00000 "},
        {"Label" : "Wealthy 4", "Color" : "#00000 "},
        {"Label" : "Wealthy 5", "Color" : "#00000 "},
        {"Label" : "Wealthy 6", "Color" : "#00000 "},
        {"Label" : "Wealthy 7", "Color" : "#00000 "},
        {"Label" : "Wealthy 8", "Color" : "#00000 "},
        {"Label" : "Wealthy 9", "Color" : "#00000 "},
    ]
)


###### 3. Relative Wealth Distribution per strategy ######
wealth_distribution_per_strategy = PieChartModule(
    [
        {"Label": "Random", "Color": "#0000000"},
        {"Label": "Pivot Point", "Color": "green"},
        {"Label": "Moving Average", "Color": "blue"},
        {"Label": "RSI", "Color": "purple"},
        {"Label": "MACD", "Color": "yellow"},
    ]
)


server = ModularServer(MarketModel, [transaction_chart, wealth_distribution_per_strategy, top_10_wealthiest_chart], "Crypto Market" , model_params)

# https://mesa.readthedocs.io/_/downloads/en/doc_builds/pdf/

# necessary for analysis
# get orderbook with the different currency pairs
# number of transaction for each currency pair
# top 10 wealthiest agents and their strategies
# top 10 wealthiest per strategy
# ranking of most exchanged currency pairs <- stablecoin???