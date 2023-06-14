from models.conjunto_cartas import ConjuntoCartas

class Sequencia(ConjuntoCartas):
    def __init__(self, id, cartas) -> None:
        super().__init__(cartas)
        self.id = id

    def canastra(self):
        return self.n_cartas >= 7

    def adicionar_carta(self, carta):
        self._adicionar_carta()

    def obter_estado(self):
        estado = super().obter_estado()
        estado['id'] = self.id
        return estado
