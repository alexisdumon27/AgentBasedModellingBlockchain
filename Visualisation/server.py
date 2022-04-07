from mesa.visualization.ModularVisualization import ModularServer, VisualizationElement
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import ChartModule, PieChartModule, BarChartModule
from numpy import char
from Model.model import MarketModel

"""
Four types of modules:
1. Number of transactions chart
2. Top 10 Wealthiest agents chart
3. Relative Wealth Distribution per strategy
4. Orderbooks <-- most important !!!!
"""

# DISPLAY current day on the simulation through currentDayModule just TEXT

# https://mesa.readthedocs.io/_/downloads/en/doc_builds/pdf/
class OrderBookModule(VisualizationElement):
    package_includes = []
    local_includes = ["OrderBookModule.js"]

    def __init__(self, exchange_symbol, height, width):
        self.height = height
        self.width = width
        self.exchange_symbol = exchange_symbol
        self.js_code = "elements.push(new OrderBookModule('" + exchange_symbol + "', 200, 500));"

    def render(self, model):
        order_book_data = model.currency_market.getOrderBook().orders
        return model.simplifyOrderBook(order_book_data)[self.exchange_symbol]

chart_array = []

##### 1. ORDERBOOKS ############

orderbook_usdt_eth = OrderBookModule("ETH/USDT:USDT/ETH", 200, 500)
orderbook_usdt_btc = OrderBookModule("BTC/USDT:USDT/BTC", 200, 500)
orderbook_usdt_bnb = OrderBookModule("BNB/USDT:USDT/BNB", 200, 500)
orderbook_bnb_eth = OrderBookModule("ETH/BNB:BNB/ETH", 200, 500)
orderbook_btc_eth = OrderBookModule("ETH/BTC:BTC/ETH", 200, 500)
orderbook_btc_bnb = OrderBookModule("BNB/BTC:BTC/BNB", 200, 500)

chart_array.append(orderbook_btc_bnb)
chart_array.append(orderbook_bnb_eth)
chart_array.append(orderbook_btc_eth)
chart_array.append(orderbook_usdt_bnb)
chart_array.append(orderbook_usdt_btc)
chart_array.append(orderbook_usdt_eth)

###### 2. Number of transactions chart ###########
transaction_chart = ChartModule(
    [
        {"Label": "num_transactions_total", "Color":"#00000"},
        {"Label": "num_transactions_ETH/USDT:USDT/ETH" , "Color":"#8fa6c9"},
        {"Label": "num_transactions_ETH/BNB:BNB/ETH" , "Color":"#ad8fc9"},
        {"Label": "num_transactions_ETH/BTC:BTC/ETH" , "Color":"#b6e0bb"},
        {"Label": "num_transactions_BNB/BTC:BTC/BNB", "Color":"#d9e0b6"},
        {"Label": "num_transactions_BNB/USDT:USDT/BNB" , "Color":"#e0c7b6"},
        {"Label": "num_transactions_BTC/USDT:USDT/BTC", "Color":"##e0b6cf"},
    ]
    , data_collector_name="datacollector") 

chart_array.append(transaction_chart)

###### 3. Top 10 Wealthiest agents chart ############
top_10_wealthiest_chart = BarChartModule(
    [
        {"Label" : "Wealthy 0", "Color" : "#02cf05 "},
        {"Label" : "Wealthy 1", "Color" : "#19bd1b "},
        {"Label" : "Wealthy 2", "Color" : "#3dbf3f "},
        {"Label" : "Wealthy 3", "Color" : "#5cbf5d "},
        {"Label" : "Wealthy 4", "Color" : "#79c77a "},
        {"Label" : "Wealthy 5", "Color" : "#87c788 "},
        {"Label" : "Wealthy 6", "Color" : "#9dc79e "},
        {"Label" : "Wealthy 7", "Color" : "#b5c7b5 "},
        {"Label" : "Wealthy 8", "Color" : "#c6cfc6 "},
        {"Label" : "Wealthy 9", "Color" : "#bdbdbd "},
    ]
)

chart_array.append(top_10_wealthiest_chart)

###### 4. Relative Wealth Distribution per strategy ######
wealth_distribution_per_strategy = PieChartModule(
    [
        {"Label": "Pivot Point", "Color": "#bab3b3"},
        {"Label": "Moving Average", "Color": "#afd197"},
        {"Label": "RSI", "Color": "#72cfc7"},
        {"Label": "MACD", "Color": "#c2a4db"},
    ]
)
chart_array.append(wealth_distribution_per_strategy)

#### 5. Who are the agents who have something in the orderbook ? ####

