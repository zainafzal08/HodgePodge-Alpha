import discord
import asyncio
import os
from modules.Module import Module
from modules.Memes import Memes
from modules.Personality import Personality
from modules.Spells import Spells
from modules.Game import Game
from modules.Db import Db
from modules.SoundBoard import SoundBoard

# Globals
client = discord.Client()
superAdmins = ["330337388196790284","182968035819126784"]
debug = False
silence = False
player = None
vc = None
OPUS_LIBS = ['libopus-0.x86.dll', 'libopus-0.x64.dll', 'libopus-0.dll', 'libopus.so.0', 'libopus.0.dylib']

# Modules
db = Db()
modules = []
modules.append(Memes(db, client))
modules.append(Personality(db))
modules.append(Spells(db))
modules.append(Game(db))
modules.append(SoundBoard(db))

# Access Level

def accessLevel(channel, person):
    roles = list(map(lambda x: x.name, person.roles))
    if person.id in superAdmins:
        return 2
    elif "Hodge Podge Wrangler" in roles:
        return 1
    elif "Robot-Whisperer" in roles:
        return 1
    else:
        return 0

# Discord event handlers
async def respond(message, res):
    if silence:
        return
    if res['output'] != None:
        for line in res['output']:
            await client.send_message(message.channel, line)

async def channelOutput(message, res):
    if silence:
        return
    await client.send_message(find(lambda c: c.id == res["channel_output_target"], client.get_all_channels()), res["channel_output"])

def load_opus_lib():
    if discord.opus.is_loaded():
        return True
    for opus_lib in OPUS_LIBS:
        try:
            discord.opus.load_opus(opus_lib)
            return
        except OSError:
            pass
    raise RuntimeError('Could not load an opus lib. Tried %s' % (', '.join(OPUS_LIBS)))

async def moduleErr(message, module, err):
    if silence:
        return
    msg = "_AwFuck_ ... My "+module+" Module has crashed\n"
    msg += "Please let my dads zain and jack know that i had error: `"+err+"`"
    await client.send_message(message.channel, msg)

async def playAudio(message, url):
    global player
    global vc
    if not discord.opus.is_loaded():
        load_opus_lib()
    author = message.author
    voice_channel = author.voice_channel
    if not voice_channel:
        await client.send_message(message.channel, "Sorry! I can't play any audio unless you are in a voice channel")
        return
    if player and player.is_playing():
        await client.send_message(message.channel, "Audio is currently already playing!")
        return
    if not vc:
        vc = await client.join_voice_channel(voice_channel)

    player = await vc.create_ytdl_player(url)
    player.start()

async def disconnectAudio(message):
    global player
    global vc
    if vc:
        if player:
            player.stop()
            player = None
        await vc.disconnect()
        vc = None
    else:
        await client.send_message(message.channel, "I'm not connected to a voice channel!")

async def stopAudio(message):
    global player
    if player:
        player.stop()
        await client.send_message(message.channel, "Audio Stopped")
    else:
        await client.send_message(message.channel, "There is no audio playing!")

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
            if "audio" in res:
                await playAudio(message, res["audio"])
            if "killAudio" in res and res["killAudio"]:
                await stopAudio(message)
            if "disconnect" in res and res["disconnect"]:
                await disconnectAudio(message)
            if len(res["channel_output"]) > 0:
                await channelOutput(message,res)
        except Exception as e:
            modules[1].crashes+=1
            await moduleErr(message,module.name,str(e))
            if debug:
                raise e

client.run(os.environ.get('BOT_TOKEN'))
client.close()
