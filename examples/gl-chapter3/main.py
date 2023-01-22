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

    producer.register(model)
    consumer.register(model)
    government.register(model)

    assert model.validate()

    result = await model.execute(0, 30, monitor_fn=lambda t: (t, consumer.cash, government.debt))
    for r in result:
        print(r)

if __name__ == '__main__':
    aio.run(main())
