from utils.Response import Response
from utils.Parser import Parser
from utils.Response import Response
import inspect

class HodgePodge():
    def __init__(self):
        self.modules = []
        self.parser = Parser()

    def attachModule(self, m):
        self.modules.append(m)
        m.connectParser(self.parser)
        self.flushModule(m)

    # ok now i admit. this is a hacky way to do this **BUT**
    # unless someone else makes a function called wrapped_f
    # i should be safe....
    def flushModule(self, m):
        for member in inspect.getmembers(m):
            if inspect.ismethod(member[1]):
                if member[1].__name__ == "wrapped_f":
                    member[1].__call__()

    def processRequest(response, request):
        pass

    def talk(self, message, roles, locationId):
        # Doesn't handle any clashes, overrides.
        match = self.parser.parse(message,roles,locationId)
        if not match:
            return None
        r = match.trigger()
        response = r[0]
        if r[1]:
            self.processRequest(response, r[1])
        return response
