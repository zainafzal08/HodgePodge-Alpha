from modules.ModuleDecorator import Trigger
from modules.Module import Module
from utils.Response import Response
from utils.Formatter import Formatter
import random

# enforce the parser stuff
class Game(Module):
    def __init__(self):
        self.formatter = Formatter()
        self.diceTypeRange = (1,1000)
        self.diceNumRange = (1,1000)
        self.diceCheck = (self.validDice,"I can only handle d%d to d%d"%self.diceTypeRange)
        self.diceNumCheck = (self.validDiceNum,"I can only handle %d to %d rolls"%self.diceTypeRange)
        super().__init__()

    def validDice(self, d):
        d = int(d)
        return d >= self.diceTypeRange[0] and d <= self.diceTypeRange[1]

    def validDiceNum(self, d):
        d = int(d)
        return d >= self.diceNumRange[0] and d <= self.diceNumRange[1]

    @Trigger('hodge podge.*roll.*a.*d\s*(\-?\d+)',[],["diceCheck"])
    def roll(self, context):
        diceType = int(context["groups"][0])
        res = Response()
        result = random.randint(1,diceType)
        res.textResponce("I Got %d!"%result,context["locationId"],"output")
        return res

    @Trigger('hodge podge.*roll[^\d]*(\d+)[^d]*d\s*(\-?\d+)',[],["diceNumCheck","diceCheck"])
    def multiroll(self, context):
        # set up
        res = Response()
        diceNum = int(context["groups"][0])
        diceType = int(context["groups"][1])
        # calculate
        components = []
        sum = 0
        for i in range(diceNum):
            d = random.randint(1,diceType)
            sum += d
            components.append(str(d))
        rollStr = "I got %d!"%sum
        componentStr = " (%s)"%("+".join(components))
        if len(rollStr) + len(componentStr) < 2000:
            rollStr += componentStr
        res.textResponce(rollStr,context["locationId"],"out")
        return res
