import discord
import asyncio
from dbInterface import Database

# Globals
client = discord.Client()
database = Database('data.db')
commands = []
# commands

def newResultObject():
    res = {}
    res["err"] = False
    res["errMsg"] = ""
    res["output"] = False
    res["outputMsg"] = []
    res["response"] = "Noted."
    return res

def listCommand(channel, arg):
    phrases = database.allPhrases(channel)
    res = newResultObject()
    res["output"] = True
    raw = []
    raw.append("```")
    raw.append("Trigger                    | Response                    ")
    raw.append("=========================================================")
    raw.append("```")
    for phrase in phrases:
        raw.append(phrase[0].ljust(20)+"|"+phrase[1].ljust(10))
    res["outputMsg"].append("\n".join(raw))
    return res

def killCommand(channel, arg):
    res = newResultObject()
    if len(arg.strip()) == 0:
        res["err"] = True
        res["errMsg"] = "I may be a genius but i'm not psychic, you need to tell me what phrase to kill"
        return res
    elif not database.containsTrigger(channel, arg):
        res["err"] = True
        res["errMsg"] = "I haven't been told to keep track of that phrase, perhaps try to use your brain at more then 1\% power?"
        return res
    database.deletePhrase(channel, arg)
    res["response"] = "I won't mention the phrase again, but it will *always* be in my databanks along with everything else"
    return res

def helpCommand(channel, arg):
    res = newResultObject()
    res["output"] = True
    raw = []
    raw.append("```")
    raw.append("Command                    | Action                      ")
    raw.append("=========================================================")
    raw.append("!hodge list                | lists all phrases hodge is  ")
    raw.append("                           | keeping track of            ")
    raw.append("---------------------------------------------------------")
    raw.append("!hodge kill <phrase>       | removes a phrase from hodges")
    raw.append("                           | database                    ")
    raw.append("---------------------------------------------------------")
    raw.append("!hodge help                | displays this message       ")
    raw.append("---------------------------------------------------------")
    raw.append("!hodge on <t> say <s>      | tells hodge to say <s>      ")
    raw.append("                           | whenever <t> is mentioned   ")
    raw.append("=========================================================")
    raw.append("```")
    res["outputMsg"].append("\n".join(raw))
    return res

def regiserCommand(channel, arg):
    args = arg.split(" ")
    res = newResultObject()
    if args[-1] == "say" or "say" not in args:
        res["err"] = True
        res["errMsg"] = "You don't register as a child but your responses suggest otherwise, you have to give both a trigger AND a response phrase. !hodge on <trigger> say <response>"
        return res
    i = len(args)-1
    say = ""
    on = ""
    while args[i] != "say":
        say = args[i] + " " + say
        i-=1
    on = " ".join(args[:i])
    say = say.strip()
    on = on.strip()
    database.newPhrase(channel, on, say)
    return res

# Messagae Interperting Functions

async def isCommand(message):
    m = message.content.lower()
    args = m.split(" ")
    if len(args) < 2:
        return False
    if args[0] != "!hodge":
        return False
    if args[1] not in list(map(lambda x: x[0],commands)):
        return False
    if not message.author.permissions_in(message.channel).administrator:
        return False
    return True

async def runCommand(message):
    m = message.content.lower()
    c = m.split(" ")[1]
    arg = " ".join(m.split(" ")[2:])
    i = list(map(lambda x: x[0],commands)).index(c)
    res = commands[i][1](message.channel.id, arg)
    if res["err"]:
        await client.send_message(message.channel, res["errMsg"])
    elif res["output"]:
        for line in res["outputMsg"]:
            await client.send_message(message.channel, line)
    else:
        await client.send_message(message.channel, res["response"])

async def isQuestion(message):
    return False

async def answerQuestion(message):
    return None

async  def triggerResponse(message):
    phrases = database.allPhrases(message.channel.id)
    m = message.content.lower()
    output = []
    for phrase in phrases:
        if m.find(phrase[0]) != -1:
            output.append(phrase[1])
    if len(output) > 0:
        await client.send_message(message.channel, "\n".join(output))


# Discord event handlers
@client.event
async def on_ready():
    commands.append(("list", listCommand))
    commands.append(("on", regiserCommand))
    commands.append(("kill", killCommand))
    commands.append(("help",helpCommand))
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
    # attempt admin command parsing
    if await isCommand(message):
        await runCommand(message)
    # attempt question answering
    elif await isQuestion(message):
        await answerQuestion(message)
    # attempt to respond to triggers
    await triggerResponse(message)

client.run("Mzk1MzgyNzA0OTYwNzAwNDE2.DSSITw.Te0v0ti0k_xkpxG-vxqm-tKQVZs")
client.close()
