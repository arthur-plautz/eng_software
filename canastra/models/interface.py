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
        self.tempo_inicial = None
        self.partida_andamento = False
        self.finalizacao = False

        self.jogador = Jogador("Jogador")
        self.oponente = Jogador("Oponente")
    
        self.mesa_jogo = MesaJogo()
        self.menu_jogo = MenuJogo(self.jogador, width=self.width, height=self.height)

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
            finalizacao=self.finalizacao,
            monte=estado_monte,
            lixo=estado_lixo,
            jogador=estado_jogador,
            oponente=estado_oponente
        )

    def atualizar_estado(self, estado):
        self.partida_andamento = estado.get('partida_andamento')
        self.finalizacao = estado.get('finalizacao')
        if self.partida_andamento:
            self.mesa_jogo.lixo.atualizar_estado(estado.get('lixo'))
            self.mesa_jogo.monte.atualizar_estado(estado.get('monte'))
            self.oponente.atualizar_estado(estado.get('jogador'))
            self.jogador.atualizar_estado(estado.get('oponente'))
            self.atualizar_interface()
        else:
            self.finalizar_partida()

    def enviar_jogada(self):
        messagebox.showinfo(message='Turno do oponente')
        self.finalizar_turno()
        estado = self.obter_estado()
        self.server_proxy.send_move(
            match_id=self.match_id,
            payload=estado
        )

    def limpar_interface(self):
        if self.partida_andamento:
            self.oponente.mesa.limpar_interface()
            self.mesa_jogo.limpar_interface()
            self.jogador.mesa.limpar_interface()
            self.menu_jogo.limpar_interface()
        if self._frame_jogo: self._frame_jogo.destroy()

    def tela_inicial(self):
        self.limpar_interface()

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

    def finalizar_turno(self):
        self.alterar_turno()
        if self.jogador.mao.vazio() or self.mesa_jogo.monte.vazio():
            self.partida_andamento = False

    def definir_turno_inicial(self):
        limiar_decisao = timedelta(seconds=2)
        tempo_inicializacao = datetime.now() - self.tempo_inicial
        if tempo_inicializacao > limiar_decisao:
            self.turno_local = True
            self.menu_jogo.habilitado = True
            self.menu_jogo.inicio_turno = True
            self.jogador.nome = "Jogador 1"
            self.oponente.nome = "Jogador 2"
        else:
            self.turno_local = False
            self.menu_jogo.habilitado = False
            self.menu_jogo.inicio_turno = False
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

        self.oponente.mesa.inicializar_interface(self.master)
        self.mesa_jogo.inicializar_interface(self.master)
        self.jogador.mesa.inicializar_interface(self.master)
        self.menu_jogo.inicializar_interface(self.master)

        self.jogador.enviar_jogada = self.enviar_jogada
        self.jogador.alterar_fase_turno = self.alterar_fase_turno
        self.menu_jogo.finalizar_partida = self.finalizar_partida

    def finalizar_partida(self):
        self.jogador.calcular_pontuacao()
        self.oponente.calcular_pontuacao()

        if not self.finalizacao:
            self.finalizacao = True
            self.enviar_jogada()

        # Info
        if self.jogador.pontuacao > self.oponente.pontuacao:
            self.jogador.vencedor = True
            messagebox.showinfo(message=f"{self.jogador.nome} Venceu!")
        elif self.jogador.pontuacao < self.oponente.pontuacao:
            self.oponente.vencedor = True
            messagebox.showinfo(message=f"{self.oponente.nome} Venceu!")
        else:
            messagebox.showinfo(message=f"Empate!")

        self.oponente.mesa.limpar_interface()
        self.mesa_jogo.limpar_interface()
        self.jogador.mesa.limpar_interface()
        self.menu_jogo.limpar_interface()
        self.tela_inicial()

    def alterar_turno(self):
        if self.turno_local:
            self.turno_local = False
            self.menu_jogo.habilitado = False
        else:
            self.turno_local = True
            self.menu_jogo.habilitado = True
            self.alterar_fase_turno()

    def alterar_fase_turno(self):
        if self.menu_jogo.inicio_turno:
            self.menu_jogo.inicio_turno = False
        else:
            self.menu_jogo.inicio_turno = True

    def atualizar_interface(self):
        self.oponente.mesa.atualizar_interface()
        self.mesa_jogo.atualizar_interface()
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

    def receive_match(self, match=None):# Pyng use case "receive match"
        messagebox.showinfo(message='Partida iniciada')
        self.set_match_id(match.match_id)
        self.partida_andamento = True

        self.definir_turno_inicial()
        if not self.turno_local:
            messagebox.showinfo(message='Turno do Oponente')

        mao, monte = self.definir_estado_inicial()

        self.mesa_jogo.iniciar_partida(monte)
        self.oponente.iniciar_partida(self.mesa_jogo, mao, visivel=False)
        self.jogador.iniciar_partida(self.mesa_jogo, mao)

        self.inicializar_interface()

    def receive_move(self, move):# Pyng use case "receive move"
        estado = move.payload
        self.atualizar_estado(estado)
        self.alterar_turno()
