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

        self.sequencias = []
        self.mao = Mao()

    def inicia_interface(self):
        self._inicia_interface()

        self.canvas_pontuacao = Canvas(self.frame, width=self.width/3, height=self.height, bg="white")
        self.canvas_pontuacao.pack(side='right')

        self.canvas_pontuacao.create_text(10, 10, anchor=NW, text=f"Pontuação Total [{self.jogador}]:")
        self.canvas_pontuacao.create_text(10, 40, anchor=NW, text="0")
        self.atualiza_interface()

    def atualiza_pontuacao(self):
        self.canvas_pontuacao.delete(ALL)

        pontuacao = sum([sequencia.n_cartas*10 for sequencia in self.sequencias]) - self.mao.n_cartas * 10
        self.canvas_pontuacao.create_text(10, 10, anchor=NW, text=f"Pontuação Total [{self.jogador}]:")
        self.canvas_pontuacao.create_text(10, 40, anchor=NW, text=pontuacao)

    def atualiza_interface(self):
        self.canvas_mesa.delete(ALL)

        # Mao
        if self.visivel:
            x_mao, y_mao = 10, 270
            self.canvas_mesa.create_text(x_mao, y_mao-25, anchor=NW, text=f"Mão: {self.mao.n_cartas}")
            for carta in self.mao.cartas:
                self.canvas_mesa.create_image(x_mao, y_mao, anchor=NW, image=carta.photo)
                x_mao += 20

        # Sequencias
        x_sequencias, y_sequencias = 10, 30
        i = 1
        for sequencias in self.sequencias:
            self.canvas_mesa.create_text(x_sequencias, y_sequencias-20, anchor=NW, text=f"C{i}")
            for carta in sequencias.cartas:
                self.canvas_mesa.create_image(x_sequencias, y_sequencias, anchor=NW, image=carta.photo)
                y_sequencias += 20
            x_sequencias += 100
            y_sequencias = 30
            i += 1

        self.atualiza_pontuacao()