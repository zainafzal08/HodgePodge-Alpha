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

    def removeDuplicates(self, l, i):
        seen = []
        s = []
        for e in l:
            if e[i] in seen:
                continue
            else:
                seen.append(e[i])
                s.append(e)
        return s

    def newTrack(self, url, track):
        c = self.conn.cursor()
        c.execute("SELECT * FROM TRACKS WHERE URL = %s",(url,))
        t = c.fetchone()
        if t:
            return t[1]
        c.execute("INSERT INTO TRACKS VALUES(%s,%s)",(url,track))
        self.conn.commit()
        return None


    def getTrack(self, track):
        c = self.conn.cursor()
        c.execute("SELECT * FROM TRACKS WHERE TRACK = %s",(track,))
        t = c.fetchone()
        if t:
            return t[0]
        else:
            return None

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
        return self.removeDuplicates(self.fetchAll(c),0);

    def scoreEdit(self, channel, scoreType, person, score):
        c = self.conn.cursor()
        c.execute("SELECT * FROM SCORES WHERE CHANNEL = %s AND TYPE = %s AND PERSON = %s",(channel,scoreType,person))
        entry = c.fetchone()
        if entry == None:
            c.execute("INSERT INTO SCORES VALUES (%s,%s,%s,%s)",(channel,scoreType,person,score))
            self.conn.commit()
            return score
        else:
            score += entry[3]
            c.execute("UPDATE SCORES SET POINTS = %s WHERE CHANNEL = %s AND PERSON = %s AND TYPE = %s",(score,channel,person,scoreType))
            self.conn.commit()
            return score

    def scoreListTypes(self, channel):
        c = self.conn.cursor()
        c.execute("SELECT TYPE FROM SCORES WHERE CHANNEL = %s",(channel,))
        return self.removeDuplicates(self.fetchAll(c),0)

    def getAllScores(self, channel, scoreType):
        c = self.conn.cursor()
        c.execute("SELECT PERSON, POINTS FROM SCORES WHERE CHANNEL = %s and TYPE = %s",(channel,scoreType))
        return list(set(list(map(lambda x: (str(x[0]),str(x[1])),self.fetchAll(c)))))

    def spellGet(self, spell):
        c = self.conn.cursor()
        spell = "%"+spell+"%"
        spell = spell.upper()
        c.execute("SELECT * FROM SPELLS WHERE UPPER(NAME) LIKE %s",(spell,))
        return self.fetchAll(c)

    def spellSearch(self, search):
        c = self.conn.cursor()
        query = "SELECT * FROM SPELLS WHERE "
        params = []
        for i,k in enumerate(search.keys()):
            if i == 0:
                query+="UPPER("+k+") LIKE %s"
            else:
                query+=" AND UPPER("+k+") LIKE %s"
            params.append("%"+search[k].upper()+"%")
        c.execute(query,tuple(params))
        return self.fetchAll(c)
