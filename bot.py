import discord
import asyncio
import os
from modules.Module import Module
from modules.Memes import Memes
from modules.Personality import Personality
from modules.Spells import Spells
from modules.Game import Game
from modules.Db import Db

# Modules
db = Db()
modules = []
modules.append(Memes(db))
modules.append(Personality(db))
modules.append(Spells(db))
modules.append(Game(db))

# Globals
client = discord.Client()
superAdmins = ["theGayAgenda","JDX3"]
debug = True

# Access Level

def accessLevel(channel, person):
    roles = list(map(lambda x: x.name, person.roles))
    if person.name in superAdmins:
        return 2
    elif "Hodge Podge Wrangler" in roles:
        return 1
    else:
        return 0

# Discord event handlers
async def respond(message, res):
    if res['output'] != None:
        for line in res['output']:
            await client.send_message(message.channel, line)

async def moduleErr(message, module, err):
    msg = "_AwFuck_ ... My "+module+" Module has crashed\n"
    msg += "Please let my dads zain and jack know that i had error: `"+err+"`"
    await client.send_message(message.channel, msg)

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

    # trigger modules
    raw = message.content
    level = accessLevel(message.channel, message.author)
    for module in modules:
        try:
            res = module.trigger(message, level)
            await respond(message, res)
        except Exception as e:
            await moduleErr(message,module.name,str(e))
            if debug:
                raise e

client.run(os.environ.get('BOT_TOKEN'))
client.close()
