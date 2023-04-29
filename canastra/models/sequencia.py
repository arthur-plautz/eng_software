
class Sequencia:
    def __init__(self, cartas) -> None:
        self.cartas = cartas
    
    @property
    def n_cartas(self):
        return len(self.cartas)

    def adiciona_carta(self, carta):
        self.cartas.append(carta)
