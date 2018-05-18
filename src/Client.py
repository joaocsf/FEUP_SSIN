import socket
from Crypto.PublicKey import RSA
from base64 import b64decode
from Crypto.Cipher import PKCS1_OAEP
import pickle
from pprint import pprint 
from Shared import HostData, RouteRequest, Onion, Layer, split

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 10000000
MESSAGE = "Potatos"

class Client: 
  def __init__(self, directorydata=('127.0.0.1',5005), bufferSize = BUFFER_SIZE):
    self.directoryData = directorydata
    self.BUFFER_SIZE = bufferSize

  def sendMessage(self, serverData, message):
    servers = self.retrieveDirectoryRoute()

    route = [(e[0],e[1]) for e in servers]

    baseLayer = Layer(serverData, message)

    for server in servers[::-1]:
      key = RSA.importKey(server[2])
      chunks = split(baseLayer.serialize(), 128)
      serialized = []
      for chunk in chunks:
        encryptedChunk = key.encrypt(chunk, 128)
        serialized.append(encryptedChunk)

      newLayer = Layer((server[0],server[1]), serialized)
      baseLayer = newLayer

    print(baseLayer.serialize())
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    nextHop = baseLayer.hop

    if nextHop:
      print("Next Hop", nextHop)
      s.connect(nextHop)
      s.send(baseLayer.serialize())

      response = s.recv(self.BUFFER_SIZE)

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

