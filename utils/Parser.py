import re

class Match():
    def __init__(self, m, rgx, acs,f):
        self.module = m
        self.regex = re.compile(rgx)
        self.access = acs
        self.function = f
        self.context = {}
        self.context["groups"] = None
        self.context["locationId"] = None
        self.context["raw"] = None
        self.context["userRoles"] = None
    def trigger(self):
        return getattr(self.module,self.function)(self.context)

class Parser():
    def __init__(self):
        self.triggers = []
        pass

    def register(self, m, rgx, acs, f):
        match = Match(m,rgx,acs,f)
        self.triggers.append(match)

    def permission(self, roles, access):
        if len(access) == 0:
            return True
        for r in roles:
            if r in access:
                return True
        return False

    def parse(self, message,roles,locationId):
        m = message.lower()
        for trigger in self.triggers:
            s = trigger.regex.search(m)
            if s and self.permission(roles,trigger.access):
                trigger.context["groups"] = s.groups()
                trigger.context["raw"] = message
                trigger.context["locationId"] = locationId
                trigger.context["userRoles"] = roles
                return trigger
            else:
                continue
        return None
