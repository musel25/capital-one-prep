"""Unique keys, parameterized insertion, and stable conflict semantics."""
SCAFFOLD='''import sqlite3

def solve(data):
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    try:
        connection.execute("CREATE TABLE accounts(username TEXT PRIMARY KEY NOT NULL, quota INTEGER NOT NULL)")
        connection.executemany("INSERT INTO accounts VALUES (?, ?)", [(r["username"], r["quota"]) for r in data["initial"]])
        responses = [create_account(connection, r["username"], r["quota"]) for r in data["requests"]]
        rows = [dict(r) for r in connection.execute("SELECT username, quota FROM accounts ORDER BY username ASC")]
        return {"responses": responses, "accounts": rows}
    finally:
        connection.close()

'''
QUERY='''def create_account(connection, username, quota):
    cursor = connection.execute("INSERT INTO accounts(username, quota) VALUES (?, ?) ON CONFLICT(username) DO NOTHING", (username, quota))
    record = dict(connection.execute("SELECT username, quota FROM accounts WHERE username = ?", (username,)).fetchone())
    status = 201 if cursor.rowcount == 1 else (200 if record["quota"] == quota else 409)
    return {"status": status, "record": record}
'''
JAVA='''public Object solve(Map<String,Object> d){
    TreeMap<String,Integer> accounts=new TreeMap<>();for(Object value:arr(d.get("initial"))){Map<String,Object> r=obj(value);accounts.put(s(r.get("username")),n(r.get("quota")));}List<Object> responses=new ArrayList<>();
    for(Object value:arr(d.get("requests"))){Map<String,Object> r=obj(value);String username=s(r.get("username"));int quota=n(r.get("quota")),status;
        if(!accounts.containsKey(username)){accounts.put(username,quota);status=201;}else status=accounts.get(username)==quota?200:409;
        responses.add(map("status",status,"record",map("username",username,"quota",accounts.get(username))));}
    List<Object> rows=new ArrayList<>();for(Map.Entry<String,Integer> e:accounts.entrySet())rows.add(map("username",e.getKey(),"quota",e.getValue()));return map("responses",responses,"accounts",rows);
}'''
def row(user,quota=10):return {"username":user,"quota":quota}
def response(status,user,quota=10):return {"status":status,"record":row(user,quota)}
def case(initial,requests,responses,accounts,label):return {"input":{"initial":initial,"requests":requests},"expected":{"responses":responses,"accounts":accounts},"label":label}
CASES=[case([],[row("ada"),row("ada")],[response(201,"ada"),response(200,"ada")],[row("ada")],"duplicate identical create is a replay"),case([row("ada")],[row("ada",20)],[response(409,"ada")],[row("ada")],"conflicting quota preserves original"),case([],[row("O'Reilly")],[response(201,"O'Reilly")],[row("O'Reilly")],"quote in bound username"),case([],[],[],[],"empty database and requests"),case([row("b"),row("a")],[],[],[row("a"),row("b")],"final rows ordered even with no writes"),case([],[row("a",0)],[response(201,"a",0)],[row("a",0)],"zero quota"),case([],[row("a",1000000)],[response(201,"a",1000000)],[row("a",1000000)],"maximum quota"),case([],[row("a"),row("A")],[response(201,"a"),response(201,"A")],[row("A"),row("a")],"case-sensitive uniqueness"),case([row("a")],[row("a",11),row("a")],[response(409,"a"),response(200,"a")],[row("a")],"conflict does not replace stored value"),case([],[row("'; DROP TABLE accounts; --"),row("safe")],[response(201,"'; DROP TABLE accounts; --"),response(201,"safe")],[row("'; DROP TABLE accounts; --"),row("safe")],"SQL-looking username remains data"),case([row("a",0)],[row("a",0)],[response(200,"a",0)],[row("a",0)],"existing zero quota compares by value"),case([],[row("a")]*3,[response(201,"a"),response(200,"a"),response(200,"a")],[row("a")],"repeated requests do not add rows"),case([row("a")],[row("b",20),row("a",10),row("c",30)],[response(201,"b",20),response(200,"a"),response(201,"c",30)],[row("a"),row("b",20),row("c",30)],"new and existing accounts interleave")]
GENERATED=[{"initial":[row(f"user{j}",j+i) for j in range(i%5)],"requests":[row(f"user{j%6}",(j+i)%11) for j in range(i+2)]+[row(f"quoted'{i}",i)]} for i in range(18)]
SPEC={"number":34,"slug":"sql-unique-create","title":"Create accounts with stable conflict rules","difficulty":"Medium","time":35,"prerequisites":"Problems 24 and 31–33; replay semantics, SQLite placeholders, and queries.","learn":"A unique database constraint is the final guard against duplicate keys. Checking for a row in application code before inserting it is not enough when concurrent writers exist. An insert can instead use a conflict policy tied to the unique key. This exercise keeps the first stored value. The application then distinguishes a matching repeated request from a request that tries to change that value. Use bound parameters even when the schema is small. Quotes and SQL punctuation can appear in a valid username. The simulation is sequential, so it demonstrates the constraint and result policy without claiming to test concurrent transactions or durable storage.","task":('Complete `create_account(connection, username, quota)` in the SQLite scaffold. The table has `username TEXT PRIMARY KEY NOT NULL` and `quota INTEGER NOT NULL`. Text comparison is case-sensitive (the default).\n'
    '\n'
    '**Input:** `data` has:\n'
    '- `initial`: a list of `{"username": string, "quota": int}`, with unique usernames.\n'
    '- `requests`: a list of records with the same shape. Usernames can repeat.\n'
    '\n'
    '**Rules:** for each request:\n'
    '- New username → insert the row and return `{"status": 201, "record": stored row}`.\n'
    '- Existing username, same quota → status 200.\n'
    '- Existing username, different quota → status 409.\n'
    '- In both existing cases, do not change the row, and return its original record.\n'
    '\n'
    '**Return:** the scaffold returns `{"responses": [...], "accounts": [...]}`, with the responses in request order and the final accounts in username order.\n'
    '\n'
    '**Practice:** use a parameterized insert with a uniqueness conflict policy, and a parameterized lookup. The reference runs SQLite. The judge cannot check SQL use or parameter binding.'),"constraints":["0–200 initial accounts and 0–300 requests. Initial usernames are unique with exact case.","Usernames have 1–80 printable ASCII characters; quotes, spaces, and SQL punctuation are valid.","Quota is an integer from 0 through 1000000. All records contain exactly username and quota."],"hints":["ON CONFLICT(username) DO NOTHING preserves an existing row.","Read the stored row after the insert attempt, then compare its quota with the requested quota."],"starter":SCAFFOLD+"def create_account(connection, username, quota):\n    raise NotImplementedError\n","reference":SCAFFOLD+QUERY,"java":JAVA,"approach":"The primary key enforces uniqueness. INSERT with a targeted DO NOTHING conflict clause avoids replacing a row. rowcount separates creation from an existing key, and a lookup determines replay versus conflict. Indexed inserts and lookups take about O(log n) each; final ordering is O(n log n) at worst. Production code must define transaction, concurrency, and durability requirements separately.","cases":CASES,"generated":GENERATED,"mutations":[{"name":"overwrite quota on duplicate username","old":"ON CONFLICT(username) DO NOTHING","new":"ON CONFLICT(username) DO UPDATE SET quota = excluded.quota"}],"sources":["https://www.sqlite.org/lang_upsert.html","https://docs.python.org/3.11/library/sqlite3.html#how-to-use-placeholders-to-bind-values-in-sql-queries"]}
