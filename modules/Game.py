from modules.ModuleDecorator import Trigger
from modules.Module import Module
from utils.Response import Response
from utils.Formatter import Formatter
import random

# enforce the parser stuff
class Game(Module):
    def __init__(self):
        self.formater = Formatter()
        self.diceTypeLimit = 1000
        self.diceNumLimit = 1000
        super().__init__()

    def validDice(self, d):
        if d < 0:
            return False
        if d > self.diceTypeLimit:
            return False
        return True

    @Trigger('hodge podge.*roll.*a.*d\s*(\-?\d+)',[])
    def roll(self, context):
        res = Response()
        diceType = int(context["groups"][0])
        if not self.validDice(diceType):
            errMsg = "Sorry! I can't roll a d%d, I need a number >0 and <=%d"%(diceType,self.diceTypeLimit)
            res.textResponce(errMsg,context["locationId"])
        else:
            diceRoll = random.randint(1,diceType)
            rollStr = "I got %d!"%diceRoll
            res.textResponce(rollStr,context["locationId"])
        return (res,None)

    @Trigger('hodge podge.*roll[^\d]*(\d+)[^d]*d\s*(\-?\d+)',[])
    def multiroll(self, context):
        res = Response()
        diceNum = int(context["groups"][0])
        diceType = int(context["groups"][1])
        if not self.validDice(diceType):
            errMsg = "Sorry! I can't roll a d%d, I need a number >0 and <=%d"%(diceType,self.diceTypeLimit)
            res.textResponce(errMsg,context["locationId"])
        elif diceNum < 0 or diceNum > self.diceNumLimit:
            errMsg = "Sorry! I can't roll %d dice, I need a number >0 and <=%d"%(diceType,self.diceNumLimit)
            res.textResponce(errMsg,context["locationId"])
        else:
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
            res.textResponce(rollStr,context["locationId"])
        return (res,None)
