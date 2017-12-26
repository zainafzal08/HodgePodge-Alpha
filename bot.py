import discord
import asyncio
import sqlite3

client = discord.Client()

# Helper Functions

# result.err = 1 if name exists
def register(channel, name):
    res = {}
    res["err"] = 0
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM USERS WHERE CHANNEL_ID=? AND NAME=?', (channel, name))
    if c.fetchone() != None:
        res["err"] = 1
        return res;
    c.execute("INSERT INTO USERS VALUES (?,?,?)", (channel, name, 0))
    conn.commit()
    return res

# result.err = 1 if wrong name
# result.err = 2 if wrong value
# result.new = new flirt point val
def reward(channel, name, amount):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    res = {}
    res["err"] = 0
    res["new"] = None
    c.execute('SELECT * FROM USERS WHERE CHANNEL_ID=? AND NAME=?', (channel, name))
    row = c.fetchone()
    if row == None:
        res["err"] = 1
        return res;
    val = None
    try:
        val = int(amount)
    except:
        res["err"] = 2
        return res;
    newPoints = val + row[2]
    c.execute("UPDATE USERS SET POINTS = ? WHERE NAME = ? AND CHANNEL_ID = ?", (newPoints,name, channel))
    conn.commit()
    res["new"] = newPoints
    return res
# result.err = 1 if wrong name
# result.err = 2 if wrong value
# result.new = new flirt point val
def punish(channel, name, amount):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    res = {}
    res["err"] = 0
    res["new"] = None
    c.execute('SELECT * FROM USERS WHERE CHANNEL_ID=? AND NAME=?', (channel, name))
    row = c.fetchone()
    if row == None:
        res["err"] = 1
        return res;
    val = None
    try:
        val = int(amount)
    except:
        res["err"] = 2
        return res;
    newPoints = row[2] - val
    c.execute("UPDATE USERS SET POINTS = ? WHERE NAME = ? AND CHANNEL_ID = ?", (newPoints,name, channel))
    conn.commit()
    res["new"] = newPoints
    return res

# result.err = 1 if no names
# result.data = array of printable stats
def status(channel):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    res = {}
    res["err"] = 0
    res["data"] = []
    c.execute('SELECT * FROM USERS WHERE CHANNEL_ID = ?', (channel,))
    row = c.fetchone()
    if row == None:
        res["err"] = 1
        return res
    while row != None:
        res["data"].append("%s [%d]"%(row[1],row[2]))
        row = c.fetchone()
    return res

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    print(client)


@client.event
async def on_message(message):
    m = message.content.split(" ")
    if m[0] == "!ft" and len(m) > 1:
        c = m[1]
        args = m[2:]
        if c == "register":
            res = register(message.channel.id,args[0])
            if res["err"] == 1:
                await client.send_message(message.channel, "I already know who %s is silly!"%args[0])
            else:
                await client.send_message(message.channel, "Welcome %s! You have 0 Points, get to flirting :D"%args[0])
        elif c == "reward":
            res = reward(message.channel.id,args[0],args[1])
            if res["err"] == 1:
                await client.send_message(message.channel, "Sorry! I don't know who %s is, Perhaps try doing !ft register %s :)"%args[0])
            elif res["err"] == 2:
                await client.send_message(message.channel, "Sorry! Flirt points must be simple integers!")
            else:
                await client.send_message(message.channel, "%s is now at %d flirt points!"%(args[0],res["new"]))
        elif c == "punish":
            res = punish(message.channel.id,args[0],args[1])
            if res["err"] == 1:
                await client.send_message(message.channel, "Sorry! I don't know who %s is, Perhaps try doing !ft register %s :)"%args[0])
            elif res["err"] == 2:
                await client.send_message(message.channel, "Sorry! Flirt points must be simple integers!")
            else:
                await client.send_message(message.channel, "%s is now at %d flirt points :("%(args[0],res["new"]))
        elif c == "status":
            res = status(message.channel.id)
            if res["err"] == 1:
                await client.send_message(message.channel, "Sorry i don't know anyone in this channel yet! Perhaps try doing !ft register :)"%args[0])
            else:
                for r in res["data"]:
                    print(r)
                    await client.send_message(message.channel, r)
    # a lil hint message
    if message.lower().contains("good flirt"):
        await client.send_message(message.channel, "Well hello, is sombody blushing? Maybe it's time to give someone some points ;)"%args[0])

client.run("Mzk1MTU0ODc5NzAzNjc4OTc3.DSO0Fw.KVo8P42u9GeBB_RLBZ2dQGnEvKw")
client.close()
