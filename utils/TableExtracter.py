def extract(raw, idName):
    table = getTable(raw, idName)
    if len(table) == 0:
        return None
    # we don't care about the first 2 lines
    table = table[2:]
    result = []
    for l in table:
        # get rid of pipes on either end
        l = l[1:-1]
        l = l.strip()
        l = l.split("|")
        result.append(tuple(l))
    return result

def getTable(raw, idName):
    active = False
    buff = []
    for l in raw.split("\n"):
        l = l.strip()
        if l == ("!!start %s command list"%idName):
            active = True
        elif l == ("!!end %s command list"%idName):
            active = False
            break
        elif active:
            buff.append(l)
    return buff
