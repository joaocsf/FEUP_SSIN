import pickle

class Serializable:
    def serialize(self):
        return pickle.dumps(self)

class HostData(Serializable):
    def __init__ (self, port):
        self.port = port

class RouteRequest(Serializable): pass

class Onion(Serializable):
    def __init__ (self, route, message):
        self.route = route
        self. message = message
    
    def popNextHop(self):
        if len(self.route) == 0:
            return False
        return self.route.pop(0)
    
    def last(self):
        return len(self.route) == 0
    