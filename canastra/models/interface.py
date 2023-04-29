from models.jogador import Jogador
from models.mesa_jogo import MesaJogo
from models.menu import MenuJogo
from tkinter import *
from tkinter import messagebox
from py_netgames_client.tkinter_client.PyNetgamesServerProxy import PyNetgamesServerProxy
from py_netgames_client.tkinter_client.PyNetgamesServerListener import PyNetgamesServerListener

class Interface(PyNetgamesServerListener):
    def __init__(self):
        self.width = 1600
        self.height = 1200

        self.master = Tk()
        self.master.title("Canastra")
        self.master.geometry(f"{self.width}x{self.height}")
        self.master.resizable(False, False)

        self.jogador1 = Jogador(self.master, "Jogador 1")
        self.jogador2 = Jogador(self.master, "Jogador 2", visivel=False)
        
        self.mesa = MesaJogo(self.master)
        self.menu = MenuJogo(self.master, width=self.width, height=self.height)

        self.server_url = "wss://py-netgames-server.fly.dev"
        self.add_listener()
        self.send_connection()

        self.tela_inicial()
        self.master.mainloop()

    def tela_inicial(self):
        self.frame.destroy()

        self.frame = Frame(self.master)
        self.frame.pack()
        self.canvas = Canvas(self.frame, width=self.width, height=self.height)
        self.canvas.pack()

        label = Label(self.canvas, text="Canastra", font="Arial 40")
        self.partida_button = Button(self.canvas, text="Iniciar Partida", command=self.inicia_partida)
        self.sair_button = Button(self.canvas, text="Sair", command=self.master.destroy)

        label.pack()
        self.partida_button.pack()
        self.sair_button.pack()

    def inicia_partida(self):
        self.frame.destroy()

        self.jogador2.inicia_partida(self.mesa.lixo, self.mesa.baralho)
        self.mesa.inicia_interface()
        self.jogador1.inicia_partida(self.mesa.lixo, self.mesa.baralho)
        self.menu.inicia_interface()

        self.menu.atualiza_jogador(self.jogador1)

    def atualiza_mesas(self):
        self.mesa_canvas.delete(ALL)

        self.mesa.atualiza_interface()
        self.jogador2.mesa.atualiza_interface()
        self.jogador1.mesa.atualiza_interface()

    def set_match_id(self, match_id):
        self.match_id = match_id
        
    def get_match_id(self):
        return self.match_id

    def add_listener(self): # Pyng use case "add listener"
        self.server_proxy = PyNetgamesServerProxy()
        self.server_proxy.add_listener(self)

    def send_connection(self):  # Pyng use case "send connect"
        self.server_proxy.send_connect(self.server_url)
        #self.server_proxy.send_connect()

    def send_match(self, amount_of_players):    # Pyng use case "send match"
        self.server_proxy.send_match(amount_of_players)

    def receive_connection_success(self):   # Pyng use case "receive connection"
        messagebox.showinfo(message='Conectado ao servidor') 
        self.send_match(2)  # Pyng use case "send match"

    def receive_disconnect(self):   # Pyng use case "receive disconnect"
        messagebox.showinfo(message='Desconectado do servidor')
        self.tela_inicial()
        # new_state = self.myBoard.getState()
        # self.update_user_interface(new_state)
        self.send_connection()  # Pyng use case "send connect"

    def receive_error(self, error): # Pyng use case "receive error"
        messagebox.showinfo(message='Notificação de erro do servidor. Feche o programa.') 

    def receive_match(self, match): # Pyng use case "receive match"
        messagebox.showinfo(message='Partida iniciada') 
        self.set_match_id(match.match_id)
        if (match.position == 1):
            self.inicia_partida()

    def receive_move(self, move):   # Pyng use case "receive move"
        received_move = move.payload
        # self.menu.botao_descarta.click(int(received_move['line']), int(received_move['column']))
        # new_state = self.myBoard.getState()
        # self.update_user_interface(new_state)
        # if (new_state.get_match_status() == 2):
        #     self.enable_interface()
