from models.conjunto_cartas import ConjuntoCartas

class Mao(ConjuntoCartas):
    def __init__(self, cartas=[]):
        super().__init__(cartas)

    def remover_carta(self, valor=None, naipe=None):
        if valor:
            for carta in self.cartas:
                if naipe and carta.naipe == naipe and carta.valor == valor:
                    self.cartas.remove(carta)
                    return carta
        else:
            return self.cartas.pop()

    def adicionar_carta(self, carta):
        self._adicionar_carta(carta)
