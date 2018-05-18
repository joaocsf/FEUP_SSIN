import pickle

class Serializable:
    def serialize(self):
        return pickle.dumps(self)

class HostData(Serializable):
    def __init__ (self, port, publicKey):
        self.port = port
        self.publicKey = publicKey

class RouteRequest(Serializable): pass

class Layer(Serializable):
    def __init__ (self, hop, message):
        self.hop = hop
        self.message = message

class Onion(Serializable):
    def __init__ (self):
        self.layers = []
    
def split(str, num):
  return [ str[start:start+num] for start in range(0, len(str), num)]