import psycopg2
import urllib.parse as urlparse
import os
import json
from tqdm import tqdm

url = urlparse.urlparse(os.environ['DATABASE_URL'])
dbname = url.path[1:]
user = url.username
password = url.password
host = url.hostname
port = url.port
conn = psycopg2.connect(dbname=dbname,user=user,password=password,host=host,port=port)

c = conn.cursor()

f = open("formattedSpells.json","r")
j = json.load(f)
f.close()

for e in tqdm(j):
    new = e
    v = (new["name"],new["concentration"],new["page"],new["range"],new["components"],new["ritual"],new["duration"],new["level"],new["castingTime"],new["school"],new["description"],new["classes"])
    c.execute("INSERT INTO SPELLS VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",v)

conn.commit()
