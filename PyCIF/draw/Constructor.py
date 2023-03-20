from abc import ABC, abstractmethod

from PyCIF.helpers.Dotdict import Dotdict
from PyCIF.draw.Optspec import Optspec

class Constructor(ABC):
    optspecs = Dotdict()

    @abstractmethod
    def make(self):
        pass

