class Fila(object):
    def __init__(self):
        self.dados = []

    def insere(self, elemento):
        self.dados.append(elemento)

    def retira(self):
        if not self.vazia():
            return self.dados.pop(0)

    def vazia(self):
        return len(self.dados) == 0