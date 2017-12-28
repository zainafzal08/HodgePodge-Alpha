import sqlite3
import json

conn = sqlite3.connect("data.db")
c = conn.cursor()
f = open("spells.json")
j = json.load(f)
f.close()

for e in j:
    nme = e["name"].strip()
    sch = e["school"].strip()
    lvl = e["level"]
    cst = e["casting_time"].strip()
    cmp = e["components"].strip()
    dur = e["duration"].strip()
    rng = e["range"].strip()
    cla = ", ".join(e["classes"]).strip()
    dsr = e["description"].strip()
    ahl = e["at_higher_levels"].strip()
    data = (nme,sch,lvl,cst,cmp,dur,rng,cla,dsr,ahl)

    c.execute("SELECT * FROM SPELLS WHERE NAME = ?",(nme,))
    if(c.fetchone() != None):
        print("DUPLICATE NAME: "+nme)
    else:
        c.execute("INSERT INTO SPELLS VALUES (?,?,?,?,?,?,?,?,?,?)", data)
conn.commit()
