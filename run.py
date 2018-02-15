import discord
import asyncio
import os
import re
from bots/HodgePodge/HodgePodge import HodgePodge

# Globals
client = discord.Client()
bots = []
bots.append(HodgePodge(client))
botNames.append(bots[0].name.lower())

def helpCmd(channel, m):
    s = re.search("(.*) help with (.*)",m)
    if not s:
        return
    if s.group(1).strip().lower() in botNames:
        helpObj = bots[botNames.indexOf(s.group(1).strip().lower())].getHelp()
    if not helpObj:
        return
    response = []
    response.append("Here's some of the commands you can use with me!")
    for l in helpObj["cmds"]:
        response.append("**%s**"%l[0])
        response.append("%s"%l[1])
        response.append("`%s`"%l[2])
        response.append("")
    response.append("Check out the documentation if you want some more info!\n%s"%helpObj["docs"])
    response = "\n".join(response)
    if(len(response) > 2000):
        await client.send_message(channel, "There are a tad too many commands in that module for me to give you here! Try checking out the documentation here\n%s"%helpObj["docs"])
    else:
        await client.send_message(channel, response)

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
    helpCmd(message.content)
    # interact with bots
    for bot in bots:
        bot.talk(message)

client.run(os.environ.get('BOT_TOKEN'))
client.close()
