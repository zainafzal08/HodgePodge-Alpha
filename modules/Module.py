class Module():
    def __init__(self, name):
        self.name = name


    def blankRes(self):
        res = {}
        res["output"] = []
        return res

    def trigger(self, message, requestLevel):
        return self.blankRes()
