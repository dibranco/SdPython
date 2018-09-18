class Banco(object):
    def __init__(self):
        self.dicionario = []
        
    def create(self, chave, valor):
        try:
            self.dicionario.append([chave, valor]) #inclui (chave, valor) no mapa
            return True
        except:
            print("ERROR")
            return False
        
    def recovery(self, chave):
        for ind in range(len(self.dicionario)-1):
            if chave == self.dicionario[ind][0]:
                return self.dicionario[ind][1]
        return None
    
    def update(self, chave, novoValor):
        for ind in range(len(self.dicionario)-1):
            if chave == self.dicionario[ind][0]:
                self.dicionario[ind][1] = novoValor
                return True
        return False

    def delete(self, chave):
        for ind in range(len(self.dicionario)-1):
            if chave == self.dicionario[ind][0]:
                del(self.dicionario[ind])
                return True
        return False 
    
#def main():
#    A = Banco()
#    print(A)
#    A.create(104,87641874)
#    A.create(543,87398478)
#    A.create(456,93287823)
#    A.create(789,91473299)
#    
#    y = A.recovery(543)
#    print(y)
#    
#    print(A.dicionario)
#    A.update( 104, 9090)
#    A.update( 543, 999999)
#    print(A.dicionario)
#    A.delete(104)
#    print(A.dicionario)
#main()
