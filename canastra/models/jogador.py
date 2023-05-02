from models.mesa_jogador import MesaJogador
from models.sequencia import Sequencia

class Jogador:
    def __init__(self, master, nome, visivel=True):
        self.master = master
        self.nome = nome

        self.mesa = MesaJogador(master, nome, visivel)

    @property
    def mao(self):
        return self._mao

    @property
    def sequencias(self):
        return self._sequencias

    def inicia_partida(self, lixo, baralho):
        self._lixo = lixo
        self._baralho = baralho
    
        cartas_mao = self.inicia_mao()
        self.mesa.inicia_partida(cartas_mao)

        self._sequencias = self.mesa.sequencias
        self._mao = self.mesa.mao

    def inicia_mao(self):
        cartas = []
        for i in range(11):
            carta = self._baralho.compra_carta()
            cartas.append(carta)
        return cartas

    def atualiza_acao(self):
        self.mesa.destroy_popup()
        self.mesa.atualiza_interface()

    def comprar_carta(self):
        carta = self._baralho.compra_carta()
        self._mao.adiciona_carta(carta)
        self.atualiza_acao()

    def baixar_cartas(self):
        cartas = []
        for i in range(3):
            cartas.append(self._mao.remove_carta())
        sequencia = Sequencia(cartas)
        self._sequencias.append(sequencia)
        self.atualiza_acao()

    def descartar_carta(self):
        carta = self._mao.remove_carta()
        self._lixo.adiciona_carta(carta)
        self.atualiza_acao()

    def verifica_sequencia(self, sequencia):
        pass
