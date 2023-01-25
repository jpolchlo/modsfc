from modsfc import Actor, Model

class Producer(Actor):
    def __init__(self, wage=1):
        self.wage_rate = wage

    @Producer.action('produce', ['consumption', 'govt_spending', 'labor'], ['income'])
    def produce(self, consumption, govt_expend, labor_offer):
        Y = consumption + govt_expend
        labor_demand = Y / self.wage_rate
        labor_consumed = min(labor_offer, labor_demand)
        return [labor_consumed * self.wage_rate]
