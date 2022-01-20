from mesa import model
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import CanvasGrid, ChartModule

from model import MarketModel

chart = ChartModule(
    [{"Label": "num_of_transactions", "Color":"#00000"},
    {"Label": "num_of_tether_transactions", "Color":"#99ffcc"},
    {"Label": "num_of_ethereum_transactions", "Color":"#6600cc"}
    ]
    
    , data_collector_name="datacollector") 

model_params = {
    "num_agents": UserSettableParameter(
        "slider", "Number of market agents", 10, 3, 100, 1, description= "Choose how many agents to include in model"
    )
}

server = ModularServer(MarketModel, [chart], "Crypto Market" , model_params)