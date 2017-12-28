import discord
import asyncio
import re
import random
from dbInterface import Database

# Globals
client = discord.Client()
database = Database('data.db')
commands = []
questionTriggerPhrases = []
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
    raw.append("Trigger                    | Response                   ")
    raw.append("========================================================")
    for phrase in phrases:
        raw.append(phrase[0].ljust(27)+"| "+phrase[1].ljust(27))
    raw.append("```")
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

def extractQuestion(t):
    m = t.lower()
    m = re.sub(r'\s+',' ',m)
    m = re.sub(r'[\,\.\?\;\:\%\#\@\!\^\&\*\+\-\+\_\~\']','',m)
    m = m.strip()
    return m

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
    m = extractQuestion(message.content)
    for trigger in list(map(lambda x: x[0], questionTriggerPhrases)):
        try:
            q = " ".join(m.split(" ")[0:len(trigger.split(" "))])
        except:
            continue
        if q == trigger:
            return trigger
    return None

async def answerQuestion(question, message):
    # grab relevant info
    m = extractQuestion(message.content)
    search = " ".join(m.split(" ")[len(question.split(" ")):])
    questionObj = questionTriggerPhrases[list(map(lambda x: x[0], questionTriggerPhrases)).index(question)]
    field = questionObj[1]
    if field != None:
        results = database.searchSpell(search, field)
    else:
        results = []
    output = []
    block = False

    # check if this is a instant response
    if questionObj[2] != None:
        output.append(questionObj[2])
    # form response
    elif len(results) == 0:
        output.append("*Flames shoot from the floor*\nMy database doesn't contain relevant information, thus the question must be incorrect\n Try asking me to look up just key words like `wall` or `fire` to see some options")
    elif len(results) == 1:
        block = True
        results = results[0]
        output.append(">> "+results["name"])
        output.append("="*(len(results["name"])+5))
        output.append("\nLevel      | "+str(results["level"]))
        output.append("School     | "+results["school"])
        output.append("Casting    | "+results["casting_time"])
        output.append("Components | "+results["components"])
        output.append("Duration   | "+results["duration"])
        output.append("Range      | "+results["range"])
        output.append("Classes    | "+results["classes"]+"\n")
        output.append(results["description"])
        output.append("\nAt a higher Level: "+results["at_higher_levels"])
    else:
        block = True
        output.append("I have multiple entries for that!                              ")
        output.append("===============================================================")
        if len(results) > 10:
            random.shuffle(results)
            results = results[:10]
        for row in results:
            name = row["name"]
            school = row["school"]
            level = "Lv. "+str(row["level"])
            output.append(name.ljust(33)+"| "+school.ljust(13)+"| "+level.ljust(13))

    # respond
    if block:
        output = ["```"] + output + ["```"]
    await client.send_message(message.channel, "\n".join(output))


async def triggerResponse(message):
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
    questionTriggerPhrases.append(("hey hodge podge whats","NAME",None))
    questionTriggerPhrases.append(("hey hodge podge describe","NAME",None))
    questionTriggerPhrases.append(("hey hodge podge",None,"Hello! I am here to help you learn!\nask me to *describe* a spell like `hey hodge podge describe passwall`"))
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
        return
    # attempt question answering
    question = await isQuestion(message)
    if question != None:
        await answerQuestion(question, message)
    # attempt to respond to triggers
    await triggerResponse(message)

client.run("Mzk1MzgyNzA0OTYwNzAwNDE2.DSSITw.Te0v0ti0k_xkpxG-vxqm-tKQVZs")
client.close()
