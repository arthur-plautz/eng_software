from models.mesa import Mesa
from models.mao import Mao
from tkinter import *

class MesaJogador(Mesa):
    def __init__(self, master, jogador, visivel):
        super().__init__(
            master=master,
            height=350,
            width=1200
        )

        self.jogador = jogador
        self.visivel = visivel

    def iniciar_partida(self, mao):
        self.sequencias = []
        self.mao = Mao(mao)
        self.iniciar_interface()

    def iniciar_interface(self):
        self._iniciar_interface()

        self._canvas_pontuacao = Canvas(self._frame, width=self.width/3, height=self.height, bg="white")
        self._canvas_pontuacao.pack(side='right')

        self._canvas_pontuacao.create_text(10, 10, anchor=NW, text=f"Pontuação Total [{self.jogador}]:")
        self._canvas_pontuacao.create_text(10, 40, anchor=NW, text="0")
        self.atualizar_interface()

    def atualizar_pontuacao(self, pontuacao):
        self._canvas_pontuacao.delete(ALL)

        self._canvas_pontuacao.create_text(10, 10, anchor=NW, text=f"Pontuação Total [{self.jogador}]:")
        self._canvas_pontuacao.create_text(10, 40, anchor=NW, text=pontuacao)

    def atualizar_interface(self):
        self._canvas_mesa.delete(ALL)

        # Mao
        if self.visivel:
            x_mao, y_mao = 10, 270
            self._canvas_mesa.create_text(x_mao, y_mao-25, anchor=NW, text=f"Mão: {self.mao.n_cartas}")
            for carta in self.mao.cartas:
                self._canvas_mesa.create_image(x_mao, y_mao, anchor=NW, image=carta.imagem)
                x_mao += 20

        # Sequencias
        x_sequencias, y_sequencias = 10, 30
        i = 1
        for sequencias in self.sequencias:
            self._canvas_mesa.create_text(x_sequencias, y_sequencias-20, anchor=NW, text=f"C{i}")
            for carta in sequencias.cartas:
                self._canvas_mesa.create_image(x_sequencias, y_sequencias, anchor=NW, image=carta.imagem)
                y_sequencias += 20
            x_sequencias += 100
            y_sequencias = 30
            i += 1
