import sqlite3


class Database():
    def __init__(self):
        self.conn = sqlite3.connect('data.db')
        self.c = self.conn.cursor()

    def containsTrigger(self, channel, trigger):
        self.c.execute("SELECT * FROM PHRASES WHERE TRIGGER = ? AND CHANNEL_ID = ?",(trigger.strip(),channel))
        if(self.c.fetchone() != None):
            return True
        return False

    def allPhrases(self, channel):
        self.c.execute("SELECT * FROM PHRASES WHERE CHANNEL_ID = ?",(channel,))
        row = self.c.fetchone()
        res = []
        while row != None:
            res.append((str(row[1]).strip(),str(row[2]).strip()))
            row = self.c.fetchone()
        return res

    def deletePhrase(self, channel, phrase):
        self.c.execute("DELETE FROM PHRASES WHERE TRIGGER = ? AND CHANNEL_ID = ?", (phrase.strip(),channel))
        self.conn.commit()

    def newPhrase(self, channel, phrase, response):
        self.c.execute("INSERT INTO PHRASES VALUES (?,?,?)", (channel, phrase, response))
        self.conn.commit()

    def searchSpell(self, search, field):
        search = "%"+search+"%"
        self.c.execute("SELECT * FROM SPELLS WHERE "+field+" LIKE ?", (search,))
        row = self.c.fetchone()
        res = []
        while row != None:
            rowDict = {}
            rowDict["name"] = row[0]
            rowDict["school"] = row[1]
            rowDict["level"] = row[2]
            rowDict["casting_time"] = row[3]
            rowDict["components"] = row[4]
            rowDict["duration"] = row[5]
            rowDict["range"] = row[6]
            rowDict["classes"] = row[7]
            rowDict["description"] = row[8]
            rowDict["at_higher_levels"] = row[9]
            res.append(rowDict)
            row = self.c.fetchone()
        return res
