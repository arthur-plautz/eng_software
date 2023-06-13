from models.jogador import Jogador
from models.mesa_jogo import MesaJogo
from models.menu import MenuJogo
from tkinter import *
from tkinter import messagebox
from datetime import datetime, timedelta
from py_netgames_client.tkinter_client.PyNetgamesServerProxy import PyNetgamesServerProxy
from py_netgames_client.tkinter_client.PyNetgamesServerListener import PyNetgamesServerListener

class InterfaceJogador(PyNetgamesServerListener):
    def __init__(self):
        self.width = 1600
        self.height = 1200

        self.master = Tk()
        self.master.title("Canastra")
        self.master.geometry(f"{self.width}x{self.height}")
        self.master.resizable(False, False)
        self._frame_jogo = None

        self.turno_local = None
        self.inicio_turno = None
        self.tempo_inicial = None
        self.partida_andamento = False

        self.jogador = Jogador("Jogador")
        self.oponente = Jogador("Oponente")
    
        self.mesa_jogo = MesaJogo(self.master)
        self.menu_jogo = MenuJogo(self.master, self.jogador, width=self.width, height=self.height)

        self.tela_inicial()

        self.server_url = "wss://py-netgames-server.fly.dev"
        self.add_listener()
        self.send_connection()

        self.master.mainloop()

    def obter_estado(self):
        estado_jogador = self.jogador.obter_estado()
        estado_oponente = self.oponente.obter_estado()
        estado_monte = self.mesa_jogo.monte.obter_estado()
        estado_lixo = self.mesa_jogo.lixo.obter_estado()

        return dict(
            partida_andamento=self.partida_andamento,
            monte=estado_monte,
            lixo=estado_lixo,
            jogador=estado_jogador,
            oponente=estado_oponente
        )

    def atualizar_estado(self, estado):
        self.partida_andamento = estado.get('partida_andamento')
        self.mesa_jogo.lixo.atualizar_estado(estado.get('lixo'))
        self.mesa_jogo.monte.atualizar_estado(estado.get('monte'))
        self.jogador.atualizar_estado(estado.get('oponente'))
        self.oponente.atualizar_estado(estado.get('jogador'))

        self.atualizar_interface()

    def enviar_jogada(self):
        messagebox.showinfo(message='Turno do oponente')
        self.alterar_turno()
        estado = self.obter_estado()
        self.server_proxy.send_move(
            match=self.match_id,
            payload=estado
        )

    def tela_inicial(self):
        if self._frame_jogo: self._frame_jogo.destroy()

        self._frame_jogo = Frame(self.master)
        self._frame_jogo.pack()
        self._canvas_jogo = Canvas(self._frame_jogo, width=self.width, height=self.height)
        self._canvas_jogo.pack()

        label = Label(self._canvas_jogo, text="Canastra", font="Arial 40")
        partida_button = Button(self._canvas_jogo, text="Iniciar Partida", command=self.send_match)
        sair_button = Button(self._canvas_jogo, text="Sair", command=self.master.destroy)

        label.pack()
        partida_button.pack()
        sair_button.pack()

    def definir_turno_inicial(self):
        limiar_decisao = timedelta(seconds=2)
        tempo_inicializacao = datetime.now() - self.tempo_inicial
        if tempo_inicializacao > limiar_decisao:
            self.turno_local = True
            self.jogador.nome = "Jogador 1"
            self.oponente.nome = "Jogador 2"
        else:
            self.turno_local = False
            self.jogador.nome = "Jogador 2"
            self.oponente.nome = "Jogador 1"

    def definir_estado_inicial(self):
        if self.turno_local:
            mao = 11
            monte = 2
        else:
            mao = 0
            monte = 0
        return mao, monte

    def inicializar_interface(self):
        self._frame_jogo.destroy()

        self.oponente.inicializar_interface(self.master, self.mesa_jogo, visivel=False)
        self.mesa_jogo.inicializar_interface()
        self.jogador.inicializar_interface(self.master, self.mesa_jogo)
        self.menu_jogo.inicializar_interface()

        self.jogador.finalizar_turno = self.enviar_jogada

    def finalizar_partida(self):
        self.partida_andamento = False

        self.jogador.calcular_pontuacao()
        self.oponente.calcular_pontuacao()

    def alterar_turno(self):
        if self.turno_local:
            self.turno_local = False
        else:
            self.turno_local = True
            self.alterar_fase_turno()

    def alterar_fase_turno(self):
        if self.inicio_turno:
            self.inicio_turno = False
        else:
            self.inicio_turno = True

    def atualizar_interface(self):
        self.mesa_jogo_canvas.delete(ALL)

        self.mesa_jogo.atualizar_interface()
        self.oponente.mesa.atualizar_interface()
        self.jogador.mesa.atualizar_interface()

    def set_match_id(self, match_id):
        self.match_id = match_id
        
    def get_match_id(self):
        return self.match_id

    def add_listener(self):    # Pyng use case "add listener"
        self.server_proxy = PyNetgamesServerProxy()
        self.server_proxy.add_listener(self)

    def send_connection(self): # Pyng use case "send connect"
        self.server_proxy.send_connect(self.server_url)

    def send_match(self, amount_of_players=2):# Pyng use case "send match"
        messagebox.showinfo(message='Aguardando outro jogador')
        self.tempo_inicial = datetime.now()
        self.server_proxy.send_match(amount_of_players)

    def receive_connection_success(self):# Pyng use case "receive connection"
        messagebox.showinfo(message='Conectado ao servidor') 

    def receive_disconnect(self):# Pyng use case "receive disconnect"
        messagebox.showinfo(message='Desconectado do servidor')
        self.tela_inicial()
        self.send_connection()    # Pyng use case "send connect"
        
    def receive_error(self, error):# Pyng use case "receive error"
        messagebox.showinfo(message='Notificação de erro do servidor. Feche o programa.') 

    def receive_match(self, match):# Pyng use case "receive match"
        messagebox.showinfo(message='Partida iniciada')
        self.set_match_id(match.match_id)
        self.partida_andamento = True

        self.definir_turno_inicial()
        if not self.turno_local:
            messagebox.showinfo(message='Turno do Oponente')

        mao, monte = self.definir_estado_inicial()
        self.mesa_jogo.iniciar_partida(monte)
        self.oponente.iniciar_partida(mao)
        self.jogador.iniciar_partida(mao)

        self.inicializar_interface()

    def receive_move(self, move):# Pyng use case "receive move"
        estado = move.payload
        self.atualizar_estado(estado)
        self.alterar_turno()
