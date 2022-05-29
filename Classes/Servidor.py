import socket
import os
from tqdm import tqdm

class Server:
    def __init__(self):
        self.connectionOpen = False
        self.connection = ''
        self.clientAddr = ''
        self.address = ''
    
    def close(self):
        self.connection.close()
    def listening(self, port, ip = ''):
        """
            Creates a socket tcp IPV4
            ip: IP which will connect this server
                (default '')
            port: port to listen to

            self.connection receives connection
            self.clientAddr receives the cliente address
        """
        self.address = (ip, port)
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(self.address)
        
        print(f"\nServer is listening on {ip}:{port}")
        server.listen()

        conn, addr = server.accept()    

        print(f"\nClient connected: {addr}")
        self.connectionOpen = True

        self.connection = conn
        self.clientAddr = addr

    def sendData(self, data, size = 1024, format='utf-8',binary = False):
        """
            Send data to the client, return the client answer
            data: data to be sended
            format: data format (default utf-8)
            size: size of the packet (default 1024)
        """
        if not self.connectionOpen:
            print("\nNo client connected")
            return 
        else:
            self.connection.send(data)    
            resp = self.connection.recv(size) 
            return resp
               

    def sendFile(self, filePath, format = "utf-8", packetSize = 1024):
        
        file = open(filePath, 'rb')
        fileSize = os.path.getsize(filePath)
        self.sendData(f"{filePath}@{fileSize}".encode('utf-8'))
        bar = tqdm(range(fileSize), f"Sending {filePath}", unit="B", unit_scale=True, unit_divisor=packetSize)
       
        while True:
            data = file.read(packetSize)

            if not data:
                break

            self.sendData(data)
            bar.update(packetSize)
        self.sendData("Envio_Completo".encode('utf-8'))
    