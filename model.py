from mesa import Agent, Model
from mesa.time import RandomActivation
from random import randint

class MarketModel(Model):
    def __init__(self, num_agents, currency):
        self.num_agents = num_agents
        self.schedule = RandomActivation(self)
        self.currency = currency # will become a list of available currencies to be used in the market
        for i in range(self.num_agents):
            agents_type = 'buyer' # will have to be done better
            if i % 4 == 0:
                agents_type = 'seller'
            a = MarketAgent(i, self, agents_type)
            self.schedule.add(a)
            print ("wallet: ", a.wallet, " goods: ", a.amountOfGoodToSell, " type: ", a.type)

    def step(self):
        self.schedule.step()

        for i in range(self.num_agents):
            agent = self.schedule.agents[i]
            print ("id", agent.unique_id, ", wallet: ", agent.wallet, ", goods: ", agent.amountOfGoodToSell, " type: ", agent.type)
        print ("-------- A step has happened -------------")


# agents should have current states - depending on their states they should decide to do a particular action
class MarketAgent(Agent):

    def __init__(self, unique_id, model, agent_type):
        super().__init__(unique_id, model)
        self.type = agent_type
        self.wallet = {'fiat_currency' : 0}
        self.amountOfGoodToSell = 3
        if self.type == 'buyer':
            self.wallet = {'fiat_currency': 10} # wallet = {fiat_currency : 0, fiat_backed : 0, crypto_backed : 0 ... }
            self.amountOfGoodToSell = 0

    # what happens during one round of the simulation for one agent
    def step(self):
        
        sellers = [x for x in self.model.schedule.agents if x.type == "seller"] # should an agent be aware of all other agents? 
        buyers = [x for x in self.model.schedule.agents if x.type == "buyer"]

        if self.type == 'buyer': # tries to buy a good if it has enough money and it an find a seller
            if self.wallet['fiat_currency'] == 0:
                return
            else:
                other_agent = self.random.choice(sellers)
                if other_agent.type == 'seller' and other_agent.amountOfGoodToSell > 0:
                    self.wallet['fiat_currency'] -= 1
                    other_agent.wallet['fiat_currency'] += 1
                    self.amountOfGoodToSell += 1
                    other_agent.amountOfGoodToSell -= 1
        else: # seller, tries to get more supply of the good so it can sell more and make more money
            new_supplies = randint(0, 4)
            self.amountOfGoodToSell += new_supplies


    # depending on certain factors the agent should decide on an action to do
    # hold the currency, exchange the currency, sell the currency, buy good/service, 
    #### factors could include: the price of currencies, if they need to buy a good/service, IOW what they want to maximise
 
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

