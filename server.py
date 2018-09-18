import socket
import sys
import traceback
from threading import Thread
import fila
import banco

def main():
    abrir_conexao()

def abrir_conexao():
    soc = socket.socket()
    host = socket.gethostname()
    port = 12344
    try:
        soc.bind((host, port))
    except:
        print("Erro bind")
        
    soc.listen(5)
    print("Socket now listening")
    #abrir arquivo de log e ler os comandos antes de iniciar novas requisicoes
    start_server(soc)

def start_server(soc):
    f1 = fila.Fila()
    f2 = fila.Fila()
    f3 = fila.Fila()

    while True:
        connection, address = soc.accept()
        print("Conectado com: " + str(address[0]) + ":" + str(address[1]))
        try:
            Thread(target=client_thread, args=(connection, address, f1, f2, f3)).start()
        except:
            print("client_tread não iniciou.")
            traceback.print_exc()
    soc.close()

def duplica_thread(connection, f1, f2, f3):
    is_active = True
    print("thread duplica iniciou")
    while is_active:
        while not f1.vazia():
            comando = f1.retira()
            f2.insere(comando)
            try:
                Thread(target=log_thread, args=(connection, f2)).start()
                Thread(target=database_thread, args=(connection, f3)).start()                
            except:
                print("log_thread não iniciou.")
                traceback.print_exc()
        is_active = False
    print("thread duplica finalizou")
    
def log_thread(connection, f2):
    is_active = True
    print("thread log iniciou")
    file = open("log.txt","a")
    while is_active:
        while not f2.vazia():
            print("gravando...")
            cm = str(f2.retira())
            if "READ" not in cm:
                file.writelines(cm + "\n")
                connection.sendall("OK".encode("utf8")) #mover para thread de processamento
        is_active = False
    file.close()
    print("thread log finalizou")

def database_thread(connection, f3):
    is_active = True
    print("Thread Database iniciou")
    while is_active:
        while not f3.vazia():
            print("gravando Banco de dados")
            cm = str(f3.retira())
            

def client_thread(connection, address, f1, f2, f3):
    is_active = True

    while is_active:
        client_input = receive_input(connection)
        
        if "SAIR" in client_input:
            connection.close()
            print("Connection " + str(address[0]) + ":" + str(address[1]) + " closed")
            is_active = False
        #separar em defs
        else:
            comandos(client_input, connection, address,f1,f2,f3)
 
def comandos(client_input, connection, address, f1, f2, f3):
    print(f1.vazia())
    f1.insere(client_input)
    try:
        Thread(target=duplica_thread, args=(connection,f1, f2 ,f3)).start()
    except:
        print("Thread did not start.")
        traceback.print_exc()
    print("Insert: {}".format(f1.dados))
    
            
def receive_input(connection):
    client_input = connection.recv(1024)

    decoded_input = client_input.decode("utf8").rstrip()
    result = process_input(decoded_input)

    return result

def process_input(input_str):
    return str(input_str).upper()

main()