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
        
        self.model = model
        self.currentObjective = None
        self.setCurrentObjective()
        
        """ set everyone off with a fixed amount in their wallets """
        self.wallet = self.createWallet()

        self.amountOfGoods = random.randint(0, 2)
    

    def createWallet(self):
        wallet = {}
        for currency in self.currencyMarket.getAvailableCurrencies():
            wallet[currency.getName()] = 2.7 # for now fixed amount of both currencies!!!

        return wallet

    def setCurrentObjective(self):
        """ every round market agents are randomly assigned a new current object BUY or SELL """
        self.currentObjective = random.choice(['BUY', 'SELL'])
        # print (self.currentObjective)

    def chooseCurrencyForTransaction(self):
        """ depending on current objective agent will want to buy a good or sell a good """
        # get data for the different currencies INSTEAD OF HAVING each agent calculate make CURRENCYmARKET calculate 
        # have agents QUERY for the processed data

        # ASSUME best currency for BUYER is best for SELLER
        return None

    def hasEnoughOfCurrency(self, currency):
        return self.wallet[currency.getName()] > 1


    # what happens during one round of the simulation for one agent
    def step(self):
        """ for now it chooses a random agent and least fluctuating currency, and goes ahead with the transaction only
        buyers """

        if self.currentObjective == "BUY" and len(self.model.sellers) > 0: # if agent's objective is to BUY and there are available SELLERS
            other = self.model.sellers[0] # choose a random seller agent
            self.model.sellers = self.model.sellers[1:] # remove it from the list of available
            
            currency = self.currencyMarket.getLeastFluctuatingCurrency() # chooses least fluctuating currency
            
            chosenCurrency = self.currencyMarket.getProbabilisticCurrencyChoice(currency)
            if self.hasEnoughOfCurrency(chosenCurrency) and other.amountOfGoods >= 1: # if agent has enough of the currency and other has enough goods
                # do the exchange using the chosen currency
                currencyName = chosenCurrency.getName()
                self.wallet[currencyName] -= 1
                self.amountOfGoods -= 1

                other.wallet[currencyName] += 1
                other.amountOfGoods += 1
                
                chosenCurrency.addTransaction()

        # after finished step find new objective // could put this in model's step method... 
        self.setCurrentObjective()

        


