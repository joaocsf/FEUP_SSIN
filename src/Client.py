import socket
import pickle
from Shared import HostData

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024
MESSAGE = "Potatos"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
data = HostData(5005)
s.connect((TCP_IP, TCP_PORT))
s.send(data.serialize())
data = s.recv(BUFFER_SIZE)
data = pickle.loads(data)
print(data.port)
s.close()
