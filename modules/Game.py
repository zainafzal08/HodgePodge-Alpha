from modules.Module import Module
import re
import random
from discord.utils import find

class Game(Module):
    def __init__(self, db, client, parser, formatter):
        super().__init__("Game")
        self.parser = parser
        self.formatter = formatter
        self.db = db
        self.scoreEditLevel = 0
        self.registerCommands()

    def registerCommands(self):
        self.parser.register({
            "trigger":"hodge podge roll a d\d+\s*$",
            "function":self.roll,
            "accessLevel": 0
            })
        self.parser.register({
            "trigger": "hodge podge roll \d+ d\d+s?\ss*$",
            "function": self.multiRoll,
            "accessLevel": 0
            })
        self.parser.register({
            "trigger": "hodge podge give .* \d+ .* points?\s*$",
            "function": self.editPoints,
            "accessLevel": self.scoreEditLevel
            })
        self.parser.register({
            "trigger": "hodge podge take \d+ .* points? from .*\s*$",
            "function": self.editPoints,
            "accessLevel": self.scoreEditLevel
            })
        self.parser.register({
            "trigger": "hodge podge list all score types\s*$",
            "function": self.listPoints,
            "accessLevel": self.scoreEditLevel
            })
        self.parser.register({
            "trigger": "hodge podge summerise .* points?\s*$",
            "function": self.getPoints,
            "accessLevel": self.scoreEditLevel
            })

    def multiRoll(self, trigger):
        args = trigger["args"]
        count = int(args[0])
        d = int(args[1])
        if d > 1000 or count > 100:
            self.formatter.error("Sorry friend! That number is too big")
        else:
            roll = 0
            components = []
            for i in range(count):
                r = random.randint(1,d)
                roll += r
                components.append(str(r))
            roll = str(roll)
            self.formatter.output("I got %s! (%s)"%(roll,"+".join(components)))

    def roll(self, trigger):
        args = trigger["args"]
        d = int(args[0])
        if d > 1000:
            self.formatter.output("Sorry friend! That number is too big")
        else:
            roll = str(random.randint(1,d))
            self.formatter.output("It landed on %s!"%roll)

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
            self.formatter.error("Sorry! I don't know who to target! Did you make sure to use a valid `@` mention?")
        else:
            new = self.db.scoreEdit(message.channel.id, scoreType, person.id, score)
            self.formatter.output("%s now has %d points!"%(person.name,new))

    def listPoints(self, trigger):
        args = trigger["args"]
        l = self.db.scoreListTypes(message.channel.id)
        if len(l) == 0:
            self.formatter.error("I'm not keeping track of any points yet!")
        else:
            self.formatter.output("Here's all the score types i'm keeping track off!")
            self.formatter.list(l)

    def getPoints(self, trigger):
        args = trigger["args"]
        scoreType = args[0].lower() #TODO: Make sure we don't need a shallow clean here
        l = self.db.getAllScores(message.channel.id, scoreType)
        server = message.channel.server
        if len(l) == 0:
            self.formatter.error("Nobody has any points yet!")
        else:
            self.formatter.output("Here's all the %s scores!"%scoreType)
            l = list(map(lambda x: x[0] = find(lambda m: m.id == x[0], server.members).name))
            self.formatter.list(l)
