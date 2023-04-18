from models.jogador import *

class Interface:
    def __init__(self, master):
        self.master = master
        self.master.title("Canastra")

        self.jogador2 = Fake(master, "Jogador 2")
        self.jogador1 = Jogador(master, "Jogador 1", self.jogador2)
