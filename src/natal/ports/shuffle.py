from abc import ABCMeta, abstractmethod
from typing import List
from src.natal.amigo import Amigo


class Shuffle(metaclass=ABCMeta):

    @abstractmethod
    def shuffle(self, amigos: List[Amigo]):
        pass
