from mesa import Agent
import random
# from model import MarketModel

# agents should have current states - depending on their states they should decide to do a particular action
class ModelAgent(Agent):

    def __init__(self, unique_id, model, currencyMarket):
        super().__init__(unique_id, model)
        self.currencyMarket = currencyMarket
        self.currentObjective = None

    def getWallet(self):
        return self.wallet
    
    def step(self):
        return 27
    
    def createWallet(self):
        return {"euthereum": 1, "tether": 1}


class MarketAgent(ModelAgent):

    def __init__(self, unique_id, model, currencyMarket):
        super().__init__(unique_id, model, currencyMarket)
        
        self.currentModel = model
        
        self.currentObjective = None
        self.setCurrentObjective()
        
        """ set everyone off with a fixed amount in their wallets """
        self.wallet = self.createWallet()

        self.amountOfGoods = random.randint(-1, 2)
    
    def setCurrentObjective(self):
        """ every round market agents are randomly assigned a new current object BUY or SELL """
        self.currentObjective = random.choice(['BUY', 'SELL'])
        # print (self.currentObjective)

    def bestCurrencyForObjective(self):
        """ depending on current objective agent will want to buy a good or sell a good """
        # get data for the different currencies INSTEAD OF HAVING each agent calculate make CURRENCYmARKET calculate 
        # have agents QUERY for the processed data

        return None

    # what happens during one round of the simulation for one agent
    def step(self):
        self.setCurrentObjective()

