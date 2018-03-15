from modules.ModuleDecorator import Trigger
from modules.Module import Module

# enforce the parser stuff
class Game(Module):
    def __init__(self):
        self.lol = "fuck"
        super().__init__()

    @Trigger('.*hodge podge .* roll a d(\d+)',[])
    def roll(self):
        print("Doing the Roll")
