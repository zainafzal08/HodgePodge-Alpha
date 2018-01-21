from ../tools/Db import Db
from ../tools/Parser import Parser
from ../tools/Formatter import Formatter


class HodgePodge():
    def __init__(self, client):
        self.superAdmins = ["330337388196790284","182968035819126784"]
        self.db = Db()
        self.parser = Parser()
        self.client = client
        # Modules
        self.modules = []
        self.modules.append(Game())
        # Init Modules
        for module in self.modules:
            module.connectDb(self.db)
            for trigger in module.getTriggerList():
                self.parser.register(module, trigger)


    def accessLevel(person):
        roles = list(map(lambda x: x.name, person.roles))
        if person.id in self.superAdmins:
            return 2
        elif "Hodge Podge Wrangler" in roles:
            return 1
        else:
            return 0

    def talk(self, message):
        level = self.accessLevel(message.author)
        matches = self.parser.parse(message, level)
        for match in matches:
            match.trigger()
        for match in matches:
            match.respond(self.client)
