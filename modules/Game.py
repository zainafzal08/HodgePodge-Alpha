from modules.ModuleDecorator import Trigger
from modules.Module import Module
from utils.Response import Response

# enforce the parser stuff
class Game(Module):
    def __init__(self):
        super().__init__()

    @Trigger('.*hodge podge.*roll.*a.*d\s*(\d+)',[])
    def roll(self, context):
        res = Response()
        res.textResponce("You got it! Haha i'm kidding you haven't coded that up yet fuckface",context["locationId"])
        return (res,None)
