import asyncio as aio
from modsfc import Model

from Producer import Producer
from Consumer import Consumer
from Government import Government

async def main():
    model = Model()
    producer = Producer()
    consumer = Consumer()
    government = Government()

    model.add(consumer)
    model.add(producer)
    model.add(government)

    assert model.validate()

    result = await model.execute(0, 40, monitor_fn=lambda t: (t, consumer.cash, government.debt))
    taxes = model.get_channel_log('tax')
    consumption = model.get_channel_log('consumption')
    income = model.get_channel_log('income')

    print("Time | Debt/Wealth | Taxes       | Consumption | Income      ")
    print("-----+-------------+-------------+-------------+-------------")
    for ((t, cash, debt), tax), (cons, inc) in zip(zip(result, taxes), zip(consumption, income)):
        assert abs(cash - debt) < 1e-8
        print(f"{t:<5}| {cash:<11,.2f} | {tax:<11,.2f} | {cons:<11,.2f} | {inc:<11,.2f}")

if __name__ == '__main__':
    aio.run(main())
