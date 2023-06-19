import random
from models.carta import Carta, POSICOES
from models.conjunto_cartas import ConjuntoCartas

class Monte(ConjuntoCartas):
    def inicializar(self, qtd=1):
        naipes = ["Copas"]
        valores = POSICOES * qtd
        for valor in valores:
            if valor != "Joker":
                for naipe in naipes:
                    carta = Carta(valor, naipe)
                    self.cartas.append(carta)
            else:
                carta = Carta(valor)
                self.cartas.append(carta)
        self.embaralhar()

    def embaralhar(self):
        random.shuffle(self.cartas)

    def comprar_carta(self):
        return self._remover_carta()
