from models.mesa import Mesa
from models.lixo import Lixo
from models.baralho import Baralho
from tkinter import *

class MesaJogo(Mesa):
    def __init__(self, master,):
        super().__init__(
            master=master,
            height=200,
            width=1600
        )

        self.baralho = Baralho(2)
        self.lixo = Lixo()

    def inicia_interface(self):
        self._inicia_interface()
        self.atualiza_interface()

    def atualiza_interface(self):
        self.canvas_mesa.delete(ALL)

        # Lixo
        x_lixo, y_lixo = self.width - 300, 30
        if self.lixo.n_cartas > 0:
            carta_lixo = self.lixo.cartas[0]
            self.canvas_mesa.create_image(x_lixo, y_lixo, anchor=NW, image=carta_lixo.photo)
        self.canvas_mesa.create_text(x_lixo, y_lixo-20, anchor=NW, text=f"Lixo: {self.lixo.n_cartas}")

        # Monte
        x_baralho, y_baralho = self.width - 400, 30
        carta_baralho = self.baralho.cartas[-1]
        self.canvas_mesa.create_image(x_baralho, y_baralho, anchor=NW, image=carta_baralho.photo)
        self.canvas_mesa.create_text(x_baralho, y_baralho-20, anchor=NW, text=f"Monte: {self.baralho.n_cartas}")
