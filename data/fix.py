import json
import re
import requests
import urllib
import bs4
from tqdm import tqdm
from bs4 import BeautifulSoup

f = open("formattedSpells.json","r")
j = json.load(f)
f.close()

def clean(t):
    t = re.sub('\s+',' ',t)
    t = re.sub('^\s+$','',t)
    t = re.sub('\n','',t)
    return t.strip()

def superClean(t):
    t = clean(t)
    t = re.sub("<[^<>]+>","",t)
    t = re.sub("<\/[^<>]+>","",t)
    t = clean(t)
    return t.strip()
def getDesc(name):
    url = "https://thebombzen.com/grimoire/spells/"
    spell = re.sub(' ','-',name.lower())
    spell = re.sub('\'','',spell)
    r = requests.get(url+spell)
    if r.status_code != 200:
        return "::!!:: page grab failed: "+(url+spell)+" ::!!::"
    try:
        raw = r.text
        soup = BeautifulSoup(raw, 'html.parser')
        res = soup.find_all("article", class_="post-content")[0]
        final = []
        for child in res.children:
            if re.search("<strong>",str(child)):
                continue
            elif len(clean(str(child))) != 0:
                final.append(superClean(str(child)))
        return "\n".join(final)
    except Exception as e:
        raise e
        return "::!!:: class find failed ::!!::"

fixed = []
for e in tqdm(j):
    if e["description"] == "No Description Available":
        e["description"] = getDesc(e["name"])
    fixed.append(e)

f = open("formattedSpells.json","w")
json.dump(fixed, f)
f.close()
