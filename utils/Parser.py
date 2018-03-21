import re
from utils.Response import Response

class Match():

    def __init__(self, m, rgx, acs,f,v):
        self.module = m
        self.regex = re.compile(rgx)
        self.access = acs
        self.function = f
        self.context = {}
        self.context["groups"] = None
        self.context["locationId"] = None
        self.context["raw"] = None
        self.context["userRoles"] = None
        self.validation = list(map(lambda x: getattr(m,x),v))

    def trigger(self):
        valid = True
        err = None
        for i,g in enumerate(self.context["groups"]):
            if i < len(self.validation) and self.validation[i] and not self.validation[i][0](g):
                valid = False
                err = self.validation[i][1]
        if valid:
            return getattr(self.module,self.function)(self.context)
        else:
            res = Response()
            res.textResponce("Sorry! %s"%err,self.context["locationId"],"err")
            return (res,None)

class Parser():
    def __init__(self):
        self.triggers = []
        pass

    def register(self, m, rgx, acs, f, v):
        match = Match(m,rgx,acs,f, v)
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
