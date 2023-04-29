from tkinter import *

class Mesa:
    def __init__(self, master, height, width):
        self.master = master
        self.height = height
        self.width = width

    def _inicia_interface(self):
        self.frame = Frame(self.master)
        self.frame.pack()

        self.canvas_mesa = Canvas(self.frame, width=self.width, height=self.height, bg="green")
        self.canvas_mesa.pack(side='left')

    def cria_popup(self):
        self._popup = Toplevel(self.master)
        return self._popup

    def destroy_popup(self):
        self._popup.destroy()
