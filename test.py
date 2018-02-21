from bots.HodgePodge.modules.Game import Game
import re
import sys




def help(helpObj):
    response = []
    response.append("Here's some of the commands you can use with me!")
    for l in helpObj["cmds"]:
        response.append("**%s**"%l[0])
        response.append("%s"%l[1])
        response.append("`%s`"%l[2])
        response.append("")
    response.append("Check out the documentation if you want some more info!\n%s"%helpObj["docs"])
    response = "\n".join(response)
    print(response)


modules = {
    "game":Game()
}

if len(sys.argv) < 3:
    print("Usage: ./test <module> <level>")
    exit(1)
moduleName = sys.argv[1]
level = int(sys.argv[2])
if moduleName.lower() in modules:
    module = modules[moduleName.lower()]
    module.connectDb(None)
else:
    print("Testing system has not been set up with module '%s'"%module)
    exit(0)

print(">> Booting...")
triggerList = module.getTriggerList()
print(">> Ready.")
cmd = ""
while cmd != "done":
    inputStr = input().lower()
    if inputStr == "hodge podge help with "+moduleName:
        help(module.getHelp())
        continue
    for t in triggerList:
        s = re.search(t["trigger"],inputStr)
        if level >= t["accessLevel"] and s:
            if "id" in t:
                t["function"]({"id":tId,"args":s.groups()})
            else:
                t["function"]({"args":s.groups()})
            module.respond(None,None)
