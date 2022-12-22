from src.natal.amigo import Amigo
from tests.natal.fakeshuffle import FakeShuffle


def test_amigo_secreto():
    """Testa a função amigo_secreto."""
    amigo_jose = Amigo('José', 'IDDOJOSE')
    amigo_joao = Amigo('João', 'IDDOJOAO')
    amigo_maria = Amigo('Maria', 'IDDAMARIA')
    lista_amigos = [amigo_jose, amigo_joao, amigo_maria]
    amigo_jose.ligar(amigo_joao)
    amigo_joao.ligar(amigo_maria)
    amigo_maria.ligar(amigo_jose)
    assert amigo_jose.amigo_secreto == amigo_joao
    assert amigo_joao.amigo_secreto == amigo_maria
    assert amigo_maria.amigo_secreto == amigo_jose


def test_amigo_secreto_shuffle():
    """Testa a função amigo_secreto."""
    amigo_jose = Amigo('José', 'IDDOJOSE')
    amigo_joao = Amigo('João', 'IDDOJOAO')
    amigo_maria = Amigo('Maria', 'IDDAMARIA')
    lista_amigos = [amigo_jose, amigo_joao, amigo_maria]
    shuffle = FakeShuffle()
    shuffle.shuffle(lista_amigos)
    assert amigo_jose.amigo_secreto == amigo_joao
    assert amigo_joao.amigo_secreto == amigo_maria
    assert amigo_maria.amigo_secreto == amigo_jose
