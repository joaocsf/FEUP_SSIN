import socket
import pickle
from Shared import HostData

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024
MESSAGE = "Potatos"
MAX_CONN = 10

class Router:
    def __init__ (self, ip, port, bufferSize, maxConn, serverData):
        self.TCP_IP = ip
        self.TCP_PORT = port
        self.BUFFER_SIZE = bufferSize
        self.MAX_CONN = maxConn
        self.ConnectToDirectory(serverData)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.TCP_IP, self.TCP_PORT))
        self.socket.listen(self.MAX_CONN)

    def ConnectToDirectory(self, serverData):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data = HostData(self.TCP_PORT)
        server.connect(serverData)
        server.send(data.serialize())
        result = server.recv(BUFFER_SIZE)
        server.close()
    
    def parseMsg(self, data, addr):
        obj = pickle.loads(data)

        types = {
            'Temp' : self.demoMsg
         }

        func = types.get(type(obj).__name__, "unknownClass") 
        func(obj, addr)
    
    def demoMsg(self, obj, addr):
        print(obj, addr)

    def InitializeServer(self):
        while(1):
            (clientSocket, addr) = self.socket.accept()

            while True:
                data = clientSocket.recv(BUFFER_SIZE)
                if not data: break
                result = self.parseMsg(data, addr)
                clientSocket.send(result)
            
            clientSocket.close()
