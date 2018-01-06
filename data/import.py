import json
import re
import requests
import urllib
from tqdm import tqdm

def inPrint(s):
    print(":::> %s"%str(s))

f = open("spell.json","r")
j = json.load(f)
f.close()


def getDesc(name):
    f = {}
    f["name"] = name
    l = "https://donjon.bin.sh/5e/spells/rpc.cgi?"+urllib.parse.urlencode(f)
    raw = requests.get(l).text
    j = json.loads(raw)
    try:
        return j["Description"]
    except Exception as e:
        return "No Description Available"
final = []
for name in tqdm(j):
    concen = "Requires%sConcentration"%(" No " if j[name]["concentration"] == "no" else " ")
    page = "@ %s"%(re.sub("(\d+)","Page \g<1>",(" and".join(j[name]["page"].split(",")))))
    sRange = j[name]["range"]
    components = re.sub("V","(V)",j[name]["components"])
    components = re.sub("S","(S)",components)
    components = re.sub("M","(M)",components)
    components =re.sub("gp","(gp)",components)
    ritual = "Is%sRitual"%(" Not a " if j[name]["concentration"] == "no" else " a ")
    duration = j[name]["duration"]
    castingTime = j[name]["casting_time"]
    level = re.search("(\d+)",j[name]["level"])
    description = getDesc(name)
    if not level:
        level = 0
    else:
        level = int(level.group(1))
    school = j[name]["school"]
    new = {}
    new["name"] = name
    new["concentration"] = concen
    new["page"] = page
    new["range"] = sRange
    new["components"] = components
    new["ritual"] = ritual
    new["duration"] = duration
    new["level"] = level
    new["castingTime"] = castingTime
    new["school"] = school
    new["description"] = description
    final.append(new)

f = open("formattedSpells.json","w")
json.dump(final, f)
f.close()
