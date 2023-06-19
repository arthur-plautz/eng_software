from models.mesa_jogador import MesaJogador
from models.sequencia import Sequencia
from models.carta import Carta
from tkinter import messagebox

class Jogador:
    def __init__(self, nome):
        self.nome = nome
        self.vencedor = False
        self.pontuacao = None
        self.mao = None
        self.sequencias = None
        self.mesa = None

    def alterar_fase_turno(self):
        pass

    def enviar_jogada(self):
        pass

    def iniciar_partida(self, mesa_jogo, n_cartas, visivel=True):
        self.mesa = MesaJogador(self.nome, visivel)
        self._mesa_jogo = mesa_jogo
        self._lixo = self._mesa_jogo.lixo
        self._monte = self._mesa_jogo.monte

        cartas = []
        for i in range(n_cartas):
            carta = self._monte.comprar_carta()
            cartas.append(carta)
        self.mao, self.sequencias = self.mesa.iniciar_partida(cartas)

    def _atualizar_interface(self):
        self.mesa.destruir_popup()
        self.mesa.atualizar_pontuacao(self.pontuacao)
        self.mesa.atualizar_interface()
        self._mesa_jogo.atualizar_interface()

    def calcular_pontuacao(self):
        soma_pontos = 0
        for sequencia in self.sequencias:
            soma_pontos += sequencia.n_cartas * 10
            if sequencia.canastra() and not sequencia.suja():
                soma_pontos += 300
            elif sequencia.canastra():
                soma_pontos += 200
        soma_pontos -= self.mao.n_cartas * 10
        self.pontuacao = soma_pontos

    def comprar_carta(self, origem):
        if origem == 'Monte':
            cartas = [self._monte.comprar_carta()]
        else:
            if not self._lixo.vazio():
                cartas = self._lixo.comprar_cartas()
            else:
                messagebox.showinfo(message="Lixo vazio")
                return None

        for carta in cartas:
            self.mao.adicionar_carta(carta)
        self.calcular_pontuacao()
        self._atualizar_interface()
        self.alterar_fase_turno()

    def baixar_cartas(self, destino=None, texto_cartas=None):
        cartas = [self._obter_carta(texto) for texto in texto_cartas]
        sequencia = self.verificar_sequencia(cartas=cartas, destino=destino)
        if sequencia:
            if destino == 'Mesa':
                self.adicionar_sequencia(sequencia)
            else:
                index_seq = self.obter_posicao_sequencia(sequencia.id)
                self.sequencias[index_seq] = sequencia
            for carta in cartas:
                self.mao.remover_carta(**carta.serializacao)
        self.calcular_pontuacao()
        self._atualizar_interface()

    def descartar_carta(self, texto_carta):
        carta = self._obter_carta(texto_carta)
        self.mao.remover_carta(**carta.serializacao)
        self._lixo.adicionar_carta(carta)
        self.calcular_pontuacao()
        self._atualizar_interface()
        self.enviar_jogada()

    def _obter_carta(self, texto_carta):
        if texto_carta.find('-') != -1:
            valor, naipe = texto_carta.split('-')
            return Carta(naipe=naipe, valor=valor)
        else:
            valor = texto_carta
            return Carta(valor=valor)

    def obter_posicao_sequencia(self, seq_id):
        sequencias_existentes = [seq.id for seq in self.sequencias]
        index_seq = sequencias_existentes.index(seq_id)
        return index_seq

    def adicionar_sequencia(self, sequencia):
        self.sequencias.append(sequencia)
        self.mesa.sequencias = self.sequencias

    def ordenar_sequencia(self, sequencia):
        cartas = sequencia.cartas
        posicoes = sorted([carta.posicao for carta in cartas], reverse=True)
        for pos in posicoes:
            for carta in cartas:
                if carta.posicao == pos:
                    cartas.remove(carta)
                    sequencia.adicionar_carta(carta)
        return sequencia

    def verificar_sequencia(self, destino, cartas):
        sequencia = None
        if destino == 'Mesa':
            if len(cartas) >= 3:
                id_seq = len(self.sequencias)
                sequencia = Sequencia(f"C{id_seq}", cartas)
            else:
                messagebox.showinfo(message="Cartas Insuficientes")
                return None
        else:
            index_seq = self.obter_posicao_sequencia(destino)
            seq = self.sequencias[index_seq]
            cartas += [Carta(**carta.serializacao) for carta in seq.cartas]
            sequencia = Sequencia(id=seq.id)
            for carta in cartas:
                sequencia.adicionar_carta(carta)

        coringa = sequencia.remover_coringa()
        
        naipe = str(sequencia.cartas[0].naipe).lower()
        for carta in sequencia.cartas[1:]:
            if str(carta.naipe).lower() != naipe:
                messagebox.showinfo(message="Cartas numa sequencia devem ter o mesmo naipe")
                return None

        posicoes_ordenadas = sorted([carta.posicao for carta in sequencia.cartas])
        prev = min(posicoes_ordenadas)
        for pos in posicoes_ordenadas[1:]:
            if abs(pos - prev) == 1:
                prev = pos
            elif abs(pos - prev) == 2 and coringa:
                coringa.definir_posicao(pos-1)
                sequencia.adicionar_carta(coringa)
                coringa = None
                prev = pos-1
            else:
                messagebox.showinfo(message="Sequencia Inválida")
                return None
        sequencia_ordenada = self.ordenar_sequencia(sequencia)
        return sequencia_ordenada

    def obter_estado(self):
        sequencias = [sequencia.obter_estado() for sequencia in self.sequencias]
        return dict(
            mao=self.mao.obter_estado(),
            sequencias=sequencias,
            pontuacao=self.pontuacao,
            vencedor=self.vencedor
        )

    def atualizar_estado(self, estado):
        self.pontuacao = estado.get('pontuacao')
        self.vencedor = estado.get('vencedor')
        self.mao.atualizar_estado(estado.get('mao'))
        sequencias = []
        for sequencia in estado.get('sequencias'):
            cartas = [Carta(**carta) for carta in sequencia.get('cartas')]
            sequencias.append(Sequencia(id=sequencia.get('id'), cartas=cartas))
        self.sequencias = sequencias
        self.mesa.atualizar_estado(self.mao, self.sequencias)
