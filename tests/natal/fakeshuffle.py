from src.natal.ports.shuffle import Shuffle


class FakeShuffle(Shuffle):

    def shuffle(self, amigos):
        for i in range(len(amigos)):
            amigos[i].amigo_secreto = amigos[0] if i == len(
                amigos) - 1 else amigos[i + 1]
