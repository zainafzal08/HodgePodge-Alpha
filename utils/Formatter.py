from utils.Response import Response

class Formatter():
    def __init__(self):
        self.buffer = []
    def output(self, s):
        self.bugger.append(s)
    def error(self, s):
        self.buffer.append("_aww fuck_ %s"%s)
    def list(self, l):
        self.buffer.append("```")
        for e in l:
            self.buffer.append(" >  %s"%e)
        self.buffer.append("```")
    def multiList(self, l):
        self.buffer.append("```")
        for e in l:
            self.buffer.append("%s"%e[0])
            for subE in e[1:]:
                if type(subE) is tuple:
                    self.buffer.append("    %s %s"%(subE[0],subE[1]))
                else:
                    self.buffer.append("    >> %s"%subE)
        self.buffer.append("```")
    def generate(self):
        o = "\n".join(self.buffer)
        return o
    def generateResponse(self):
        res = Response()
        res.textResponce(rollStr,context["locationId"],"out")
        return res
    def clear(self):
        self.buffer.clear()
    def getLines(self):
        return len(self.buffer)
    def getLen(self):
        return len(self.generate())
