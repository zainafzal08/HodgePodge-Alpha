import sys
import re

class TestInterface():
    def __init__(self,boy):
        self.boy = boy
        self.level = 0
        self.done = False
        self.running = False
        self.cmds = [
            ('level (\d+)', self.updateLevel, True,"Level Updated"),
            ('quit', self.exit, False,"Goodbye"),
        ]
        self.cmdTrigger = "\\"
    def run(self):
        print(">> Launching Test Interface...")
        print(">> Ready!")
        self.running = True
        l = self.getLine()
        while self.running:
            if l[0] == self.cmdTrigger:
                r = self.interfaceCommands(l[1:])
                print(">> %s"%r)
            else:
                res = self.boy.talk(l,self.level)
            if self.running:
                l = self.getLine()
    def getLine(self):
        try:
            l = input("> ")
            return l
        except:
            self.running = False
            return None

    def updateLevel(self, l):
        if l:
            self.level = l
    def exit(self):
        self.running = False
        return
    def interfaceCommands(self, txt):
        for cmd in self.cmds:
            s = re.search(cmd[0],txt)
            if s:
                if cmd[2]:
                    cmd[1](s.groups(1))
                else:
                    cmd[1]()
                return cmd[3]
        return "Illegal Command"
