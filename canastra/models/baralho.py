import random
from models.carta import Carta


class Baralho:
    def __init__(self, qtd=1):
        self.cartas = []
        naipes = ["Hearts", "Diamonds", "Clubs", "Spades"]
        valores = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"] * qtd
        for naipe in naipes:
            for valor in valores:
                carta = Carta(naipe, valor)
                self.cartas.append(carta)
        random.shuffle(self.cartas)

    @property
    def n_cartas(self):
        return len(self.cartas)

    def compra_carta(self):
        return self.cartas.pop()
