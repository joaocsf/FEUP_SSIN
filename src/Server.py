import socket
import pickle
from Shared import HostData

TCP_IP = '127.0.0.1'
TCP_PORT = 5010
BUFFER_SIZE = 10000000
MESSAGE = "Potatos"
MAX_CONN = 10


class Server:
    def __init__ (self, ip, port, bufferSize, maxConn):
        self.TCP_IP = ip
        self.TCP_PORT = port
        self.BUFFER_SIZE = bufferSize
        self.MAX_CONN = maxConn
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.TCP_IP, self.TCP_PORT))
        self.socket.listen(self.MAX_CONN)
    
    def InitializeServer(self):
        while(1):
            print("Router Accepting Connections")
            (clientSocket, addr) = self.socket.accept()

            while True:
                data = clientSocket.recv(BUFFER_SIZE)
                if not data: break
                print("Received", data)
                clientSocket.send("Secret Information".encode())
            
            clientSocket.close()

router = Server(TCP_IP, TCP_PORT, BUFFER_SIZE, MAX_CONN)
router.InitializeServer()