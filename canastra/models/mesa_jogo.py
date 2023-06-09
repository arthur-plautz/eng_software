from models.mesa import Mesa
from models.lixo import Lixo
from models.monte import Monte
from tkinter import *

class MesaJogo(Mesa):
    def __init__(self):
        super().__init__(
            height=200,
            width=1600
        )

    def iniciar_partida(self, n_baralhos):
        self.lixo = Lixo()
        self.monte = Monte()
        self.monte.inicializar(n_baralhos)

    def inicializar_interface(self, master):
        self._inicializar_interface(master)
        self.atualizar_interface()

    def atualizar_interface(self):
        self._canvas_mesa.delete(ALL)

        # Lixo
        x_lixo, y_lixo = self.width - 300, 30
        if not self.lixo.vazio():
            carta_lixo = self.lixo.cartas[0]
            self._canvas_mesa.create_image(x_lixo, y_lixo, anchor=NW, image=carta_lixo.imagem)
        self._canvas_mesa.create_text(x_lixo, y_lixo-20, anchor=NW, text=f"Lixo: {self.lixo.n_cartas}")

        # Monte
        x_monte, y_monte = self.width - 400, 30
        if not self.monte.vazio():
            carta_monte = self.monte.cartas[-1]
            self._canvas_mesa.create_image(x_monte, y_monte, anchor=NW, image=carta_monte.imagem)
        self._canvas_mesa.create_text(x_monte, y_monte-20, anchor=NW, text=f"Monte: {self.monte.n_cartas}")
