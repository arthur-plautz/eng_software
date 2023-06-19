from models.conjunto_cartas import ConjuntoCartas

class Lixo(ConjuntoCartas):
    def __init__(self, cartas=[]):
        super().__init__(cartas)

    def comprar_cartas(self):
        cartas = self.cartas
        self.cartas = []
        return cartas

    def adicionar_carta(self, carta):
        self.cartas = [carta] + self.cartas
