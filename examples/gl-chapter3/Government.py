from modsfc import Actor, Model

class Government(Actor):
    def __init__(self, tax_rate=0.2, expenditures=20):
        self.expenditures = expenditures
        self.tax_rate = tax_rate
        self.debt = 0

    @Government.action('declare_tax_rate', [], ['tax_rate'])
    def declare_tax_rate(self):
        return [self.tax_rate]

    @Government.action('spend', [], ['govt_spending'])
    def spend(self):
        self.debt += self.expenditures
        return [self.expenditures]

    @Government.action('receive_taxes', ['tax'], [])
    def receive_taxes(self, tax_payment):
        self.debt -= tax_payment
        return []
