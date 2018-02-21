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
        if "WHERE" not in r:
            return query
        elif len(r["WHERE"].keys()) < 1:
            return query

        query += " WHERE "
        for i,fil in enumerate(r["WHERE"].keys()):
            if i == 0 and caseIns:
                query += (" UPPER(%s) = %s"%(fil,r["WHERE"][fil].upper()))
            elif caseIns:
                query += (" AND UPPER(%s) = %s"%(fil,r["WHERE"][fil].upper()))
            elif i == 0:
                query += (" %s = %s"%(fil,r["WHERE"][fil]))
            else:
                query += (" AND %s = %s"%(fil,r["WHERE"][fil]))
        return query

    def formSearchFilters(self, r, query, caseIns):
        if "WHERE" not in r:
            return (query,[])
        elif len(r["WHERE"].keys()) < 1:
            return (query,[])
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
        if c.fetchone():
            return True
        return False

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
        old = None
        new = None
        if exists:
            for i,f in enumerate(map(lambda x: x.upper(), r["SET"])):
                fieldPairs.append("%s = %s"%(f,r["VALUE"][i]))
            fieldPairs = ",".join(fieldPairs)
            query = "UPDATE %s SET %s"%(table,fieldPairs)
            query = formStrictFilters(r,query,True)
            oldQuery = "SELECT * FROM %s"%table
            oldQuery = formStrictFilters(r,oldQuery,True)
            old = c.execute(oldQuery)
            c.execute(query)
            self.conn.commit()
        elif not exists and force:
            cols = map(lambda x: x.upper(), r["SET"])
            query = "INSERT INTO %s (%s) VALUES (%s)"%(table,", ".join(cols),", ".join(r["VALUES"]))
            self.c.execute(query)
            self.conn.commit()
            newQuery = "SELECT * FROM %s"%table
            newQuery = formStrictFilters(r,newQuery,True)
            new = c.execute(newQuery)
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
        filters = self.formSearchFilters(r,query, caseIns)
        query = filters[0]
        params = filters[1]

        # Execute
        if params != None:
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
        query = self.formStrictFilters(query, caseIns)

        # Execute
        c.execute(query)
        results = c.fetchAll()
        if not dups:
            results = removeDuplicates(results)
        return results
