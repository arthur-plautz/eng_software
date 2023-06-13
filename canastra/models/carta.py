from PIL import Image, ImageTk

class Carta:
    def __init__(self, naipe, valor):
        self.naipe = naipe
        self.valor = valor
        self.caminho_imagem = f"cartas/{valor}_{naipe.lower()}.png"

    @property
    def imagem(self):
        imagem = Image.open(self.caminho_imagem)
        imagem = imagem.resize((80, 120))
        return ImageTk.PhotoImage(imagem)

    @property
    def descricao(self):
        return f"{self.valor} de {self.naipe}"

    @property
    def serializacao(self):
        return dict(
            naipe=self.naipe,
            valor=self.valor
        )
