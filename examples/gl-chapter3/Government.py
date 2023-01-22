from modsfc import Actor, Model

class Government(Actor):
    def __init__(self, tax_rate=0.2, expenditures=20):
        self.expenditures = expenditures
        self.tax_rate = tax_rate
        self.debt = 0

    def declare_tax_rate(self):
        return [self.tax_rate]

    def spend(self):
        self.debt += self.expenditures
        return [self.expenditures]

    def receive_taxes(self, tax_payment):
        self.debt -= tax_payment
        return []

    def register(self, model: Model):
        model.register_task('declare_tax_rate', self.declare_tax_rate, [], ['tax_rate'])
        model.register_task('spend', self.spend, [], ['govt_spending'])
        model.register_task('receive_taxes', self.receive_taxes, ['tax'], [])
