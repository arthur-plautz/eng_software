from tkinter import *

class Mesa:
    def __init__(self, master, height, width):
        self.master = master
        self.height = height
        self.width = width

    def _iniciar_interface(self):
        self._frame = Frame(self.master)
        self._frame.pack()

        self._canvas_mesa = Canvas(self._frame, width=self.width, height=self.height, bg="green")
        self._canvas_mesa.pack(side='left')

    def criar_popup(self):
        self._popup = Toplevel(self.master)
        return self._popup

    def destruir_popup(self):
        self._popup.destroy()
