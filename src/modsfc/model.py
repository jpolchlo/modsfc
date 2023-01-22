import asyncio as aio
from dataclasses import dataclass
import logging
import networkx as nx

from .channel import Channel

__all__ = [ 'Model' ]

class Node:
    pass

@dataclass(frozen=True)
class ChannelNode(Node):
    name: str

@dataclass(frozen=True)
class TaskNode(Node):
    name: str

class Model:
    def __init__(self):
        self.channels = {}
        self.units = []
        self.n_nodes = 0
        self.graph = nx.DiGraph()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.tick = None
        self.sync = None
        self.valid = False


    def register_task(self, task_name, fn, inputs, outputs):
        task_node = TaskNode(task_name)
        self.valid = False
        self.n_nodes += 1
        self.units.append( (fn, inputs, outputs) )
        self.graph.add_node( task_node )

        for name in inputs:
            chan_node = ChannelNode(name)
            if name not in self.channels.keys():
                self.channels[name] = Channel(name)
                self.graph.add_node(chan_node)

            self.graph.add_edge(chan_node, task_node)

        for name in outputs:
            chan_node = ChannelNode(name)
            if name not in self.channels.keys():
                self.channels[name] = Channel(name)
                self.graph.add_node(chan_node)

            self.graph.add_edge(task_node, chan_node)


    def validate(self):
        g = self.graph
        tasks = list(filter(lambda n: isinstance(n, TaskNode), g.nodes))
        channels = list(filter(lambda n: isinstance(n, ChannelNode), g.nodes))

        try:
            cyc = nx.cycles.find_cycle(g)
        except nx.NetworkXNoCycle:
            pass
        else:
            self.logger.error(f"Found dependency cycle: {cyc}")
            self.valid = False
            return False

        failed = False
        for c in channels:
            cn = ChannelNode(c.name)
            indeg = g.in_degree(cn)
            outdeg = g.out_degree(cn)
            if indeg == 0:
                self.logger.error(f"Channel {c.name} is not being filled")
                failed = True
            if indeg > 1:
                parents = list(g.pred[cn])
                self.logger.error(f"Channel {c.name} has multiple writers: {parents}")
                failed = True
            if outdeg == 0:
                self.logger.error(f"Channel {c.name} is not being consumed")
                failed = True
            if outdeg > 1:
                children = list(g.succ[cn])
                self.logger.error(f"Channel {c.name} has multiple readers: {children}")
                failed = True

        self.valid = not failed
        return not failed


    async def __execute_task(self, fn, inputs, outputs):
        while True:
            await self.tick.wait()
            values = []
            for chan in inputs:
                self.logger.debug(f"Waiting for input on channel {chan}")
                value = await self.channels[chan].pop(True)
                self.logger.debug(f"Receive value {value} on channel {chan}")
                values.append(value)
            results = fn(*values)
            for (result, chan) in zip(results, outputs):
                self.logger.info(f"Placing output {result} on channel {chan}")
                await self.channels[chan].push(result)
            self.logger.debug(f"Pausing ({self.sync.n_waiting})")
            await self.sync.wait()
            await aio.sleep(0)


    async def execute(self, t_init, t_end, dt=1, monitor_fn=None):
        self.tick = aio.Event()
        self.sync = aio.Barrier(self.n_nodes + 1)

        jobs = [self.__execute_task(*args) for args in self.units]

        results = []
        t = t_init
        async with aio.TaskGroup() as tg:
            tasks = [tg.create_task(job) for job in jobs]

            while t < t_end:
                self.tick.set()
                await self.sync.wait()
                self.tick.clear()
                results.append( monitor_fn(t) )

                t += dt

            for task in tasks:
                task.cancel()

        self.tick = None
        self.sync = None

        return results


    def get_channel_log(self, channel_name):
        return self.channels[channel_name].log
