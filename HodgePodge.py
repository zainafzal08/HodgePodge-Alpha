from utils.Response import Response
from utils.Parser import Parser

class HodgePodge():
    def __init__(self):
        self.modules = []
        self.parser = Parser()
    def attachModule(self, m):
        self.modules.append(m)
        m.connectParser(self.parser)

    # the message as a string
    # the level of the user
    # the location id of the sent message
    def talk(self, message, level, locationId):
        r = Response()
        r.textResponce("I'm Hodge Podge!",locationId)
        self.modules[0].roll()
        return r
