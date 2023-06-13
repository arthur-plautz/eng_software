from models.mesa_jogador import MesaJogador
from models.sequencia import Sequencia

class Jogador:
    def __init__(self, nome):
        self.nome = nome
        self.vencedor = False
        self.pontuacao = None
        self.mao = None
        self.sequencias = None

    def iniciar_partida(self, mao):
        cartas = []
        for i in range(mao):
            carta = self._monte.comprar_carta()
            cartas.append(carta)
        self.mesa.iniciar_partida(cartas)

    def inicializar_interface(self, master, mesa_jogo, visivel=True):
        self.mesa = MesaJogador(master, self.nome, visivel)
        self._mesa_jogo = mesa_jogo
        self._lixo = self._mesa_jogo.lixo
        self._monte = self._mesa_jogo.monte
        self.mao = self.mesa.mao
        self.sequencias = self.mesa.sequencias
        self.mesa.inicializar_interface()

    def _atualizar_interface(self):
        self.mesa.destruir_popup()
        self.mesa.atualizar_pontuacao(self.pontuacao)
        self.mesa.atualizar_interface()
        self._mesa_jogo.atualizar_interface()

    def calcular_pontuacao(self):
        soma_pontos = 0
        for sequencia in self.sequencias:
            soma_pontos += sequencia.n_cartas * 10
        soma_pontos -= self.mao.n_cartas * 10
        self.pontuacao = soma_pontos

    def comprar_carta(self):
        carta = self._monte.comprar_carta()
        self._mao.adicionar_carta(carta)
        self.calcula_pontuacao()
        self._atualizar_interface()

    def baixar_cartas(self):
        cartas = []
        for i in range(3):
            cartas.append(self._mao.remover_carta())
        sequencia = Sequencia(cartas)
        self._sequencias.append(sequencia)
        self.calcula_pontuacao()
        self._atualizar_interface()

    def descartar_carta(self):
        carta = self._mao.remover_carta()
        self._lixo.adicionar_carta(carta)
        self.calcula_pontuacao()
        self._atualizar_interface()
        self.finalizar_turno()

    def verificar_sequencia(self, cartas, destino):
        sequencia = None
        if str(destino) == 'mesa':
            if len(cartas) >= 3:
                sequencia = cartas
            else:
                pass # Notificar cartas insuficientes
        elif str(destino).startswith('c'):
            sequencias_existentes = [seq.id for seq in self.sequencias]
            if destino in sequencias_existentes:
                index_seq = sequencias_existentes.index(destino)
                sequencia = self.sequencias[index_seq]
                for carta in cartas:
                    sequencia.adicionar_carta(carta)
            else:
                pass # Notificar destino inexistente
        
        valores_ordenados = sorted([carta.valor for carta in sequencia.cartas])
        prev = min(valores_ordenados)
        for valor in valores_ordenados[1:]:
            if valor > prev and abs(valor - prev) == 1:
                prev = valor
            else:
                pass # Notificar sequencia invalida
        
        return sequencia

    def obter_estado(self):
        sequencias = [sequencia.obter_estado() for sequencia in self.sequencias]
        return dict(
            mao=self.mao.obter_estado(),
            sequencias=sequencias,
            pontuacao=self.pontuacao
        )

    def atualizar_estado(self, estado):
        self.pontuacao = self.estado.get('pontuacao')
        self.mao.atualizar(estado.get('mao'))
        self.sequencias = [Sequencia(**sequencia) for sequencia in estado.get('sequencias')]
