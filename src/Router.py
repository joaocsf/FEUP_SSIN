import socket
import pickle
import sys
from Shared import HostData

TCP_IP = '127.0.0.1'
TCP_PORT = 5007
BUFFER_SIZE = 2048
MESSAGE = "Potatos"
MAX_CONN = 10

TCP_PORT = int(sys.argv[1])

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
            'Onion' : self.handleOnion,
         }

        func = types.get(type(obj).__name__, "unknownClass") 
        return func(obj, addr)
    
    def handleOnion(self, onion, addr):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        nextHop = onion.popNextHop()
        if nextHop:
            print("Received Message from:", addr, " Sending to:", nextHop)
            s.connect(nextHop)
            message = onion.message.encode() if onion.last() else onion.serialize()
            if len(onion.route) == 0: print("Last Hop Message:", message)
            s.send(message)

            response = s.recv(self.BUFFER_SIZE)
            return response


    
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