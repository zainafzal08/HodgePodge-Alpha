import json
import re

f = open("formattedSpells.json","r")
toFix = json.load(f)
f.close()

f = open("spell.json","r")
reference = json.load(f)
f.close()

fixed = []

for e in toFix:
    e["classes"] = ", ".join(reference[e["name"]]["class"].keys())
    fixed.append(e)

f = open("formattedSpells.json","w")
json.dump(fixed, f)
f.close()
