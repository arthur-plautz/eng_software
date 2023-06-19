from PIL import ImageTk, Image

POSICOES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

class Carta:
    def __init__(self, valor, naipe=None):
        self.naipe = naipe
        self.valor = valor
        if self.naipe:
            self.caminho_imagem = f"cartas/{valor}_{naipe.lower()}.png"
        else:
            self.caminho_imagem = f"cartas/{valor.lower()}.png"
        imagem = Image.open(self.caminho_imagem)
        imagem = imagem.resize((80, 120))
        self.imagem = ImageTk.PhotoImage(imagem)
        self.posicao = self._posicao()

    def _posicao(self):
        if self.valor != 'Joker':
            i = POSICOES.index(self.valor)
            return i+1

    def definir_posicao(self, posicao):
        self.posicao = posicao

    @property
    def descricao(self):
        return f"{self.valor} de {self.naipe}"

    @property
    def serializacao(self):
        return dict(
            naipe=self.naipe,
            valor=self.valor
        )

    @property
    def texto(self):
        if self.naipe:
            return f"{self.valor}-{self.naipe}"
        else:
            return self.valor
