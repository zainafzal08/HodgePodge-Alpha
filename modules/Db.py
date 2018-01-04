import psycopg2
import urllib.parse as urlparse
import os

class Db():
    def __init__(self):
        url = urlparse.urlparse(os.environ['DATABASE_URL'])
        dbname = url.path[1:]
        user = url.username
        password = url.password
        host = url.hostname
        port = url.port
        self.conn = psycopg2.connect(dbname=dbname,user=user,password=password,host=host,port=port)

    def fetchAll(self, c):
        curr = c.fetchone()
        result = []
        while curr != None:
            result.append(curr)
            curr = c.fetchone()
        return result

    def getAllMemes(self, channel):
        c = self.conn.cursor()
        c.execute("SELECT * FROM MEMES WHERE CHANNEL = %s",(channel,))
        result = self.fetchAll(c)
        result = list(map(lambda x: x[1:],result))
        return result

    def insertMeme(self, channel, on, say):
        c = self.conn.cursor()
        c.execute("SELECT * FROM MEMES WHERE CHANNEL = %s AND TRIGGER = %s",(channel,on))
        if c.fetchone() != None:
            return True
        c.execute("INSERT INTO MEMES VALUES (%s,%s,%s)",(channel,on,say))
        self.conn.commit()
        return False

    def deleteMeme(self, channel, on):
        c = self.conn.cursor()
        c.execute("SELECT * FROM MEMES WHERE CHANNEL = %s AND TRIGGER = %s",(channel,on))
        if c.fetchone() == None:
            return True
        c.execute("DELETE FROM MEMES WHERE CHANNEL = %s AND TRIGGER = %s",(channel,on))
        self.conn.commit()
        return False

    def getMemeChannels(self):
        c = self.conn.cursor()
        c.execute("SELECT CHANNEL FROM MEMES")
        return self.fetchAll(c);
