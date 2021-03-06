from modules.Module import Module
import re
import random
from random import randint
from discord.utils import find

class Game(Module):
    def __init__(self, db):
        super().__init__("Game")
        self.commands = [
            ("hodge podge roll a d\d+\s*$", self.roll),
            ("hodge podge roll \d+ d\d+s?\s*$", self.multiRoll),
            ("hodge podge give .* \d+ .* points?\s*$", self.editPoints),
            ("hodge podge take \d+ .* points? from .*\s*$", self.editPoints),
            ("hodge podge list all score types\s*$", self.listPoints),
            ("hodge podge summerise .* points?\s*$", self.getPoints),
            ("hodge podge give me a name\s*$", self.getName)
        ]
        self.db = db
        self.scoreEditLevel = 0

    def multiRoll(self, message, level):
        s = re.search(r"hodge podge roll (\d+) d(\d+)s?\s*$",self.clean(message.content))
        count = int(s.group(1))
        d = int(s.group(2))
        res = super().blankRes()
        if d > 1000 or count > 1000:
            res["output"].append("Sorry friend! That number is too big")
        else:
            roll = 0
            components = []
            for i in range(count):
                r = random.randint(1,d)
                roll += r
                components.append(str(r))
            roll = str(roll)
            componentString = "+".join(components)
            if len(components) > 100:
                res["output"].append("I got "+roll+"!")
            else:
                res["output"].append("I got "+roll+"! ("+componentString+")")
        return res

    def roll(self, message, level):
        s = re.search(r"hodge podge roll a d(\d+)\s*$",self.clean(message.content))
        d = int(s.group(1))
        res = super().blankRes()
        if d > 1000:
            res["output"].append("Sorry friend! That number is too big")
        else:
            roll = str(random.randint(1,d))
            res["output"].append("It landed on "+roll+"!")
        return res

    def editPoints(self, message, level):
        if level < self.scoreEditLevel:
            return

        s1 = re.search(r"hodge podge give (.*) (\d+) (.*) points?\s*$",self.clean(message.content))
        s2 = re.search(r"hodge podge take (\d+) (.*) points? from (.*)\s*$",self.clean(message.content))

        if s1:
            s = s1
            score = int(s.group(2))
            scoreType = self.shallowClean(s.group(3))
        elif s2:
            s = s2
            score = int(s.group(1))*-1
            scoreType = self.shallowClean(s.group(2))

        person = None
        if len(message.mentions) != 0:
            person = message.mentions[0]
        res = super().blankRes()

        if not person:
            res["output"].append("Sorry! I don't know who to target! Did you make sure to use a valid `@` mention?")
        else:
            new = self.db.scoreEdit(message.channel.id, scoreType, person.id, score)
            res["output"].append(person.name + " now has "+str(new)+" points!")
        return res

    def getName(self, message, level):
        if level < 0:
            return
        vowels = ["a","e","i","o","u"]
        f = open("words.txt","r")
        raw = f.read()
        f.close()
        l = raw.split("\n")
        w = l[randint(0,len(l)-1)]
        a = randint(0,len(w)-1)
        b = a
        while a == b:
        	b = randint(0,len(w))
        v1 = vowels[randint(0,len(vowels)-1)]
        v2 = vowels[randint(0,len(vowels)-1)]
        w = list(w)
        w.insert(a,v1)
        w.insert(b,v2)
        final = "".join(w)
        res = super().blankRes()
        res["output"].append("Here's one! %s"%final)
        return res
    def listPoints(self, message, level):
        if level < self.scoreEditLevel:
            return
        l = self.db.scoreListTypes(message.channel.id)
        res = super().blankRes()
        result = []
        if len(l) == 0:
            result.append("I'm not keeping track of any points yet!")
        else:
            result.append("Here's all the score types i'm keeping track off!")
            for line in l:
                result.append(":::> **"+line+"**")
        res["output"].append("\n".join(result))
        return res

    def getPoints(self, message, level):
        if level < self.scoreEditLevel:
            return

        s = re.search("hodge podge summerise (.*) points\s*$",self.clean(message.content))
        scoreType = self.shallowClean(s.group(1))
        l = self.db.getAllScores(message.channel.id, scoreType)
        res = super().blankRes()
        result = []
        server = message.channel.server
        if len(l) == 0:
            result.append("Nobody has any points yet!")
        else:
            result.append("Here's all the "+scoreType+" scores!")
            for line in l:
                p = find(lambda m: m.id == line[0], server.members)
                result.append(":::> **"+p.name+"** : "+line[1])
        res["output"].append("\n".join(result))
        return res

    def shallowClean(self, t):
        return t.strip().lower()

    def clean(self, t):
        m = t.lower()
        m = re.sub(r'\s+',' ',m)
        m = re.sub(r'[\,\.\?\;\:\%\#\@\!\^\&\*\+\-\+\_\~\']','',m)
        m = m.strip()
        return m

    def trigger(self, message, requestLevel):
        res = super().blankRes()
        original = message.content;
        m = self.clean(message.content)
        for command in self.commands:
            if re.search(command[0],m):
                res = command[1](message,requestLevel)
        return res
