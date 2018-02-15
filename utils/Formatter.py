class Formatter():
    def __init__(self):
        self.buffer = []
    def consoleFlush(self):
        for l in self.buffer:
            print(l)
    def flush(self, client, channel):
        final = "\n".join(self.buffer)
        await client.send_message(channel, final)
    def output(self, s):
        self.buffer.append(s)
    def error(self, s):
        self.buffer.append("`>> %s`"%s)
    def list(self, l):
        self.buffer.append("```")
        for e in l:
            self.buffer.append(" >  %s"%e)
