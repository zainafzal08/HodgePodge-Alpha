def extract(raw, idName):
    table = getTable(raw, idName)
    if len(table) == 0:
        return None
    # ignore first 2 lines
    result = []
    table = table[2:]
    for l in table:
        # get rid of pipes on either end
        l = l[1:-1]
        l = l.strip()
        l = l.split("|")
        result.append(tuple(map(lambda x: x.strip(),l)))
    return result

def getTable(raw, idName):
    active = False
    buff = []
    startTrigger = "!!start %s command list"%idName
    endTrigger = "!!end %s command list"%idName
    for l in raw.split("\n"):
        l = l.strip()
        if l == startTrigger:
            active = True
        elif l == endTrigger:
            active = False
            break
        elif active:
            if len(l.strip()) != 0:
                buff.append(l)
    return buff
