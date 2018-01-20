import psycopg2
import urllib.parse as urlparse
import os

class Db():
    def __init__(self):
        url = urlparse.urlparse(os.environ['DATABASE_URL'])
        dbname = url.path[1:]
        user = url.username
        password = url.password
        host = url.hostname
        port = url.port
        self.conn = psycopg2.connect(dbname=dbname,user=user,password=password,host=host,port=port)

    def removeDuplicates(self, l):
        result = []
        for e in l:
            if e not in result:
                result.append(e)
        return result

    def formStrictFilters(self, r, query, caseIns):
        query += " WHERE "
        for i,fil in enumerate(r["WHERE"].keys()):
            if i == 0 and caseIns:
                query += (" UPPER(%s) = %s"%(fil,r["WHERE"][fil].upper())
            elif caseIns:
                query += (" AND UPPER(%s) = %s"%(fil,r["WHERE"][fil].upper())
            elif i == 0:
                query += (" %s = %s"%(fil,r["WHERE"][fil]))
            else:
                query += (" AND %s = %s"%(fil,r["WHERE"][fil]))
        return query

    def formSearchFilters(self, r, query, caseIns):
        query += " WHERE "
        for i,fil in enumerate(r["WHERE"].keys()):
            if i == 0 and caseIns:
                query += (" UPPER(%s) LIKE %%s"%fil)
                params.append(r["WHERE"][fil].upper())
            elif caseIns:
                query += (" AND UPPER(%s) LIKE %%s"%fil)
                params.append(r["WHERE"][fil].upper())
            elif i == 0:
                query += (" %s LIKE %%s"%fil)
                params.append(r["WHERE"][fil])
            else:
                query += (" AND %s LIKE %%s"%fil)
                params.append(r["WHERE"][fil])
        return (query,params)

    def exists(self, table, fields, r):
        query = "SELECT %s FROM %s"%(fields, table)
        query = formStrictFilters(r,query,True)
        c = self.conn.cursor()
        c.execute(query)
        if c.fetchone() != None:
            return False
        else:
            return True

    def edit(self, r):

        # basic params
        c = self.conn.cursor()
        force = r.get("FORCE",False)
        ret = r.get("RETURN","NEW")
        # get query Basics
        if "TABLE" not in r or "SET" not in r:
            raise Exception("No Table or Field Specified")
        fields = map(lambda x: x.upper(), r["SET"])
        fields = ", ".join(fields)
        table = r["TABLE"]
        exists = self.exists(table,fields,r)

        if exists:

        elif not exists and force:

        else:
            raise Exception("No Matching Entry To Update, Use force=true To Create Entry")

        if ret == "OLD":
            return old
        else:
            return new

    def search(self, r):
        # basic params
        c = self.conn.cursor()
        caseIns = r.get("CASE_INS",True)
        dups = r.get("DUPS",False)

        # form base query
        if "TABLE" not in r or "GET" not in r:
            raise Exception("No Table or Field Specified")
        fields = map(lambda x: x.upper(), r["GET"])
        fields = ", ".join(fields)
        table = r["TABLE"]
        query = "SELECT %s FROM %s"%(fields, table)
        params = None

        # form filters
        if "WHERE" in r and len(r["WHERE"].keys()) > 0:
            filters = self.formSearchFilters(r,query, caseIns)
            query = filters[0]
            params = filters[1]
        # Execute
        if params != None
            c.execute(query,tuple(params))
        else:
            c.execute(query)
        results = c.fetchAll()
        if not dups:
            results = removeDuplicates(results)
        return results

    # NOT TO BE USED FOR USER INPUT
    # USE SEARCH BECAUSE IT SANTISES INPUT
    def get(self, r):
        # basic params
        c = self.conn.cursor()
        caseIns = r.get("CASE_INS",True)
        dups = r.get("DUPS",False)

        # form base query
        if "TABLE" not in r or "GET" not in r:
            raise Exception("No Table or Field Specified")
        fields = map(lambda x: x.upper(), r["GET"])
        fields = ", ".join(fields)
        table = r["TABLE"]
        query = "SELECT %s FROM %s"%(fields, table)

        # form filters
        if "WHERE" in r and len(r["WHERE"].keys()) > 0:
            query = self.formStrictFilters(query, caseIns)
        # Execute
        c.execute(query)
        results = c.fetchAll()
        if not dups:
            results = removeDuplicates(results)
        return results
