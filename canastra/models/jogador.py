import tkinter as tk
from models.mesa import Mesa

class Jogador:
    def __init__(self, master, nome_jogador, oponente):
        self.master = master
        self.nome_jogador = nome_jogador
        self.oponente = oponente
        self.tela_inicial()

    def inicia_partida(self):
        self.frame.destroy()
        self.oponente.inicia_partida()
        self.mesa = Mesa(self.master, self.nome_jogador)

    def tela_inicial(self):
        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.canvas = tk.Canvas(self.frame, width=1500, height=900)
        self.canvas.pack()

        label = tk.Label(self.canvas, text="Canastra", font="Arial 40")
        label.pack()

        self.partida_button = tk.Button(self.canvas, text="Iniciar Partida", command=self.inicia_partida)
        self.partida_button.pack()

        self.sair_button = tk.Button(self.canvas, text="Sair", command=self.master.destroy)
        self.sair_button.pack()

class Fake:
    def __init__(self, master, nome_jogador):
        self.master = master
        self.nome_jogador = nome_jogador
    
    def inicia_partida(self):
        self.mesa = Mesa(self.master, self.nome_jogador, principal=False)


