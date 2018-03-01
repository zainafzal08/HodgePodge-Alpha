import discord
import asyncio
import os
import re
from bots.HodgePodge.HodgePodge import HodgePodge
from utils import TableExtracter
from utils.Formatter import Formatter

# Globals
client = discord.Client()

botObjs = []
botObjs.append(HodgePodge(client))
bots = {}
for bot in botObjs:
    bots[bot.name.lower()] = bot

async def helpCmd(channel, m):
    # set up
    f = Formatter()
    s = re.search("(.*) help with (.*)",m)
    helpObj = None
    if not s:
        return
    requestName = s.group(1).strip().lower()
    requestMod = s.group(2).strip().lower()
    if requestName in bots:
        helpObj = bots[requestName].getHelp(requestMod)
    if not helpObj:
        return
    # get fields
    cmds = None
    docs = helpObj.get("docs",None)
    if "raw" in helpObj:
        try:
            cmd = TableExtracter.extract(requests.get(helpObj["raw"]).text,requestMod)
        except:
            cmd = None
    # handle errors
    if not docs and cmds:
        tooLongMessage = "There are a tad too many commands in that module for me to give you here!"
        docMessage = None
    elif docs and not cmds:
        tooLongMessage = None
        docMessage = "Check out the documentation if you want some more info!\n%s"%docs
    elif not docs and not cmds:
        return
    else:
        tooLongMessage = "There are a tad too many commands in that module for me to give you here! Try checking out the documentation here\n%s"%docs
        docMessage = "Check out the documentation if you want some more info!\n%s"%docs

    if cmds:
        f.output("Here's some of the commands you can use with that module!")
        cmds = list(map(formatCmd,cmds))
        f.list(cmds)
    if docMessage:
        f.output(docMessage)
    messLen = f.getLen()
    if(messLen > 2000):
        f.clear()
        f.output(tooLongMessage)
    await f.flush(client, channel)

def formatCmd(e):
    if len(e) == 0:
        return (e[0],"")
    if e[2][0] == "`" and e[2][-1] == "`":
        desc = "%s (%s)"%(e[1],e[2][1:-1])
    else:
        desc = "%s (%s)"%(e[1],e[2])
    return (e[0],desc)

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
    # help
    await helpCmd(message.channel, message.content)
    # interact with bots
    for bot in bots:
        await bots[bot].talk(message)

if __name__ == "__main__":
    client.run(os.environ.get('BOT_TOKEN'))
    client.close()
