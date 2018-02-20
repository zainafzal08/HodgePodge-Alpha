class Formatter():
    def __init__(self):
        self.buffer = []
    def consoleFlush(self):
        for l in self.buffer:
            print(l)
    def flush(self, client, channel):
        final = "\n".join(self.buffer)
        if len(final) > 2000:
            msg = "... There was more but i can only send 2000 characters at a time!"
            final = final[0:1995-len(msg)]+msg
        await client.send_message(channel, final)
    def output(self, s):
        self.buffer.append(s)
    def error(self, s):
        self.buffer.append("_aww fuck_ i had a error! Let my dads know that: `>> %s`"%s)
    def list(self, l):
        self.buffer.append("```")
        for e in l:
            self.buffer.append(" >  %s"%e)
        self.bugger.append("```")
