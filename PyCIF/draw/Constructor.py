from abc import ABC, abstractmethod

from PyCIF.helpers.Dotdict import Dict
from PyCIF.draw.Optspec import Optspec

class Constructor(ABC):
    optspecs = Dict()

    @abstractmethod
    def make(self):
        pass

