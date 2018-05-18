import socket
import pickle
from Shared import HostData, RouteRequest, Onion

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 2048
MESSAGE = "Potatos"

class Client: 
  def __init__(self, directorydata=('127.0.0.1',5005), bufferSize = BUFFER_SIZE):
    self.directoryData = directorydata
    self.BUFFER_SIZE = bufferSize
  
  def sendMessage(self, serverData, message):
    route = self.retrieveDirectoryRoute()
    route.append(serverData)
    onion = Onion(route, message)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    nextHop = onion.popNextHop()
    print(route)
    print(onion.route)
    if nextHop:
      print("Next Hop", nextHop)
      s.connect(nextHop)
      s.send(onion.serialize())

      response = s.recv(self.BUFFER_SIZE)
      print(response)

  def retrieveDirectoryRoute(self):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(self.directoryData)
    s.send(RouteRequest().serialize())

    data = s.recv(self.BUFFER_SIZE)
    data = pickle.loads(data)
    print(data)
    s.close()
    return data

client = Client(bufferSize=BUFFER_SIZE)
client.sendMessage(('127.0.0.1',5010), "Hello There")

