class Response():
    def __init__(self):
        self.text = {}
    def textResponce(self, msg, target, type):
        self.text["msg"] = msg
        self.text["target"] = target
        self.text["type"] = type
    def getTextTarget(self):
        return self.text.get("target",None)
    def getTextMsg(self):
        return self.text.get("msg",None)
