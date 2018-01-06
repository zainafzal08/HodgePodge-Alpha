from modules.Module import Module
import re
import random

class Spells(Module):
    def __init__(self, db):
        super().__init__("Spells")
        self.db = db
        self.spellSearchLevel = 0
        self.commands = [
            ("hodge podge whats .*$",self.isValidCommand,self.basicSearch),
            ("hodge podge describe .*$",self.isValidCommand,self.basicSearch),
            ("hodge podge list .* spells$",self.valid,self.advancedSearch),
            ("hodge podge how do i search spells$",self.valid,self.searchHelp),
        ]
        self.classes = [
            "barbarian",
            "bard",
            "cleric",
            "druid",
            "fighter",
            "monk",
            "paladin",
            "ranger",
            "sorcerer",
            "rogue",
            "warlock",
            "wizard"
        ]
        self.schools = [
            "abjuration",
            "conjuration",
            "divination",
            "enchantment",
            "evocation",
            "illusion",
            "necromancy",
            "transmutation",
            "universal"
        ]

    def searchHelp(self, message):
        result = []
        result.append("To Search spells just say `hodge podge list <search params> spells`")
        result.append("You can search spells by level, components, concentration, spellRange, ritual, school and class")
        result.append("")
        result.append("`hodge podge list transmutation level 5 concentration no ritual druid spells`")
        res = super().blankRes()
        res["output"].append("\n".join(result))
        return res

    def isValidCommand(self, message, level):
        if level < self.spellSearchLevel:
            return False
        s = re.search("hodge podge whats (.*)$",self.clean(message.content))
        if not s:
            s = re.search("hodge podge describe (.*)$",self.clean(message.content))
        spell = self.shallowClean(s.group(1))
        if len(spell.split(" ")) > 7:
            return False
        return True

    def valid(self, message, level):
        if level < self.spellSearchLevel:
            return False
        return True

    def getClass(self, m):
        for spellClass in self.classes:
            if re.search(spellClass, m):
                return spellClass
        return None

    def getSchool(self, m):
        for school in self.schools:
            if re.search(school, m):
                return school
        return None

    def advancedSearch(self, message):
        s = re.search("hodge podge list (.*) spells$",self.clean(message.content))
        params = self.clean(s.group(1))
        m = self.clean(message.content)
        search = {}
        res = super().blankRes()

        if re.search("concentration",m):
            search["CONCENTRATION"] = "Requires Concentration"
        elif re.search("no concentration",m):
            search["CONCENTRATION"] = "Requires No Concentration"
        if re.search("ritual",m):
            search["RITUAL"] = "Is a Ritual"
        elif re.search("no ritual",m):
            search["RITUAL"] = "Is Not a Ritual"
        if re.search("level \d+",m):
            search["LEVEL"] = re.search("level (\d+)",m).group(1)
        spellClass = self.getClass(m)
        school = self.getSchool(m)
        if spellClass:
            search["CLASSES"] = spellClass
        if school:
            search["SCHOOL"] = school

        results = self.db.spellSearch(search)
        random.shuffle(results)
        if len(results) == 0:
            res["output"].append("Sorry friend! I got no results")
        elif len(results) == 1:
            res["output"].append(self.formatSpell(results[0]))
        else:
            res["output"].append("I found a couple of spells that might do the trick")
            # this needs to be a bit smarter
            output = []
            output.append("```")
            for i,spell in enumerate(results):
                if i > 15:
                    break
                output.append(spell[0])
                output.append("    Lvl. "+spell[7])
                output.append("    Sch. "+spell[9])
                output.append("    Cls. "+spell[11])
            output.append("```")
            if len(results) > 15:
                output.append("...Plus more that i don't have room to display! Try narrowing your search a bit")
            res["output"].append("\n".join(output))
        return res

    def formatSpell(self, e):
        result = []
        result.append("```")
        result.append(">> "+e[0])
        result.append("="*(len(e[0])+3))
        result.append("")
        result.append("Concentration  | "+ e[1])
        result.append("Page           | " + e[2])
        result.append("Range          | " + e[3])
        result.append("Components     | " + e[4])
        result.append("Ritual         | " + e[5])
        result.append("Duration       | " + e[6])
        result.append("Level          | " + e[7])
        result.append("Casting Time   | " + e[8])
        result.append("School         | " + e[9])
        result.append("Classes        | " + e[11])
        result.append("```")
        result.append(e[10])
        return "\n".join(result)

    def basicSearch(self, message):
        s = re.search("hodge podge whats (.*)$",self.clean(message.content))
        if not s:
            s = re.search("hodge podge describe (.*)$",self.clean(message.content))
        spell = self.shallowClean(s.group(1))
        results = self.db.spellGet(spell)
        res = super().blankRes()
        if len(results) == 0:
            res["output"].append("Sorry friend! I have no idea what spell you are talking about")
        elif len(results) == 1:
            res["output"].append(self.formatSpell(results[0]))
        else:
            res["output"].append("I have multiple entires for that! Which one did you mean?")
            res["output"].append("```"+("\n".join(map(lambda x: ":::> "+x[0],results)))+"```")
        return res

    def clean(self, t):
        m = t.lower()
        m = re.sub(r'\s+',' ',m)
        m = re.sub(r'[\,\.\?\;\:\%\#\@\!\^\&\*\+\-\+\_\~\']','',m)
        m = m.strip()
        return m

    def shallowClean(self, t):
        return t.strip().lower()

    def trigger(self, message, requestLevel):
        res = super().blankRes()
        original = message.content;
        m = self.clean(message.content)
        for command in self.commands:
            if re.search(command[0],m) and command[1](message,requestLevel):
                res = command[2](message)
        return res
