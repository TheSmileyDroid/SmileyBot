from typing import Union


class Amigo:
    """Classe que representa um amigo."""

    def __init__(self, nome: str, id: str):
        """Inicializa um amigo."""
        self.nome = nome
        self.id = id
        self.amigo_secreto: Union['Amigo', None] = None

    def __str__(self) -> str:
        """Retorna uma string representando o amigo."""
        return self.nome

    def __repr__(self) -> str:
        """Retorna uma string representando o amigo."""
        return self.nome

    def ligar(self, amigo: 'Amigo'):
        """Liga o amigo a outro amigo."""
        self.amigo_secreto = amigo