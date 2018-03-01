class Formatter():
    def __init__(self):
        self.buffer = []
    def consoleFlush(self):
        for l in self.buffer:
            print(l)
        self.buffer.clear()
    async def flush(self, client, channel):
        final = "\n".join(self.buffer)
        if len(final) > 2000:
            msg = "... There was more but i can only send 2000 characters at a time!"
            final = final[0:(1995-len(msg))]+msg
        await client.send_message(channel, final)
        self.buffer.clear()
    def output(self, s):
        self.buffer.append(s)
    def error(self, s):
        self.buffer.append("_aww fuck_ %s"%s)
    def list(self, l):
        self.buffer.append("```")
        for e in l:
            self.buffer.append(" >  %s"%e)
        self.bugger.append("```")
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
    def getRaw(self):
        return "\n".join(self.buffer)
    def clear(self):
        self.buffer.clear()
    def getLen(self):
        return len(self.getRaw())