orderbook_agents_per_strategy = BarChartModule(
    [
        {"Label": "Random orderbook", "Color": "#0000000"},
        {"Label": "Pivot Point orderbook", "Color": "bab3b3"},
        {"Label": "Moving Average orderbook", "Color": "afd197"},
        {"Label": "RSI orderbook", "Color": "72cfc7"},
        {"Label": "MACD orderbook", "Color": "c2a4db"},
    ]
)
chart_array.append(orderbook_agents_per_strategy)

#### 6. number of transactions per strategy per currency pair (have diagram like bar chart)

# 6.1
pivot_point_transactions_chart = BarChartModule(
    [
        {"Label": "num_transactions_pivot_point_ETH/USDT:USDT/ETH" , "Color":"#00000"},
        {"Label": "num_transactions_pivot_point_ETH/BNB:BNB/ETH" , "Color":"#00000"},
        {"Label": "num_transactions_pivot_point_ETH/BTC:BTC/ETH" , "Color":"#00000"},
        {"Label": "num_transactions_pivot_point_BNB/BTC:BTC/BNB", "Color":"#00000"},
        {"Label": "num_transactions_pivot_point_BNB/USDT:USDT/BNB" , "Color":"#00000"},
        {"Label": "num_transactions_pivot_point_BTC/USDT:USDT/BTC", "Color":"#00000"},
    ]
)

# 6.2
moving_average_transactions_chart = BarChartModule(
    [
        {"Label": "num_transactions_moving_average_ETH/USDT:USDT/ETH" , "Color":"#00000"},
        {"Label": "num_transactions_moving_average_ETH/BNB:BNB/ETH" , "Color":"#00000"},
        {"Label": "num_transactions_moving_average_ETH/BTC:BTC/ETH" , "Color":"#00000"},
        {"Label": "num_transactions_moving_average_BNB/BTC:BTC/BNB", "Color":"#00000"},
        {"Label": "num_transactions_moving_average_BNB/USDT:USDT/BNB" , "Color":"#00000"},
        {"Label": "num_transactions_moving_average_BTC/USDT:USDT/BTC", "Color":"#00000"},
    ]
)

# 6.3
rsi_transactions_chart = BarChartModule(
    [
        {"Label": "num_transactions_rsi_ETH/USDT:USDT/ETH" , "Color":"#00000"},
        {"Label": "num_transactions_rsi_ETH/BNB:BNB/ETH" , "Color":"#00000"},
        {"Label": "num_transactions_rsi_ETH/BTC:BTC/ETH" , "Color":"#00000"},
        {"Label": "num_transactions_rsi_BNB/BTC:BTC/BNB", "Color":"#00000"},
        {"Label": "num_transactions_rsi_BNB/USDT:USDT/BNB" , "Color":"#00000"},
        {"Label": "num_transactions_rsi_BTC/USDT:USDT/BTC", "Color":"#00000"},
    ]
)

# 6.4
macd_transactions_chart = BarChartModule(
    [
        {"Label": "num_transactions_macd_ETH/USDT:USDT/ETH" , "Color":"#00000"},
        {"Label": "num_transactions_macd_ETH/BNB:BNB/ETH" , "Color":"#00000"},
        {"Label": "num_transactions_macd_ETH/BTC:BTC/ETH" , "Color":"#00000"},
        {"Label": "num_transactions_macd_BNB/BTC:BTC/BNB", "Color":"#00000"},
        {"Label": "num_transactions_macd_BNB/USDT:USDT/BNB" , "Color":"#00000"},
        {"Label": "num_transactions_macd_BTC/USDT:USDT/BTC", "Color":"#00000"},
    ]
)

chart_array.append(pivot_point_transactions_chart)
chart_array.append(moving_average_transactions_chart)
chart_array.append(rsi_transactions_chart)
chart_array.append(macd_transactions_chart)

#### 7. record dates of when transactions took place for each currency pair for each strategy


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
        "slider", "Number of market agents", 127, 67, 400, 10, description= "Choose how many agents to include in model"
    ),
    "ratio_of_random_strategy_to_other": UserSettableParameter(
        "slider", "Ratio of Random Strategy agents", 0.85, 0.1, 1, 0.1, description= "Choose ratio of random strategy agents relative to the total number of agents"
    ),
    "ratio_of_agents_engaged_each_turn": UserSettableParameter(
        "slider", "Ratio of agents active per turn", 1, 0.1, 1, 0.1, description= "Choose ratio of agents relative active each turn relative to the total number of agents"
    ),
    "starting_date" : UserSettableParameter('choice', 'My Choice', value= 33,
                                          choices=list_of_dates)   
}

server = ModularServer(MarketModel, chart_array, "Crypto Market" , model_params)