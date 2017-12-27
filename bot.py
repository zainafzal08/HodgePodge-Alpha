import discord
import asyncio
import sqlite3

client = discord.Client()


def argError():
    message = "*Flames Shoot out of the floor* :: Not enough/bad arguments!"
    return message

def command(channel, args):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    res = {}
    res["data"] = None
    res["status"] = 0
    if args[0] == "on" and "say" in args:
        say = ""
        on = ""
        i = len(args)-1
        if args[i] == "say":
            conn.close()
            res["status"] = 1
            return res
        while args[i] != "say":
            say = args[i] + " " + say
            i-=1
        i-=1
        while args[i] != "on":
            on = args[i] + " "+on
            i-=1
        say = say.strip()
        on = on.strip()
        c.execute("SELECT * FROM PHRASES WHERE TRIGGER = ?",(on,))
        if(c.fetchone() != None):
            conn.close()
            res["status"] = 2
            return res
        c.execute("INSERT INTO PHRASES VALUES (?,?,?)", (channel, on, say))
        conn.commit()
        conn.close()
        return res
    elif args[0] == "kill" and len(args)>1:
        phrase = (" ".join(args[1:])).strip()
        c.execute("SELECT * FROM PHRASES WHERE TRIGGER = ?",(phrase,))
        if c.fetchone() != None:
            c.execute("DELETE FROM PHRASES WHERE TRIGGER = ?", (phrase,))
        else:
            conn.close()
            res["status"] = 1
            return res
        conn.commit()
        conn.close()
        return res
    elif args[0] == "list":
        res["status"] = 3
        res["data"] = []
        c.execute("SELECT * FROM PHRASES WHERE CHANNEL_ID = ?",(channel,))
        row = c.fetchone()
        while row != None:
            res["data"].append(str(row[1])+" -> "+str(row[2]))
            row = c.fetchone()
        return res
    else:
        conn.close()
        res["status"] = 1
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
    # ignore bots
    if(message.author.bot):
        return
    m = message.content.lower().split(" ")
    if len(m) > 1 and m[0] == "!hodge" and discord.permissions_in(message.channel).administrator:
        res = command(message.channel.id, m[1:])
        if res["status"] == 1:
            await client.send_message(message.channel, argError())
        elif res["status"] == 2:
            await client.send_message(message.channel, "I already have a phrase for that! You have to kill it first before replacing it.")
        elif res["status"] == 3:
            for line in res["data"]:
                await client.send_message(message.channel, line)   
        else:
            await client.send_message(message.channel, "Got it!")
    elif len(m) == 1 and m[0] == "!hodge":
        await client.send_message(message.channel, argError())
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM PHRASES WHERE CHANNEL_ID = ?",(message.channel.id,))
    pairs = []
    row = c.fetchone()
    while row != None:
        pairs.append((row[1],row[2]))
        row = c.fetchone()
    for pair in pairs:
        if message.content.lower().find(str(pair[0])) != -1:
           await client.send_message(message.channel, str(pair[1]))
           

client.run("Mzk1MzgyNzA0OTYwNzAwNDE2.DSSITw.Te0v0ti0k_xkpxG-vxqm-tKQVZs")
client.close()
