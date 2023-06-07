import random
from models.carta import Carta


class Monte:
    def __init__(self, qtd=1):
        self.cartas = []
        naipes = ["Copas", "Ouros", "Paus", "Espadas"]
        valores = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"] * qtd
        for naipe in naipes:
            for valor in valores:
                carta = Carta(naipe, valor)
                self.cartas.append(carta)
        random.shuffle(self.cartas)

    @property
    def n_cartas(self):
        return len(self.cartas)

    def comprar_carta(self):
        return self.cartas.pop()
