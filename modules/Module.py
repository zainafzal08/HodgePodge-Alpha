class Module():
    def __init__(self, name):
        self.name = name


    def blankRes(self):
        res = {}
        res["output"] = []
        res["channel_output_target"] = ""
        res["channel_output"] = ""
        return res

    def trigger(self, message, requestLevel):
        return self.blankRes()
