import pickle

class Serializable:
    def serialize(self):
        return pickle.dumps(self)

class HostData(Serializable):
    def __init__ (self, port):
        self.port = port