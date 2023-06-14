from models.conjunto_cartas import ConjuntoCartas

class Mao(ConjuntoCartas):
    def __init__(self, cartas=[]):
        super().__init__(cartas)

    def remover_carta(self):
        return self._remover_carta()

    def adicionar_carta(self, carta):
        self._adicionar_carta(carta)
