from modules.Module import Module
import re
import random
from discord.utils import find

class Game(Module):
    def __init__(self):
        super().__init__("Game")
        self.scoreEditLevel = 0
        self.triggerList = []
        self.db = None
        self.formatter = Formatter()
        self.triggerList.append({
            "trigger":"hodge podge roll a (d\d+)\s*$",
            "function":self.roll,
            "accessLevel": 0
            })
        self.triggerList.append({
            "trigger": "hodge podge roll (\d+) (d\d)+s?\ss*$",
            "function": self.multiRoll,
            "accessLevel": 0
            })
        self.triggerList.append({
            "trigger": "hodge podge give (.*) (\d+) (.*) points?\s*$",
            "function": self.editPoints,
            "accessLevel": self.scoreEditLevel,
            "id": 0
            })
        self.triggerList.append({
            "trigger": "hodge podge take (\d+) (.*) points? from (.*)\s*$",
            "function": self.editPoints,
            "accessLevel": self.scoreEditLevel,
            "id": 1
            })
        self.triggerList.append({
            "trigger": "hodge podge list all score types\s*$",
            "function": self.listPoints,
            "accessLevel": self.scoreEditLevel
            })
        self.triggerList.append({
            "trigger": "hodge podge summerise (.*) points?\s*$",
            "function": self.getPoints,
            "accessLevel": self.scoreEditLevel
            })

    def connectDb(self, db):
        self.db = db

    def getTriggerList(self):
        return triggerList

    def respond(self, client, channel):
        if client:
            self.formatter.flush(client, channel)
        else:
            self.formatter.consoleFlush()
    def getHelp(self):
        res = []
        res.append(("hodge podge roll a d<X>","Have hodge podge roll a dice! supports d1 to d1000","hodge podge roll a d20"))
        res.append(("hodge podge roll <Y> d<X>s","Have hodge podge roll a dice Y times! supports up to 1000 d1000","hodge podge roll 3 d8's"))
        res.append(("hodge podge give <U> <X> <T> points","Gives a user <U> (should be a @ tag) <X> points of <T>","hodge podge give @AAA 10 xp points"))
        res.append(("hodge podge take <X> <T> points from <U>","Same as above but substracts points","hodge podge take 10 xp points from @AAA"))
        res.append(("hodge podge list all score points","List all score types (such as xp or goof points) in the current channel",None))
        res.append(("hodge podge summerise <T> points","List all users and their scores (if they have scores) for score type <T>","hodge podge summerise xp points"))
        obj = {}
        obj["cmds"] = res
        # TODO: put in docs
        obj["docs"] = "lol whoops"

    def multiRoll(self, trigger):
        # TODO: get the nice formatted output from master
        args = trigger["args"]
        count = int(args[0])
        d = int(args[1])
        if d > 1000 or count > 1000:
            self.formatter.error("Sorry friend! That number is too big")
            return
        roll = 0
        components = []
        for i in range(count):
            r = random.randint(1,d)
            roll += r
            components.append(str(r))
        self.formatter.output("I got %d! (%s)"%(roll,"+".join(components)))

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
            l = list(map(lambda x: x[0] = find(lambda m: m.id == x[0], server.members).name))
            self.formatter.list(l)
