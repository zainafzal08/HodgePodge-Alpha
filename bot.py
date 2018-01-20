import discord
import asyncio
import os

# Globals
client = discord.Client()
superAdmins = ["330337388196790284","182968035819126784"]
debug = False
modules = []

# Modules
modules.append(Game())

# hacky way to get class global varaible
parser = modules[0].parser
formatter = modules[0].formatter

# Access Level

def accessLevel(channel, person):
    roles = list(map(lambda x: x.name, person.roles))
    if person.id in superAdmins:
        return 2
    elif "Hodge Podge Wrangler" in roles:
        return 1
    else:
        return 0

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

    # attempt to parse
    raw = message.content
    level = accessLevel(message.channel, message.author)
    parser.parse(raw,level)


client.run(os.environ.get('BOT_TOKEN'))
client.close()
