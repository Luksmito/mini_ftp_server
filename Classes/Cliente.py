import os
import socket
from tqdm import tqdm
import platform

SO = platform.system()

def invertString(string):
    """return the inverse of the string passed"""
    auxStr = list(string)
    aux = ['']
    i = 0
    j = len(string) - 1
    while i < j:
        aux[0] =  auxStr[i]
        auxStr[i] = auxStr[j]
        auxStr[j] = aux[0]
        j -= 1
        i += 1
    string = ''.join(auxStr)
    return string

class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connectedToAServer = False
    
    def close(self):
        self.client.close()
        
    def connectServer(self, ip, port):    
        """
        Connect to a server
        ip: ip of the server to connect
        port: port to connect
        """
        addr = (ip, port)
        
        self.client.connect(addr)

        print(f"\nConnected to {addr}")

        self.connectedToAServer = True

    def receiveData(self, size=1024):
        """
        Wait server send some data then return it
        size: packet's size (default 1024)
        format: the format to enconding (default utf-8)
        binary: if the data need to be encoded before returning (default False)
        """
        if not self.connectedToAServer:
            print("No connection")
            return
        else:
           
            data = self.client.recv(size)
            self.client.send(data)
            return data
    
    def receiveDirClone(self, binary = False):
        """
        Receives a clone of the dir wheres the server is running
        binary: if the data of the files need to be encoded before writed (default False)
        """
        fileInfo = self.receiveData()
        if SO == "Linux":
            teste = fileInfo[0].split('/')
        elif SO == "Windows":   
            teste = fileInfo[0].split('\\')
        
        if len(teste) > 2:
            arq = ''
            i = len(fileInfo[0]) - 1
            if SO == "Linux":
                while fileInfo[0][i] != '/':
                    arq += fileInfo[0][i]
                    fileInfo[0] = fileInfo[0][0:i]
                    i = i - 1
            elif SO == "Windows":
                while fileInfo[0][i] != '\\':
                    arq += fileInfo[0][i]
                    fileInfo[0] = fileInfo[0][0:i]
                    i = i - 1
            os.makedirs(fileInfo[0])
            arq = arq[-1:]
            arq = fileInfo[0]  + arq
        else:
            arq = fileInfo[0]
        
        if binary:
            with open(f"{arq}", "wb") as file:
                    
                while True:
                    data = self.receiveData(1024, binary = True)

                    if data == "Envio_Completo":
                        break

                    file.write(data)
        else:
             with open(f"{arq}", "w") as file:
                    
                while True:
                    data = self.receiveData(1024)

                    if data == "Envio_Completo":
                        break

                    file.write(data)
            
    def receiveFile(self, size = 1024):
        """
        Receives a file from the server class
        size: size of each packet (default 1024)
        binary: if the data of the file need to be encoded before writed (default False)
        format: format to be encoded
        """
        fileInfo = self.receiveData().decode('utf-8').split("@")
        fileSize = int(fileInfo[1])
        if SO == "Linux":
            fileInfo[0] = fileInfo[0].replace('\\', '/')
            test = fileInfo[0].split('/')
        elif SO == "Windows":
            test = fileInfo[0].split('\\')

        if len(test) > 2:
            arq = ''
            i = len(fileInfo[0]) - 1
            if SO == "Linux":
                while fileInfo[0][i] != '/':
                    arq += fileInfo[0][i]
                    fileInfo[0] = fileInfo[0][0:i]
                    i = i - 1
            elif SO == "Windows":
                while fileInfo[0][i] != '\\':
                    arq += fileInfo[0][i]
                    fileInfo[0] = fileInfo[0][0:i]
                    i = i - 1
            os.makedirs(fileInfo[0], exist_ok=True)
            arq = invertString(arq)
            arq = fileInfo[0] + arq
        else:
            arq = fileInfo[0]
        
        if arq == '':
            return
        bar = tqdm(range(fileSize), f"Receiving {arq}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(f"{arq}", "wb") as file:
            
            while True:
                data = self.receiveData(size)

                if data == b"Envio_Completo":
                    break

                file.write(data)
                bar.update(size)
       