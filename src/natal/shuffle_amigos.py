from src.natal.ports.shuffle import Shuffle
from random import shuffle


class ShuffleAmigos(Shuffle):

    def shuffle(self, amigos):
        shuffle(amigos)
        for i in range(len(amigos)):
            amigos[i].amigo_secreto = amigos[0] if i == len(
                amigos) - 1 else amigos[i + 1]
