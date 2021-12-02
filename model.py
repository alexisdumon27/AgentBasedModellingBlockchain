from mesa import Agent, Model
from mesa.time import RandomActivation

class MarketModel(Model):
    def __init__(self, num_agents, currency):
        self.num_agents = num_agents
        self.schedule = RandomActivation(self)
        self.currency = currency # will become a list of available currencies to be used in the market
        for i in range(self.num_agents):
            a = MarketAgent(i, self)
            self.schedule.add(a)
            print ("wallet: ", a.wallet, " goods: ", a.amountOfGoodToSell )

    def step(self):
        self.schedule.step()
        for i in range(self.num_agents):
            agent = self.schedule.agents[i]
            print ("id", agent.unique_id, ", wallet: ", agent.wallet, ", goods: ", agent.amountOfGoodToSell)
        print ("-------- A step has happened -------------")

class MarketAgent(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wallet = {'fiat_currency': 10} # wallet = {fiat_currency : 0, fiat_backed : 0, crypto_backed : 0 ... }
        self.amountOfGoodToSell = 1

    # what happens during one round of the simulation
    def step(self):
        if self.wallet['fiat_currency'] == 0:
            return
        
        other_agent = self.random.choice(self.model.schedule.agents)
        # print ('agents id', other_agent.unique_id, "agents amount to sell: ", other_agent.amountOfGoodToSell)
        if other_agent.amountOfGoodToSell > 0:
            self.wallet['fiat_currency'] -= 1
            other_agent.wallet['fiat_currency'] += 1
            self.amountOfGoodToSell += 1
            other_agent.amountOfGoodToSell -= 1

        # print ("goods: ", self.amountOfGoodToSell, "; ", self.wallet)

# a currency has a value
# a stabilising mechanism
# a supply
# should it represent the entire currency or individual coins of the currency?
class fiat_currency:
    def __init__(self, name : str, supply: int, value: int):
        self.name = name
        self.supply = supply
        self.value = value

currency = fiat_currency('fiat_currency', 10, 1)
empty_model = MarketModel(10, currency)
for i in range(10):
    empty_model.step()

