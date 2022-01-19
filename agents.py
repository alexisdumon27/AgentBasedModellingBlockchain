from mesa import Agent
import random
# from model import MarketModel

# agents should have current states - depending on their states they should decide to do a particular action
class ModelAgent(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wallet = 1
        self.currentObjective = None

    def getWallet(self):
        return self.wallet
    
    def step(self):
        return 27
    
    def init_current_objective():
        return None


class MarketAgent(ModelAgent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        
        self.currentModel = model
        
        self.currentObjective = None
        self.setCurrentObjective()
        
        """ set everyone off with a random amount in their wallets """
        self.wallet = random.randint(1, 27)

        self.amountOfGoods = random.randint(-1, 2)


    def setCurrentObjective(self):
        """ every round market agents are randomly assigned a new current object BUY or SELL """
        self.currentObjective = random.choice(['BUY', 'SELL'])
        # print (self.currentObjective)

    def tryToAchieveObjective(self):
        """ depending on current objective agent will want to buy a good or sell a good """
        # # find someone with opposite objective
        # if self.wallet > 0:
        #     potential_seller

        return None

    # what happens during one round of the simulation for one agent
    def step(self):
        self.setCurrentObjective()

        # self.tryToAchieveObjective()


# marketAgent = MarketAgent(1, MarketModel)
# print (marketAgent.currentObjective)
# marketAgent = MarketAgent(1, MarketModel)
# print (marketAgent.currentObjective)


        # sellers = [x for x in self.model.schedule.agents if x.type == "seller"] # should an agent be aware of all other agents? 
        # buyers = [x for x in self.model.schedule.agents if x.type == "buyer"]

        # if self.type == 'buyer': # tries to buy a good if it has enough money and it an find a seller
        #     if self.wallet['fiat_currency'] == 0:
        #         return
        #     else:
        #         other_agent = self.random.choice(sellers)
        #         if other_agent.type == 'seller' and other_agent.amountOfGoodToSell > 0:
        #             self.wallet['fiat_currency'] -= 1
        #             other_agent.wallet['fiat_currency'] += 1
        #             self.amountOfGoodToSell += 1
        #             other_agent.amountOfGoodToSell -= 1
        # else: # seller, tries to get more supply of the good so it can sell more and make more money
        #     new_supplies = randint(0, 4)
        #     self.amountOfGoodToSell += new_supplies


