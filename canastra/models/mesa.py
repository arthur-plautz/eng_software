import tkinter as tk
from models.baralho import Baralho
from models.mao import Mao
from models.lixo import Lixo
from models.combinacao import Combinacao


class Mesa:
    def __init__(self, master, nome_jogador, principal=True):
        self.principal = principal
        self.master = master
        self.nome_jogador = nome_jogador

        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.mesa_canvas = tk.Canvas(self.frame, width=1200, height=400, bg="green")
        self.mesa_canvas.pack(side='left')
        
        self.pontuacao_canvas = tk.Canvas(self.frame, width=300, height=400, bg="white")
        self.pontuacao_canvas.pack(side='right')

        self.pontuacao_canvas.create_text(10, 10, anchor=tk.NW, text=f"Pontuação Total [{nome_jogador}]:")
        self.pontuacao_canvas.create_text(10, 40, anchor=tk.NW, text="0")

        self.inicia_mesa()
        self.botoes()

    def botoes(self):
        if self.principal:
            self.botoes_canvas = tk.Canvas(self.master, width=1500, height=50, bg="white")
            self.botoes_canvas.pack()

            self.compra_button = tk.Button(self.botoes_canvas, text="Comprar", command=self.compra_carta)
            self.compra_button.pack(side='right')

            self.baixa_button = tk.Button(self.botoes_canvas, text="Baixar", command=self.baixa_cartas)
            self.baixa_button.pack(side='right')
            
            self.descarta_button = tk.Button(self.botoes_canvas, text="Descartar", command=self.descarta_carta)
            self.descarta_button.pack(side='right')

            self.sair_button = tk.Button(self.botoes_canvas, text="Sair", command=self.master.destroy)
            self.sair_button.pack(side="left")

    def inicia_mesa(self):
        if self.principal:
            self.baralho = Baralho(2)
            self.combinacoes = []

            self.mao = Mao()
            for i in range(11):
                carta = self.baralho.compra_carta()
                self.mao.adiciona_carta(carta)

            self.lixo = Lixo()
            carta = self.baralho.compra_carta()
            self.lixo.adiciona_carta(carta)

            self.atualiza_mesa()

    def atualiza_pontuacao(self):
        self.pontuacao_canvas.delete(tk.ALL)

        pontuacao = sum([len(comb.cartas)*10 for comb in self.combinacoes]) - len(self.mao.cartas) * 10
        self.pontuacao_canvas.create_text(10, 10, anchor=tk.NW, text=f"Pontuação Total [{self.nome_jogador}]:")
        self.pontuacao_canvas.create_text(10, 40, anchor=tk.NW, text=pontuacao)

    def atualiza_mesa(self):
        self.mesa_canvas.delete(tk.ALL)

        # Lixo
        x_lixo = 1000
        y_lixo = 30
        carta_lixo = self.lixo.cartas[0]
        self.mesa_canvas.create_image(x_lixo, y_lixo, anchor=tk.NW, image=carta_lixo.photo)
        self.mesa_canvas.create_text(x_lixo, y_lixo-20, anchor=tk.NW, text=f"Lixo: {self.lixo.n_cartas}")

        # Monte
        x_baralho = 1100
        y_baralho = 30
        carta_baralho = self.baralho.cartas[-1]
        self.mesa_canvas.create_image(x_baralho, y_baralho, anchor=tk.NW, image=carta_baralho.photo)
        self.mesa_canvas.create_text(x_baralho, y_baralho-20, anchor=tk.NW, text=f"Monte: {self.baralho.n_cartas}")

        # Mao
        x_mao = 10
        y_mao = 270
        self.mesa_canvas.create_text(x_mao, y_mao-25, anchor=tk.NW, text=f"Mão: {self.mao.n_cartas}")
        for carta in self.mao.cartas:
            self.mesa_canvas.create_image(x_mao, y_mao, anchor=tk.NW, image=carta.photo)
            x_mao += 20

        # Combinacoes
        x_combinacoes = 10
        y_combinacoes = 30
        i = 1
        for combinacao in self.combinacoes:
            self.mesa_canvas.create_text(x_combinacoes, y_combinacoes-20, anchor=tk.NW, text=f"C{i}")
            for carta in combinacao.cartas:
                self.mesa_canvas.create_image(x_combinacoes, y_combinacoes, anchor=tk.NW, image=carta.photo)
                y_combinacoes += 20
            x_combinacoes += 100
            y_combinacoes = 30
            i += 1
        
        self.atualiza_pontuacao()

    
    def compra_carta_acao(self):
        carta = self.baralho.compra_carta()
        self.mao.adiciona_carta(carta)
        self.atualiza_mesa()
        self.popup.destroy()

    
    def compra_carta(self):
        self.popup = tk.Toplevel(self.master)

        label = tk.Label(self.popup, text="Escolha uma opção de compra")
        monte_button = tk.Button(self.popup, text="Monte", command=self.compra_carta_acao)
        lixo_button = tk.Button(self.popup, text="Lixo", command=self.compra_carta_acao)

        label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        monte_button.grid(row=1, column=1, padx=5, pady=5, sticky="e")
        lixo_button.grid(row=1, column=2, padx=5, pady=5, sticky="e")
    
    
    def baixa_cartas_acao(self):
        cartas = []
        for i in range(3):
            cartas.append(self.mao.remove_carta())
        combinacao = Combinacao(cartas)
        self.combinacoes.append(combinacao)
        self.atualiza_mesa()
        self.popup.destroy()


    def descarta_cartas_acao(self):
        carta = self.mao.remove_carta()
        self.lixo.adiciona_carta(carta)
        self.atualiza_mesa()
        self.popup.destroy()


    def baixa_cartas(self):
        self.popup = tk.Toplevel(self.master)

        label = tk.Label(self.popup, text="Digite as cartas a serem baixadas (1,A,K)")
        cartas_entry = tk.Entry(self.popup)
        baixar_button = tk.Button(self.popup, text="Baixar Cartas", command=self.baixa_cartas_acao)

        label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        cartas_entry.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        baixar_button.grid(row=2, column=0, padx=5, pady=5, sticky="w")

    
    def descarta_carta(self):
        self.popup = tk.Toplevel(self.master)

        label = tk.Label(self.popup, text="Digite as cartas a serem descartadas (1,A,K)")
        cartas_entry = tk.Entry(self.popup)
        descartar_button = tk.Button(self.popup, text="Descartar Cartas", command=self.descarta_cartas_acao)

        label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        cartas_entry.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        descartar_button.grid(row=2, column=0, padx=5, pady=5, sticky="w")
