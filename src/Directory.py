import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024
MAX_CONN = 1

print("starting directory", flush=True)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(MAX_CONN)

while(True):
  (clientSocket , addr) = s.accept()

  while True:
    data = clientSocket.recv(BUFFER_SIZE)
    if not data: break
    print("received data: ", data.decode(), flush=True)
    clientSocket.send(data)
  
  clientSocket.close()