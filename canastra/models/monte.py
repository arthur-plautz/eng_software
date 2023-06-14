import random
from models.carta import Carta
from models.conjunto_cartas import ConjuntoCartas

class Monte(ConjuntoCartas):
    def inicializar(self, qtd=1):
        naipes = ["Copas", "Ouros", "Paus", "Espadas"]
        valores = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"] * qtd
        for naipe in naipes:
            for valor in valores:
                carta = Carta(naipe, valor)
                self.cartas.append(carta)
        self.embaralhar()

    def embaralhar(self):
        random.shuffle(self.cartas)

    def comprar_carta(self):
        return self._remover_carta()
