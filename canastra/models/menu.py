from tkinter import *

class MenuJogo:
    def __init__(self, master, width, height) -> None:
        self.master = master
        self.height = height
        self.width = width

    def atualiza_jogador(self, jogador):
        self.jogador = jogador

    def inicia_interface(self):
        self.canvas = Canvas(self.master, width=self.width, height=self.height, bg="white")
        self.canvas.pack()

        self.atualiza_interface()

    def atualiza_interface(self):
        self.botao_compra = Button(self.canvas, text="Comprar", command=self.comprar)
        self.botao_compra.pack(side='right')
        self.botao_baixa = Button(self.canvas, text="Baixar", command=self.baixar)
        self.botao_baixa.pack(side='right')
        self.botao_descarta = Button(self.canvas, text="Descartar", command=self.descartar)
        self.botao_descarta.pack(side='right')

        self.botao_sair = Button(self.canvas, text="Sair", command=self.master.destroy)
        self.botao_sair.pack(side="left")

    def comprar(self):
        popup = self.jogador.mesa.cria_popup()

        label = Label(popup, text="Escolha uma opção de compra")
        monte_button = Button(popup, text="Monte", command=self.jogador.comprar_carta)
        lixo_button = Button(popup, text="Lixo", command=self.jogador.comprar_carta)

        # Layout
        label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        monte_button.grid(row=1, column=1, padx=5, pady=5, sticky="e")
        lixo_button.grid(row=1, column=2, padx=5, pady=5, sticky="e")

    def baixar(self):
        popup = self.jogador.mesa.cria_popup()

        # Selecionar Cartas
        carta_label = Label(popup, text="Selecione as cartas a serem baixadas")
        cartas_listbox = Listbox(popup, selectmode=MULTIPLE)
        for carta in self.jogador.mao.cartas:
            cartas_listbox.insert(END, f"{carta.valor} - {carta.naipe}")

        # Selecionar Destino
        destino_label = Label(popup, text="Selecione o destino")
        destino_listbox = Listbox(popup, selectmode=SINGLE)
        destino_listbox.insert(END, "Mesa")
        for i in range(len(self.jogador.sequencias)):
            destino_listbox.insert(END, f"C{i+1}")
        baixar_button = Button(popup, text="Baixar Cartas", command=self.jogador.baixar_cartas)

        # Layout
        carta_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        cartas_listbox.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        destino_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        destino_listbox.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        baixar_button.grid(row=4, column=0, padx=5, pady=5, sticky="w")

    def descartar(self):
        popup = self.jogador.mesa.cria_popup()

        # Selecionar Cartas
        label = Label(popup, text="Selecione as cartas a serem baixadas")
        cartas_listbox = Listbox(popup, selectmode=MULTIPLE)
        for carta in self.jogador.mao.cartas:
            cartas_listbox.insert(END, f"{carta.valor} - {carta.naipe}")
        descartar_button = Button(popup, text="Descartar Cartas", command=self.jogador.descartar_carta)

        # Layout
        label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        cartas_listbox.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        descartar_button.grid(row=2, column=0, padx=5, pady=5, sticky="w")
