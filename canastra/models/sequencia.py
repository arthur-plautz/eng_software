from models.conjunto_cartas import ConjuntoCartas

class Sequencia(ConjuntoCartas):
    def __init__(self, id=None, cartas=[]) -> None:
        super().__init__(cartas)
        self.id = id

    def canastra(self):
        return self.n_cartas >= 7

    def suja(self):
        return "Joker" in [carta.valor for carta in self.cartas]

    def remover_carta(self, valor, naipe=None):
        for carta in self.cartas:
            if naipe and carta.naipe == naipe and carta.valor == valor:
                self.cartas.remove(carta)
                return carta

    def adicionar_carta(self, carta):
        self._adicionar_carta(carta)
    
    def remover_coringa(self):
        for carta in self.cartas:
            if carta.valor == "Joker":
                return self.cartas.remove(carta)

    def obter_estado(self):
        estado = super().obter_estado()
        estado['id'] = self.id
        return estado
