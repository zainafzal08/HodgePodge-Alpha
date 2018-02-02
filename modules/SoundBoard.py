from modules.Module import Module
import discord
import re

class SoundBoard(Module):
    def __init__(self, db):
        super().__init__("SoundBoard")
        self.commands = [
            ("hodge podge play (.*)$", self.playSound),
            ("hodge podge stop$", self.endSound),
            ("hodge podge leave$", self.byebye),
            ("hodge podge remember (.*) as (.*)$", self.register),
            ("hodge podge quickplay (.*)$", self.quickPlay)
        ]
        self.db = db

    def register(self, message, level):
        if level < 2:
            return
        res = super().blankRes()
        s = re.search("hodge podge remember (.*) as (.*)$",self.shallowClean(message.content))
        url = s.group(1)
        track = s.group(2)
        err = self.db.newTrack(url,track)
        if err:
            res["output"].append("I already have a name for that link! (%s)"%err)
        else:
            res["output"].append("Got it!")
        return res

    def quickPlay(self, message, level):
        if level < 2:
            return
        res = super().blankRes()
        s = re.search("hodge podge quickplay (.*)$",self.shallowClean(message.content))
        track = self.shallowClean(s.group(1))
        res["output"].append("Attempting to play %s"%track)
        res["audio"] = track
        return res

    def playSound(self, message, level):
        if level < 2:
            return
        res = super().blankRes()
        s = re.search("hodge podge play (.*)$",self.shallowClean(message.content))
        sound = self.shallowClean(s.group(1))
        track = self.db.getTrack(sound)
        if not track:
            res["output"].append("I Don't know that track!")
            return res

        res["output"].append("playing %s ..."%sound)
        res["audio"] = track
        return res

    def endSound(self, message, level):
        if level < 2:
            return
        res = super().blankRes()
        res["killAudio"] = True
        return res

    def byebye(self, message, level):
        if level < 2:
            return
        res = super().blankRes()
        res["output"] .append("Goodbye!")
        res["disconnect"] = True
        return res

    def clean(self, t):
        m = t.lower()
        m = re.sub(r'\s+',' ',m)
        m = re.sub(r'[\,\.\?\;\:\%\#\@\!\^\&\*\+\-\+\_\~\']','',m)
        m = m.strip()
        return m

    def shallowClean(self, t):
        return t.strip()

    def trigger(self, message, requestLevel):
        res = super().blankRes()
        original = message.content;
        m = self.clean(message.content)
        for command in self.commands:
            if re.search(command[0],m):
                res = command[1](message,requestLevel)
        return res
