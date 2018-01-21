import discord
import asyncio
import os
from bots/HodgePodge import HodgePodge

# Globals
client = discord.Client()
bots = []
bots.append(HodgePodge(client))

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
    # interact with bots
    for bot in bots:
        bot.talk(message)

client.run(os.environ.get('BOT_TOKEN'))
client.close()
