import socket
import sys
import threading
import time

def resposta_thread():
    ativo = True
    print("Resposta Thread iniciou")
    while ativo:
        msg = soc.recv(1024).decode()
        if  msg == "OK":
            ativo = False
            print(msg)
    print("Resposta Thread finalizou") 

def crud_thread():
    ativo = True
    print("Crud Thread iniciou.")#
    while ativo:
        mensagem = ""
        while mensagem != 'sair':
            mensagem = input("entre com o comando: ")
            print(validar_comando(mensagem))
            if validar_comando(mensagem):
                soc.send(mensagem.encode("utf8"))
                r = threading.Thread(target=resposta_thread)
                r.start()
                r.join()
            else:
                print("Comando não reconhecido")
        soc.send(b'sair')
        ativo = False
    print("Crud Thread finalizou.")#


def validar_comando(mensagem):
    str(mensagem).upper()
    msg = mensagem.split(' ', 1)
    #if "SAIR" in msg:
    opcoes = ["SAIR", "INSERT", "DELETE", "UPDATE"]
    if msg[0] in opcoes:
        return True
    else:
        return False
        
        

soc = socket.socket()
host = socket.gethostname()
port = 12344
soc.connect((host, port))
try:
   c = threading.Thread(target=crud_thread)
   c.start()
   c.join()
except:
    print("Erro ao iniciar Thread")
    soc.close()