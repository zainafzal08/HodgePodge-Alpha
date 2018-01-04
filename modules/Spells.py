from modules.Module import Module
import re

class Spells(Module):
    def __init__(self, db):
        super().__init__()
        self.db = db

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

        return res
