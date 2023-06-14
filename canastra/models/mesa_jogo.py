from models.mesa import Mesa
from models.lixo import Lixo
from models.monte import Monte
from tkinter import *

class MesaJogo(Mesa):
    def __init__(self, master):
        super().__init__(
            master=master,
            height=200,
            width=1600
        )

    def iniciar_partida(self, monte):
        self.lixo = Lixo()
        self.monte = Monte(monte)

    def inicializar_interface(self):
        self._inicializar_interface()
        self.atualizar_interface()

    def atualizar_interface(self):
        self._canvas_mesa.delete(ALL)

        # Lixo
        x_lixo, y_lixo = self.width - 300, 30
        if not self.lixo.vazio():
            carta_lixo = self.lixo.cartas[0]
            self._canvas_mesa.create_image(x_lixo, y_lixo, anchor=NW, image=carta_lixo.photo)
        self._canvas_mesa.create_text(x_lixo, y_lixo-20, anchor=NW, text=f"Lixo: {self.lixo.n_cartas}")

        # Monte
        x_monte, y_monte = self.width - 400, 30
        carta_monte = self.monte.cartas[-1]
        self._canvas_mesa.create_image(x_monte, y_monte, anchor=NW, image=carta_monte.photo)
        self._canvas_mesa.create_text(x_monte, y_monte-20, anchor=NW, text=f"Monte: {self.monte.n_cartas}")
