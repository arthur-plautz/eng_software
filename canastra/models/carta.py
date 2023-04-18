from PIL import Image, ImageTk


class Carta:
    def __init__(self, naipe, valor):
        self.naipe = naipe
        self.valor = valor
        self.caminho_imagem = f"cartas/{valor}_of_{naipe.lower()}.png"
        self.imagem = Image.open(self.caminho_imagem)
        self.imagem = self.imagem.resize((80, 120))
        self.photo = ImageTk.PhotoImage(self.imagem)
        
    
    def __str__(self):
        return f"{self.valor} of {self.naipe}"
