import sqlite3


class Database():
    def __init__(self, file):
        self.conn = sqlite3.connect('data.db')
        self.c = self.conn.cursor()

    def containsTrigger(self, channel, trigger):
        self.c.execute("SELECT * FROM PHRASES WHERE TRIGGER = ? AND CHANNEL_ID = ?",(trigger.strip(),channel))
        if(self.c.fetchone() != None):
            return True
        return False

    def allPhrases(self, channel):
        self.c.execute("SELECT * FROM PHRASES WHERE CHANNEL_ID = ?",(channel,))
        row = c.fetchone()
        res = []
        while row != None:
            res.append((str(row[1]).strip(),str(row[2]).strip()))
            row = self.c.fetchone()
        return res

    def deletePhrase(self, channel, phrase):
        self.c.execute("DELETE FROM PHRASES WHERE TRIGGER = ? AND CHANNEL_ID = ?", (phrase.strip(),channel))
        self.conn.commit()

    def newPhrase(self, channel, phrase, response):
        self.c.execute("INSERT INTO PHRASES VALUES (?,?,?)", (channel, on, say))
        self.conn.commit()
