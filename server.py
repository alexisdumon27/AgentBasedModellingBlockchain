from mesa import model
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import CanvasGrid, ChartModule

from model import MarketModel

transactionChart = ChartModule(
    [{"Label": "num_of_transactions", "Color":"#00000"},
    {"Label": "num_of_tether_transactions", "Color":"#99ffcc"},
    {"Label": "num_of_ethereum_transactions", "Color":"#6600cc"}
    ]
    , data_collector_name="datacollector") 


bnb_usd = ChartModule(
    [
        {"Label": "BNB/USD", "Color": "#00000"},
    ]
)

# not necessary for analysis
bnb_usdt = ChartModule([ {"Label": "BNB/USDT", "Color": "#00000"},])
bnb_eth = ChartModule([{"Label": "BNB/ETH", "Color": "#00000"},])
bnb_btc = ChartModule([{"Label": "BNB/BTC", "Color": "#00000"},])
desired_exchange_rate_chart = ChartModule([ {"Label": "desired_exchange", "Color": "#00000"},])

chart_modules = []
chart_modules.append(desired_exchange_rate_chart) # does not work
chart_modules.append(bnb_usd)
chart_modules.append(bnb_usdt)
chart_modules.append(bnb_eth)
chart_modules.append(bnb_btc)

# necessary for analysis
# get orderbook with the different currency pairs
# number of transaction for each currency pair
# top 10 wealthiest agents and their strategies
# top 10 wealthiest per strategy
# ranking of most exchanged currency pairs <- stablecoin???
# 


model_params = {
    "num_agents": UserSettableParameter(
        "slider", "Number of market agents", 10, 3, 1000, 1, description= "Choose how many agents to include in model"
    ),
    "currency_0" : UserSettableParameter(
        'choice', 'Currency 0', value='BNB', choices=['BTC', 'ETH', 'BNB']), # will come as a list with all possible pairs
    "currency_1" : UserSettableParameter(
        'choice', 'Currency 1', value='USDT', choices=['BTC', 'ETH', 'BNB']) # will come as a list with all possible pairs
}


server = ModularServer(MarketModel, chart_modules, "Crypto Market" , model_params)