from modules.Module import Module
import re
import random
from discord.utils import find

class Game(Module):
    def __init__(self):
        super().__init__("Game")
        self.scoreEditLevel = 0
        self.registerCommands()

    def registerCommands(self):
        parser.register({
            "trigger":"hodge podge roll a d\d+\s*$",
            "function":self.roll,
            "accessLevel": 0
            })
        parser.register({
            "trigger": "hodge podge roll \d+ d\d+s?\ss*$",
            "function": self.multiRoll,
            "accessLevel": 0
            })
        parser.register({
            "trigger": "hodge podge give .* \d+ .* points?\s*$",
            "function": self.editPoints,
            "accessLevel": self.scoreEditLevel
            })
        parser.register({
            "trigger": "hodge podge take \d+ .* points? from .*\s*$",
            "function": self.editPoints,
            "accessLevel": self.scoreEditLevel
            })
        parser.register({
            "trigger": "hodge podge list all score types\s*$",
            "function": self.listPoints,
            "accessLevel": self.scoreEditLevel
            })
        parser.register({
            "trigger": "hodge podge summerise .* points?\s*$",
            "function": self.getPoints,
            "accessLevel": self.scoreEditLevel
            })

    def generateDbRequest():

    def multiRoll(self, trigger):
        args = trigger["args"]
        count = int(args[0])
        d = int(args[1])
        if d > 1000 or count > 100:
            formatter.error("Sorry friend! That number is too big")
            return
        roll = 0
        components = []
        for i in range(count):
            r = random.randint(1,d)
            roll += r
            components.append(str(r))
        formatter.output("I got %d! (%s)"%(roll,"+".join(components)))

    def roll(self, trigger):
        args = trigger["args"]
        d = int(args[0])
        if d > 1000:
            formatter.output("Sorry friend! That number is too big")
        else:
            roll = str(random.randint(1,d))
            formatter.output("It landed on %s!"%roll)

    def editPoints(self, trigger):
        args = trigger["args"]
        match = trigger["match"]

        if match == 0:
            s = s1
            score = int(args[1])
            scoreType = args[2].lower()
        else:
            s = s2
            score = int(args[0])*-1
            scoreType = args[1].lower()

        person = None
        if len(message.mentions) > 0:
            person = message.mentions[0]
        if not person:
            formatter.error("Sorry! I don't know who to target! Did you make sure to use a valid `@` mention?")
        else:
            request = {
                "TABLE": "SCORES"
                "SET": ["SCORE"],
                "VALUE": [score],
                "WHERE": {
                    "CHANNEL": message.channel.id,
                    "TYPE": scoreType,
                    "PERSON": person.id
                },
                "RETURN": "NEW",
                "FORCE": True
            }
            new = db.edit(request)
            formatter.output("%s now has %d points!"%(person.name,new))

    def listPoints(self, trigger):
        request = {
            "TABLE": "SCORES",
            "GET": ["TYPE"],
            "WHERE": {
                "CHANNEL" : message.channel.id
            },
            "DUP": False
        }
        l = db.get(request)
        if len(l) == 0:
            formatter.error("I'm not keeping track of any points yet!")
        else:
            formatter.output("Here's all the score types i'm keeping track off!")
            formatter.list(l)

    def getPoints(self, trigger):
        args = trigger["args"]
        scoreType = args[0]
        request = {
            "TABLE": "SCORES",
            "GET": ["PERSON","SCORE"],
            "WHERE": {
                "CHANNEL" : message.channel.id,
                "TYPE": scoreType
            },
            "DUP": False
        }
        l = self.db.get(request)
        server = message.channel.server
        if len(l) == 0:
            formatter.error("Nobody has any points yet!")
        else:
            formatter.output("Here's all the %s scores!"%scoreType)
            l = list(map(lambda x: x[0] = find(lambda m: m.id == x[0], server.members).name))
            formatter.list(l)
