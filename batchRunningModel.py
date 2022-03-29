from model import MarketModel
import pandas as pd
from dataVisualisationMethods import *
from mesa.batchrunner import BatchRunner
import time 
model = MarketModel(starting_date=1, ratio_of_random_strategy_to_other=0.5, ratio_of_agents_engaged_each_turn=0.5, num_agents=150)

# number of steps in first two months 1433
end_step = 314
# end_step = 10
start = time.time()
for i in range(end_step):
    start_0 = time.time()
    print ("step: ", i)
    model.step()
    end_0 = time.time()
    print(end_0 - start_0)

end = time.time()
print(end - start)

print(model.currency_market.open_order_by_currency_pair.items())
print(model.currency_market.close_order_by_currency_pair.items())
model_df = model.datacollector.get_model_vars_dataframe()
model_df.to_csv("smallModelResults.csv")
print (model_df)

