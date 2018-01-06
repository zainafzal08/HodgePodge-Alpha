from modules.Module import Module
import re

class Personality(Module):
    def __init__(self, db):
        super().__init__("Personality")
        self.crashes = 0
        self.triggers = {
            "i love you hodge podge": "I love you too friend :heart:",
            "hodge podge i love you": "I love you too friend :heart:",
            "how are you hodge podge": "I'm Wonderful! I hope you are doing well too :)",
            "hodge podge how are you": "I'm Wonderful! I hope you are doing well too :)",
            "hi hodge podge\s*$": "Hello!",
            "hey hodge podge\s*$": "Hello!",
            "yo hodge podge\s*$": "Hello!",
            "hodge podge who made you": "Zain and Jack are my fathers! And i love them a lot :heart:",
            "hodge podge who are your parents": "Zain and Jack are my fathers! And i love them a lot :heart:",
            "im crying": "Don't cry! I love you afterall :smile:",
            "im gonna fucken cry": "Don't cry! I love you afterall :smile:",
            "im gonna cry": "Don't cry! I love you afterall :smile:",
            "^\s*crying\s*$": "Don't cry! I love you afterall :smile:",
            "bye hodge podge": "Goodbye! I hope i get to talk to you again :heart:"
        }
        self.superAdminTriggers = {
            "love our robot son": "I love you too dad :heart:",
            "hey son": "hey dad!",
            "where is our bot boy": "right here!",
            "our son is great": "So are you dad!"
        }

    def clean(self, t):
        m = t.lower()
        m = re.sub(r'\s+',' ',m)
        m = re.sub(r'[\,\.\?\;\:\%\#\@\!\^\&\*\+\-\+\_\~\']','',m)
        m = m.strip()
        return m

    def trigger(self, message, requestLevel):
        res = super().blankRes()
        original = message.content;
        m = self.clean(message.content)
        for key in self.triggers:
            if re.search("("+key+")",m) != None:
                res["output"].append(self.triggers[key])

        if requestLevel > 1:
            for key in self.superAdminTriggers:
                if re.search("("+key+")",m) != None:
                    res["output"].append(self.superAdminTriggers[key])

        if re.search("hodge podge status report",m):
            res["output"].append("Here you go dad!\n\n`[Crashes: %d]"%self.crashes)
        return res
