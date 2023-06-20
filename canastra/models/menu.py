from tkinter import *
from tkinter import messagebox

class MenuJogo:
    def __init__(self, jogador, width, height) -> None:
        self.jogador = jogador
        self.height = height
        self.width = width

        self.inicio_turno = None
        self.habilitado = None

    @property
    def inicio_turno(self):
        return self._inicio_turno

    @inicio_turno.setter
    def inicio_turno(self, inicio_turno):
        self._inicio_turno = inicio_turno

    def limpar_interface(self):
        self._frame.destroy()

    def inicializar_interface(self, master):
        self.master = master

        self._frame = Frame(self.master)
        self._frame.pack()
        self._canvas = Canvas(self._frame, width=self.width, height=self.height, bg="white")
        self._canvas.pack()

        self.atualizar_interface()

    def atualizar_interface(self):
        self.botao_compra = Button(self._canvas, text="Comprar", command=self.comprar)
        self.botao_compra.pack(side='right')
        self.botao_baixa = Button(self._canvas, text="Baixar", command=self.baixar)
        self.botao_baixa.pack(side='right')
        self.botao_descarta = Button(self._canvas, text="Descartar", command=self.descartar)
        self.botao_descarta.pack(side='right')

        self.botao_sair = Button(self._canvas, text="Sair", command=self.master.destroy)
        self.botao_sair.pack(side="left")

    def comprar(self):
        if self.habilitado:
            if self.inicio_turno:
                popup = self.jogador.mesa.criar_popup()
                self._dados_popup = dict()

                label = Label(popup, text="Escolha uma opção de compra")
                origem_listbox = Listbox(popup, selectmode=SINGLE)
                origem_listbox.insert(END, "Monte", "Lixo")
                def origem_select(event):
                    selected = [origem_listbox.get(idx) for idx in origem_listbox.curselection()]
                    self._dados_popup['origem'] = selected[0]
                origem_listbox.bind('<<ListboxSelect>>', origem_select)

                # Botão Comprar
                def comprar_click():
                    self.jogador.comprar_carta(**self._dados_popup)
                comprar_button = Button(popup, text="Comprar Carta(s)", command=comprar_click)

                # Layout
                label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
                origem_listbox.grid(row=1, column=0, padx=5, pady=5, sticky="w")
                comprar_button.grid(row=2, column=0, padx=5, pady=5, sticky="w")
            else:
                messagebox.showinfo(message="Turno em fase principal. Você pode baixar ou descartar.")
        else:
            messagebox.showinfo(message="Turno do Oponente")

    def baixar(self):
        if self.habilitado:
            if not self.inicio_turno:
                popup = self.jogador.mesa.criar_popup()
                self._dados_popup = dict()

                # Selecionar Cartas
                carta_label = Label(popup, text="Selecione as cartas a serem baixadas")
                cartas_listbox = Listbox(popup, selectmode=MULTIPLE)
                cartas_listbox.insert(END, *[carta.texto for carta in self.jogador.mao.cartas])
                def cartas_select(event):
                    selected = [cartas_listbox.get(idx) for idx in cartas_listbox.curselection()]
                    if selected:
                        self._dados_popup['texto_cartas'] = selected
                cartas_listbox.bind('<<ListboxSelect>>', cartas_select)

                # Selecionar Destino
                destino_label = Label(popup, text="Selecione o destino")
                destino_listbox = Listbox(popup, selectmode=SINGLE)
                destino_listbox.insert(END, "Mesa", *[seq.id for seq in self.jogador.sequencias])
                def destino_select(event):
                    selected = [destino_listbox.get(idx) for idx in destino_listbox.curselection()]
                    if selected:
                        self._dados_popup['destino'] = selected[0]
                destino_listbox.bind('<<ListboxSelect>>', destino_select)

                # Botão Baixar
                def baixar_click():
                    self.jogador.baixar_cartas(**self._dados_popup)
                baixar_button = Button(popup, text="Baixar Cartas", command=baixar_click)

                # Layout
                carta_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
                cartas_listbox.grid(row=1, column=0, padx=5, pady=5, sticky="w")
                destino_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
                destino_listbox.grid(row=3, column=0, padx=5, pady=5, sticky="w")
                baixar_button.grid(row=4, column=0, padx=5, pady=5, sticky="w")
            else:
                messagebox.showinfo(message="Turno em fase inicial. Você deve comprar.")
        else:
            messagebox.showinfo(message="Turno do Oponente")

    def descartar(self):
        if self.habilitado:
            if not self.inicio_turno:
                if not self.jogador.mao.vazio():
                    popup = self.jogador.mesa.criar_popup()
                    self._dados_popup = dict()

                    # Selecionar Cartas
                    label = Label(popup, text="Selecione carta a ser descartada")
                    cartas_listbox = Listbox(popup, selectmode=SINGLE)
                    cartas_listbox.insert(END, *[carta.texto for carta in self.jogador.mao.cartas])
                    def carta_select(event):
                        selected = [cartas_listbox.get(idx) for idx in cartas_listbox.curselection()]
                        self._dados_popup['texto_carta'] = selected[0]
                    cartas_listbox.bind('<<ListboxSelect>>', carta_select)

                    # Botão Descartar
                    def descartar_click():
                        self.jogador.descartar_carta(**self._dados_popup)
                    descartar_button = Button(popup, text="Descartar Cartas", command=descartar_click)

                    # Layout
                    label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
                    cartas_listbox.grid(row=1, column=0, padx=5, pady=5, sticky="w")
                    descartar_button.grid(row=2, column=0, padx=5, pady=5, sticky="w")
                else:
                    messagebox.showinfo(message="Fim de jogo!")
                    self.finalizar_partida()
            else:
                messagebox.showinfo(message="Turno em fase inicial. Você deve comprar.")
        else:
            messagebox.showinfo(message="Turno do Oponente")