from modules.Module import Module
import re

class Memes(Module):
    def __init__(self, db, client):
        super().__init__("Memes")
        self.client = client
        self.commands = [
            ("hodge podge list your memes", self.list),
            ("hodge podge on .+ say .+$",self.newMeme),
            ("hodge podge kill .+$",self.killMeme),
            ("hodge podge override list channels$",self.listChannels),
            ("hodge podge override on channel \w+ on .+ say .+$",self.overrideNewMeme),
            ("hodge podge override on channel \w+ list memes",self.overrideListMeme),
            ("hodge podge override on channel \w+ kill .+$",self.overrideKillMeme)
        ]
        self.db = db

    def clean(self, t):
        m = t.lower()
        m = re.sub(r'[\,\.\?\;\%\#\@\!\^\&\*\+\-\+\_\~\']','',m)
        m = re.sub(r'\s+',' ',m)
        m = m.strip()
        return m

    def shallowClean(self, t):
        m = re.sub(r'\s+',' ',t)
        m = m.strip()
        return m

    def channelIdToName(self, search):
        channel = self.client.get_channel(search)
        server = channel.server
        return "%s (%s)"%(server.name, channel.name)

    def cycleImage(self, message, level):
        if level < 1:
            return

    def listChannels(self, message, level):
        if level < 2:
            return
        channels = list(map(lambda x: x[0],self.db.getMemeChannels()))

        response = []
        if len(channels) == 0:
            response.append("Sorry Friends, I don't know any channels yet!")
        else:
            response.append("Here are all the channels i know!")
            response.append("\n")
            for channel in channels:
                response.append("**"+channel+"**:\t"+self.channelIdToName(channel))
            response.append("\n")
        res = super().blankRes()
        res["output"].append("\n".join(response))
        return res

    def overrideNewMeme(self, message, level):
        if level < 2:
            return
        channels = list(map(lambda x: x[0],self.db.getMemeChannels()))
        s = re.search("hodge podge override on channel (\w+) on (.+) say (.+)$",self.shallowClean(message.content),flags=re.IGNORECASE)
        channel = s.group(1).strip()
        on = self.clean(s.group(2))
        say = s.group(3).strip()
        res = super().blankRes()
        if channel in channels:
            err = self.db.insertMeme(channel, on, say)
            if err:
                res["output"].append("Sorry! I already have a response for that, you can do a overide kill though!")
            else:
                res["output"].append("**dabs** Got it!")
        else:
            res["output"].append("Now i'm no scientist but i don't think that channel exists")
        return res

    def overrideKillMeme(self, message, level):
        if level < 2:
            return
        s = re.search("hodge podge override on channel (\w+) kill (.+)$",self.shallowClean(message.content),flags=re.IGNORECASE)
        res = super().blankRes()
        channel = s.group(1).strip()
        on = self.clean(s.group(2))
        channels = list(map(lambda x: x[0],self.db.getMemeChannels()))
        if channel in channels:
            err = self.db.deleteMeme(channel, on)
            if err:
                res["output"].append("Sorry Friend! I don't know that phrase!")
            else:
                res["output"].append("**poof** It's gone!")
        else:
            res["output"].append("Now i'm no scientist but i don't think that channel exists")
        return res

    def overrideListMeme(self, message, level):
        if level < 2:
            return
        s = re.search("hodge podge override on channel (\w+) list memes",self.shallowClean(message.content),flags=re.IGNORECASE)
        channel = s.group(1).strip()
        channels = list(map(lambda x: x[0],self.db.getMemeChannels()))
        res = super().blankRes()
        response = []
        if channel in channels:
            memes = self.db.getAllMemes(channel)
            if len(memes) == 0:
                response.append("That channel doesn't have any memes!")
                response.append("\n")
            else:
                response.append("Here are all the memes i know!")
                response.append("\n")
                for meme in memes:
                    response.append("**on**:\t"+meme[0])
                    response.append("**say**:\t"+meme[1])
                    response.append("")
                response.append("\n")
                res["output"].append("\n".join(response))
        else:
            res["output"].append("Now i'm no scientist but i don't think that channel exists")
        return res

    def killMeme(self, message, level):
        if level < 1:
            return
        s = re.search("hodge podge kill (.+)$",self.shallowClean(message.content),flags=re.IGNORECASE)
        res = super().blankRes()
        on = self.clean(s.group(1))
        err = self.db.deleteMeme(message.channel.id, on)
        if err:
            res["output"].append("Sorry Friend! I don't know that phrase!")
        else:
            res["output"].append("**poof** It's gone!")
        return res

    def newMeme(self, message, level):
        if level < 1:
            return
        s = re.search("hodge podge on (.+) say (.+)$",self.shallowClean(message.content),flags=re.IGNORECASE)
        on = self.clean(s.group(1))
        say = s.group(2).strip()
        err = self.db.insertMeme(message.channel.id, on, say)
        res = super().blankRes()
        if err:
            res["output"].append("Sorry Friend! I already have a reponse for that, do `hodge podge kill <trigger>` to get rid of it!")
        else:
            res["output"].append("**dabs** Got it!")
        return res

    def list(self, message, level):
        if level < 1:
            return
        memes = self.db.getAllMemes(message.channel.id)
        res = super().blankRes()
        response = []
        if len(memes) == 0:
            response.append("I don't know any memes! say `hodge podge on <trigger> say <response>` to help me learn!")
            response.append("\n")
        else:
            response.append("Here are all the memes i know!")
            response.append("\n")
            for meme in memes:
                response.append("**on**:\t"+meme[0])
                response.append("**say**:\t"+meme[1])
                response.append("")
            response.append("\n")
        res["output"].append("\n".join(response))
        return res

    def trigger(self, message, requestLevel):
        res = None
        m = self.clean(message.content)
        for command in self.commands:
            if re.search(command[0],m):
                res = command[1](message,requestLevel)
        if not res:
            memes = self.db.getAllMemes(message.channel.id)
            res = super().blankRes()
            for meme in memes:
                if re.search(meme[0],m):
                    res["output"].append(meme[1])
        return res
