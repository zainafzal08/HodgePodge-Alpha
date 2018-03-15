class Response():
    def __init__(self):
        self.text = {}
        self.voice = {}
    def textResponce(self, msg, target):
        self.text["msg"] = msg
        self.text["target"] = target
    def getTextTarget(self):
        return self.text.get("target",None)
    def getTextMsg(self):
        return self.text.get("msg",None)
