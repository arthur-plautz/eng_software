from PIL import Image, ImageTk

class Carta:
    def __init__(self, naipe, valor):
        self.naipe = naipe
        self.valor = valor
        self.caminho_imagem = f"cartas/{valor}_of_{naipe.lower()}.png"

    @property
    def imagem(self):
        imagem = Image.open(self.caminho_imagem)
        imagem = imagem.resize((80, 120))
        return ImageTk.PhotoImage(imagem)

    @property
    def descricao(self):
        return f"{self.valor} de {self.naipe}"
