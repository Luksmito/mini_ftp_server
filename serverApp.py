import sys
import os
sys.path.append(".\\Classes")
import Servidor as sr
import Cliente as cl
import platform

SO = platform.system()

def separaDir(caminho):
    i = len(caminho) - 1
    if SO == 'Linux':
        while caminho[i] != '/':
            caminho = caminho[0:i]
            i = i - 1
    elif SO == 'Windows':
        while caminho[i] != '\\':
            caminho = caminho[0:i]
            i = i - 1
    
    return caminho


def criaDir(listaDir):
    caminhos = []
    for i in listaDir:
        i = separaDir(i)
        if SO == 'Linux':
            caminhos.append(i.split('/'))
        elif SO == 'Windows':
            caminhos.append(i.split('\\'))
    for i in caminhos:
        texto = ''
        for j in i:
            if SO == 'Linux':
                texto += j + '/'
            elif SO == 'Windows':
                texto += j + '\\'
        os.makedirs(texto, exist_ok=True)


    


def listaDiretorio():
    arquivos = []
    for i in os.walk("."):
        for j in i[2]:
            if SO == 'Linux':
                caminho = i[0] + "/" + j 
            elif SO == 'Windows':
                caminho = i[0] + "\\" + j  
            arquivos.append(caminho)
    return arquivos
    
def enviarArquivo(server):
    arquivo = input("Digite o caminho para o arquivo: ")
    server.sendFile(arquivo)


def recebeCloneDir(client):
    tam = int(client.receiveData())

    for i in range(tam):
        client.receiveFile()

def enviarCloneDir(server):
    arquivos = listaDiretorio()
    if SO == 'Linux':
        arquivos.remove('./serverApp.py')
    elif SO == 'Windows':
        arquivos.remove('.\\serverApp.py')
    print(arquivos)
    server.sendData(str(len(arquivos)).encode('utf-8'))

    for arquivo in arquivos:
        server.sendFile(arquivo)

def teste():
    enviarCloneDir(1)
def main():
    debug = True
    while True:
        print("\t\tAplicacao socket local\n\t\tDeseja 1 - abrir uma conexao ou 2 - se conectar?\n\n")
        option = int(input())
        if option == 1:
            server = sr.Server()
            if not debug:
                server.listening(int(input("Em qual porta deseja abrir?: ")))
            else:
                server.listening(55555)
            print("Operações possiveis para o servidor:")
            option = int(input("\n\t\t1 - Enviar arquivo\n\t\t2 - Clonar esse diretorio\n\t\t3 - Criar Chat\n\t\t"))
            
            operacoes = {1: enviarArquivo, 2: enviarCloneDir}
            
            operacoes[option](server)
            server.close()

        elif option == 2:
            client = cl.Client()
            if not debug:
                endereco = input("Digite o endereco ipv4 da conexao: ")
                endereco = endereco.split(':')
                client.connectServer(endereco[0], int(endereco[1]))
            else:
                client.connectServer('localhost', 55555)

            print("Operações possiveis para o servidor:")
            option = int(input("\n\t\t1 - Receber arquivo\n\t\t2 - Receber clone de um diretorio\n\t\t3 - Criar Chat\n\t\t"))
            options = {1: client.receiveFile, 2: recebeCloneDir}
            options[option](client)
        elif option == 3:
            print("Nao implementado")
if __name__ == "__main__":
    main()
    #teste()