class Module():
    def __init__(self):
        pass

    def blankRes(self):
        res = {}
        res["output"] = []
        return res

    def trigger(self, message, requestLevel):
        return self.blankRes()
