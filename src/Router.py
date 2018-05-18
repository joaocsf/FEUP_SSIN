import socket
from Crypto.PublicKey import RSA
from Crypto import Random
import pickle
import sys
from Shared import HostData, split

TCP_IP = '127.0.0.1'
TCP_PORT = 5007
BUFFER_SIZE = 10000000
MESSAGE = "Potatos"
MAX_CONN = 10

TCP_PORT = int(sys.argv[1])

class Router:
    def __init__ (self, ip, port, bufferSize, maxConn, serverData):
        self.TCP_IP = ip
        self.TCP_PORT = port
        self.BUFFER_SIZE = bufferSize
        self.MAX_CONN = maxConn
        self.initializeRSA()
        self.ConnectToDirectory(serverData)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.TCP_IP, self.TCP_PORT))
        self.socket.listen(self.MAX_CONN)
    
    def initializeRSA(self):
        random_gen = Random.new().read
        self.key = RSA.generate(2048)
        self.publicKey = self.key.publickey()

    def ConnectToDirectory(self, serverData):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        publicKeyExported = self.publicKey.exportKey()
        data = HostData(self.TCP_PORT, publicKeyExported)
        server.connect(serverData)
        server.send(data.serialize())
        result = server.recv(BUFFER_SIZE)
        server.close()
    
    def parseMsg(self, data, addr):
        obj = pickle.loads(data)

        types = {
            'Layer' : self.handleLayer,
         }

        func = types.get(type(obj).__name__, "unknownClass") 
        return func(obj, addr)
    
    def handleLayer(self, layer, addr):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        message = []
        if isinstance(layer.message, list):
            for chunk in layer.message:
                decryptedChunk = self.key.decrypt(chunk)
                message.append(decryptedChunk)
        
        message = b''.join(message)
        hiddenLayer = pickle.loads(message)
        lastMSG = not isinstance(hiddenLayer.message, list)
        nextHop = hiddenLayer.hop
        if nextHop:
            print("Received Message from:", addr, " Sending to:", nextHop, " Content:", hiddenLayer.message)
            s.connect(nextHop)
            message = hiddenLayer.serialize() if not lastMSG else hiddenLayer.message.encode()
            s.send(message)
            response = s.recv(self.BUFFER_SIZE)
            response = self.key.encrypt(response, 128)
            return response[0]

    def InitializeServer(self):
        while(1):
            print("Router Accepting Connections")
            (clientSocket, addr) = self.socket.accept()

            while True:
                data = clientSocket.recv(BUFFER_SIZE)
                if not data: break
                result = self.parseMsg(data, addr)
                if not result: break
                clientSocket.send(result)
            
            clientSocket.close()

router = Router(TCP_IP, TCP_PORT, BUFFER_SIZE, MAX_CONN, ('127.0.0.1', 5005))
router.InitializeServer()