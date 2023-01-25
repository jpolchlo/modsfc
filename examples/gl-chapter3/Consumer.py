from modsfc import Actor, Model

class Consumer(Actor):
    def __init__(self, α1=0.6, α2=0.4):
        self.cash = 0
        self.last_income = 0
        self.α1 = α1
        self.α2 = α2

    @Consumer.action('supply_labor', [], ['labor'])
    def supply_labor(self):
        return [float("Inf")]

    @Consumer.action('receive_income', ['income'], [])
    def receive_income(self, income):
        self.cash += income
        self.last_income = income
        return []

    @Consumer.action('make_payments', ['tax_rate'], ['tax', 'consumption'])
    def make_payments(self, θ):
        income = self.last_income
        self.cash -= income
        assert self.cash >= 0
        tax_payment = θ * income
        YD = income - tax_payment
        consumption = self.α1 * YD + self.α2 * self.cash
        self.cash += YD - consumption
        return tax_payment, consumption
