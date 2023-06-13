from models.carta import Carta

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

    def obter_estado(self):
        return [carta.serializacao for carta in self.cartas]

    def atualizar_estado(self, estado):
        self.cartas = [Carta(**carta) for carta in estado] 