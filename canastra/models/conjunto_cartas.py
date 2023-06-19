from models.carta import Carta

class ConjuntoCartas:
    def __init__(self, cartas=[]):
        self.cartas = cartas

    def _adicionar_carta(self, carta):
        self.cartas.append(carta)

    def _remover_carta(self, carta=None):
        if carta:
            return self.cartas.remove(carta)
        else:
            return self.cartas.pop()

    @property
    def n_cartas(self):
        return len(self.cartas)

    def vazio(self):
        return self.n_cartas == 0

    def obter_estado(self):
        return dict(
            cartas=[carta.serializacao for carta in self.cartas]
        )

    def atualizar_estado(self, estado):
        self.cartas = [Carta(**carta) for carta in estado.get('cartas')]
