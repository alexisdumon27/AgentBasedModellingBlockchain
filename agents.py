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


class MarketAgent(ModelAgent):

    def __init__(self, unique_id, model, currencyMarket):
        super().__init__(unique_id, model, currencyMarket)
        
        self.currentModel = model
        
        self.currentObjective = None
        self.setCurrentObjective()
        
        """ set everyone off with a fixed amount in their wallets """
        self.wallet = self.createWallet()

        self.amountOfGoods = random.randint(-1, 2)
    

    def createWallet(self):
        wallet = {}
        for currency in self.currencyMarket.getAvailableCurrencies():
            wallet[currency.getName()] = 2.7 # for now fixed amount of both currencies!!!

        return wallet

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
        """ for now it chooses a random agent and currency, and goes ahead with the transaction all
        buyers and all sellers do it """
        self.setCurrentObjective()
        other = random.choice(self.model.schedule.agents) # choose a random agent
        currency = random.choice(self.currencyMarket.getAvailableCurrencies()).name # choose a random currency
        # print (currency)
        if self.currentObjective == "BUY":
            self.wallet[currency] -= 1
            self.amountOfGoods -= 1

            other.wallet[currency] += 1
            other.amountOfGoods += 1
        else:
            self.wallet[currency] += 1
            self.amountOfGoods += 1

            other.wallet[currency] -= 1
            other.amountOfGoods -= 1
        
        print (currency)
        if currency == "ethereum":
            self.model.addEthereumTransaction()
        elif currency == "tether":
            self.model.addTetherTransaction()
        
        self.model.addTransaction()

        


