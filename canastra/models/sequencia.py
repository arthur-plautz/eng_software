
class Sequencia:
    def __init__(self, id, cartas) -> None:
        self.id = id
        self.cartas = cartas
    
    @property
    def n_cartas(self):
        return len(self.cartas)

    def canastra(self):
        return self.n_cartas >= 7

    def adicionar_carta(self, carta):
        self.cartas.append(carta)

    def obter_estado(self):
        return dict(
            id=self.id,
            cartas=[carta.serializacao for carta in self.cartas ]
        )
