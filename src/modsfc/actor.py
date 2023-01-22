import abc
from .model import Model

__all__ = ['Actor']

class Actor(metaclass=abc.ABCMeta):
    """Abstract base class for a model component"""
    ## Cribbed from https://realpython.com/python-interface/

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass.register) and
                callable(subclass.register) or
                NotImplemented)

    @abc.abstractmethod
    def register(self, model: Model):
        """Add all model-defined components to the complete model"""
        raise NotImplementedError
