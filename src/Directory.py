import socket
import pickle
from Shared import HostData

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024
MAX_CONN = 1

class Directory:

  def __init__ (self, ip, port, bufferSize, maxConn):
    self.TCP_IP = ip
    self.TCP_PORT = port
    self.BUFFER_SIZE = bufferSize
    self.MAX_CONN = maxConn
    self.routers = set()
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.bind((self.TCP_IP, self.TCP_PORT))
    self.socket.listen(self.MAX_CONN)
    print("Directory Initialized", flush=True)

  def parseMsg (self, data, addr):
    obj = pickle.loads(data)
    
    types = {
      'HostData' : self.handleHostRequest
    }

    func = types.get(type(obj).__name__, "unknownClass")
    func(obj, addr)
  
  def handleHostRequest(self, hostData, addr):
      print("Obj Found", hostData.port, flush=True)
      entry = (addr[0], hostData.port)
      self.routers.add(entry)
      print("Added Router Entry", entry, flush=True)
      print("Total Entries: ", len(self.routers), flush=True)

  def accept(self):
    while(True):
      (clientSocket , addr) = self.socket.accept()

      while True:
        data = clientSocket.recv(BUFFER_SIZE)
        if not data: break
        result = self.parseMsg(data, addr)
        clientSocket.send(result)
      
      clientSocket.close()

d = Directory(TCP_IP, TCP_PORT, BUFFER_SIZE, MAX_CONN)
d.accept()