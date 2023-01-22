import asyncio as aio

__all__ = [ 'Channel' ]

class Channel:
    def __init__(self, name):
        self.name = name
        self.q = aio.Queue()
        self.log = []

    @property
    def queue(self):
        return self.q

    async def push(self, value):
        self.log.append(value)
        await self.q.put(value)

    async def pop(self, auto_clear=False):
        result = await self.q.get()
        if auto_clear:
            self.q.task_done()
        return result

    async def clear(self):
        self.q.task_done()
