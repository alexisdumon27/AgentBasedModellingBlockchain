from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import CanvasGrid, ChartModule

from model import MarketModel

chart = ChartModule([{"Label": "num_of_transactions", "Color":"#00000"}], data_collector_name="datacollector") 

model_params = {
    "num_agents": UserSettableParameter(
        "slider", "Number of market agents", 10, 3, 27,
    )
}

server = ModularServer(MarketModel, [chart])