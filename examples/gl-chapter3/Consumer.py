from modsfc import Actor, Model

class Consumer(Actor):
    def __init__(self, α1=0.6, α2=0.4, endowment=0):
        self.cash = endowment
        self.last_income = 0
        self.α1 = α1
        self.α2 = α2

    def supply_labor(self):
        return [float("Inf")]

    def receive_income(self, income):
        self.cash += income
        self.last_income = income
        return []

    def make_payments(self, θ):
        income = self.last_income
        self.cash -= income
        tax_payment = θ * income
        YD = income - tax_payment
        consumption = self.α1 * YD + self.α2 * self.cash
        self.cash += YD - consumption
        return tax_payment, consumption

    def register(self, model: Model):
        model.register_task('supply_labor', self.supply_labor, [], ['labor'])
        model.register_task('receive_income', self.receive_income, ['income'], [])
        model.register_task('make_payments', self.make_payments, ['tax_rate'], ['tax', 'consumption'])
