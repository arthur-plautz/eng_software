
class Mao:
    def __init__(self, cartas) -> None:
        self.cartas = cartas if cartas else []

    @property
    def n_cartas(self):
        return len(self.cartas)

    def remover_carta(self):
        return self.cartas.pop()
    
    def adicionar_carta(self, carta):
        self.cartas.append(carta)
