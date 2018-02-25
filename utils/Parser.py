import re

class Match():
    def __init__(self, triggerFunction, triggerObject, responseF):
        self.f = triggerFunction;
        self.triggerObj = triggerObject
        self.resF = responseF
    def trigger(self):
        self.f(self.triggerObj)
    async def respond(self, c, ch):
        await self.resF(c,ch)

class Parser():
    def __init__(self):
        self.triggerList = []
    def register(self, module, trigger):
        t = {}
        t["re"] = re.compile(trigger["trigger"])
        t["f"] = trigger["function"]
        t["l"] = trigger["accessLevel"]
        if "id" in trigger:
            t["id"] = trigger["id"]
        else:
            t["id"] = None
        t["module"] = module
        if "ignore" in trigger:
            t["ignore"] = trigger["ignore"]
        else:
            t["ignore"] = []
        self.triggerList.append(t)
    def parse(self, m, l):
        m = m.content.lower()
        matches = []
        for t in self.triggerList:
            cleanedM = m
            for phrase in t["ignore"]:
                cleanedM = cleanedM.replace(phrase,"")
            attempt = t["re"].search(cleanedM)
            if l >= t["l"] and attempt:
                matches.append(self.createMatch(attempt,t))
        return matches

    def createMatch(self,a,t):
        obj = {}
        obj["args"] = a.groups()
        obj["id"] = t["id"]
        return Match(t["f"],obj,t["module"].respond)
