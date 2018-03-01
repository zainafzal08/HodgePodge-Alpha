from bots.HodgePodge.modules.BotModule import BotModule
from utils.Formatter import Formatter
import re
import random
from discord.utils import find

class Game(BotModule):
    def __init__(self):
        super().__init__("Game")
        self.scoreEditLevel = 0
        self.rollLevel = 0
        self.triggerList = []
        self.db = None
        self.formatter = Formatter()
        self.triggerList.append({
            "trigger":"^\s*hodge\s*podge roll a\s*d(\d+)(\s*[\+\-]\s*\d+)?",
            "function":self.roll,
            "accessLevel": self.rollLevel
            })
        self.triggerList.append({
            "trigger": "^\s*hodge\s*podge roll (\d+)\s*d(\d+)s?(\s*[\+\-]\s*\d+)?",
            "function": self.multiRoll,
            "accessLevel": self.rollLevel
            })
        self.triggerList.append({
            "trigger": "^\s*hodge\s*podge give (.*) (\d+) (.*) points?",
            "function": self.editPoints,
            "accessLevel": self.scoreEditLevel,
            "id": 0
            })
        self.triggerList.append({
            "trigger": "^\s*hodge\s*podge take (\d+) (.*) points? from (.*)",
            "function": self.editPoints,
            "accessLevel": self.scoreEditLevel,
            "id": 1
            })
        self.triggerList.append({
            "trigger": "^\s*hodge\s*podge list all score types",
            "function": self.listPoints,
            "accessLevel": self.scoreEditLevel
            })
        self.triggerList.append({
            "trigger": "^\s*hodge\s*podge summerise (.*) points?",
            "function": self.getPoints,
            "accessLevel": self.scoreEditLevel
            })

    def connectDb(self, db):
        self.db = db

    def getTriggerList(self):
        return self.triggerList

    async def respond(self, client, channel):
        if client:
            await self.formatter.flush(client, channel)
        else:
            self.formatter.consoleFlush()

    def getHelp(self):
        obj = {}
        obj["docs"] = "https://github.com/zainafzal08/HodgePodge/blob/dev/bots/HodgePodge/docs/main.md#game"
        obj["raw"] = "https://raw.githubusercontent.com/zainafzal08/HodgePodge/dev/bots/HodgePodge/docs/main.md#game"
        return obj

    def multiRoll(self, trigger):
        args = trigger["args"]
        count = int(args[0])
        d = int(args[1])
        mod = 0
        if args[2] and re.search(r"\+",args[2]):
            mod = int(re.search("(\d+)",args[2]).group(1))
        elif args[2] and re.search(r"\-",args[2]):
            mod = -1*int(re.search("(\d+)",args[2]).group(1))
        if d > 1000 or count > 1000:
            self.formatter.error("Sorry friend! That number is too big")
            return
        elif d < 1 or count < 1:
            self.formatter.error("Sorry friend! That number is too small")
            return
        roll = 0
        components = []
        for i in range(count):
            r = random.randint(1,d)
            roll += r
            components.append(str(r))
        roll += mod
        if len(components) > 100:
            self.formatter.output("You got %d!"%roll)
        else:
            componentString = "+".join(components)
            self.formatter.output("You got %d! (%s)"%(roll,componentString))

    def roll(self, trigger):
        args = trigger["args"]
        d = int(args[0])
        mod = 0
        if args[1] and re.search(r"\+",args[1]):
            mod = int(re.search("(\d+)",args[1]).group(1))
        elif args[1] and re.search(r"\-",args[1]):
            mod = -1*int(re.search("(\d+)",args[1]).group(1))

        if d > 1000:
            self.formatter.output("Sorry friend! That number is too big")
        elif d < 1:
            self.formatter.output("Sorry friend! That number is too small")
        else:
            roll = random.randint(1,d) + mod
            self.formatter.output("You Got %d!"%roll)

    def editPoints(self, trigger):
        args = trigger["args"]
        match = trigger["id"]

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
            request = {
                "TABLE": "SCORES",
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
            new = self.db.edit(request)
            self.formatter.output("%s now has %d points!"%(person.name,new))

    def listPoints(self, trigger):
        request = {
            "TABLE": "SCORES",
            "GET": ["TYPE"],
            "WHERE": {
                "CHANNEL" : message.channel.id
            },
            "DUP": False
        }
        l = self.db.get(request)
        if len(l) == 0:
            self.formatter.error("I'm not keeping track of any points yet!")
        else:
            self.formatter.output("Here's all the score types i'm keeping track off!")
            self.formatter.list(l)

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
            self.formatter.error("Nobody has any points yet!")
        else:
            self.formatter.output("Here's all the %s scores!"%scoreType)
            for i in range(len(l)):
                l[i][0] = find(lambda m: m.id == l[i][0], server.members).name
            self.formatter.list(l)
