
class Lixo:
    def __init__(self) -> None:
        self.cartas = []

    @property
    def n_cartas(self):
        return len(self.cartas)
    
    def remover_carta(self):
        return self.cartas.pop()
    
    def adicionar_carta(self, carta):
        self.cartas = [carta] + self.cartas
