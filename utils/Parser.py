# REMEMER TO TELL MODULES WHEN TRIGGERING THEM OF CLASHES
import re

class Match():
    def __init__(self, triggerFunction, triggerObject, responseF):
        self.f = triggerFunction;
        self.triggerObj = triggerObject
        self.resF = responseF
    def trigger(self):
        self.f(self.triggerObj)
    def respond(self, c, ch):
        self.resF(c,ch)

class Parser():
    def __init__(self):
        self.triggerList = []
    def register(self, module, trigger):
        t = {}
        t["re"] = re.compile(trigger["trigger"]) #TODO: does this work?
        t["f"] = trigger["function"]
        t["l"] = trigger["accessLevel"]
        if trigger["id"]:
            t["id"] = trigger["id"]
        else:
            t["id"] = None
        t["module"] = module
        t["ignore"] = trigger["ignore"]
        self.triggerList.append(t)
    def parse(self, m, l):
        m = m.content.lower()
        matches = []
        for t in self.triggerList:
            cleanedM = m
            for phrase in t["ignore"]:
                cleanedM = re.sub(phrase,"",cleanedM)
            attempt = t["re"].search(cleanedM) #TODO: does this work?
            if l >= t["l"] and attempt:
                matches.append(self.createMatch(attempt,t))
        return matches

    def createMatch(self,a,t):
        obj = {}
        obj["args"] = a.groups() #TODO: does this work?
        obj["id"] = t["id"]
        return Match(t["function"],obj,t["module"].respond)
