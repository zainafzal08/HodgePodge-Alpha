from tools.Db import Db
from tools.Parser import Parser
from tools.Formatter import Formatter

class Module():
    db = Db()
    parser = Parser()
    formatter = Formatter()
    def __init__(self, name):
        self.name = name
