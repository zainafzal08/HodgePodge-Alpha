class BotModule():
    def __init__(self, name):
        self.name = name.lower()
    def getTriggerList(self):
        return []
    def connectDb(self, db):
        return
    async def respond(self, client, channel):
        return
