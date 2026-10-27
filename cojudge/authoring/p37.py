import random
REFERENCE = '''import sqlite3

def solve(data: dict) -> dict:
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE document (id INTEGER PRIMARY KEY, value TEXT, version INTEGER)")
    db.execute("INSERT INTO document VALUES (1, ?, ?)", (data["value"], data["version"]))
    db.commit()
    results = []
    for op in data["updates"]:
        with db:
            count = db.execute("UPDATE document SET value = ?, version = version + 1 WHERE id = 1 AND version = ?", (op["value"], op["expected"])).rowcount
        results.append(count == 1)
    value, version = db.execute("SELECT value, version FROM document WHERE id = 1").fetchone()
    db.close()
    return {"accepted": results, "value": value, "version": version}
'''
def op(expected, value="new"):
    return {"expected": expected, "value": value}
def c(version, value, updates, accepted, final, end, label):
    return {"input": {"version": version, "value": value, "updates": updates}, "expected": {"accepted": accepted, "value": final, "version": end}, "label": label}
CASES = [
    c(0,"old",[op(0)],[True],"new",1,"matching version updates"),
    c(2,"old",[op(1)],[False],"old",2,"stale writer is rejected"),
    c(0,"old",[op(0,"one"),op(0,"two")],[True,False],"one",1,"two readers share a version"),
    c(0,"",[],[],"",0,"no updates"),
    c(4,"same",[op(4,"same")],[True],"same",5,"same value still advances version"),
    c(0,"a",[op(1,"b")],[False],"a",0,"future version is rejected"),
    c(3,"a",[op(3,"b"),op(4,"c")],[True,True],"c",5,"sequential writers"),
    c(3,"a",[op(2),op(3,"c")],[False,True],"c",4,"rejection does not advance version"),
    c(1,"a",[op(1,""),op(2,"z")],[True,True],"z",3,"empty text value"),
    c(8,"a",[op(0),op(9),op(8,"yes")],[False,False,True],"yes",9,"only exact version matches"),
    c(0,"a",[op(0,"quoted \"text\"")],[True],'quoted "text"',1,"text uses SQL parameters"),
    c(10,"start",[op(10,"x"),op(10,"y"),op(11,"z"),op(11,"q")],[True,False,True,False],"z",12,"retry uses refreshed version"),
]
rng = random.Random(37)
SPEC={"number":37,"slug":"sql-optimistic-locking","title":"Reject stale SQL updates","difficulty":"Medium","time":25,
"prerequisites":"SQL UPDATE and transaction basics.",
"learn":"A client can read a document and then write after another client has changed it. A version number lets the database detect that stale write. The client sends the version it read. One UPDATE statement checks that version, changes the value, and increments the version. If the statement changes no rows, the client must refresh its data before it retries. Checking the version in a separate read is not the same guarantee: another writer could run between the read and write. This exercise supplies an ordered trace of client proposals. Even a write of the same value counts as an accepted update and advances the version.",
"task":('**Input:** `data` has:\n'
    '- `value`: the initial document string.\n'
    '- `version`: its initial integer version.\n'
    '- `updates`: a list of `{"value": string, "expected": int}`.\n'
    '\n'
    '**Rules:** for each update:\n'
    '- Accept it only when `expected` is equal to the current version. Then replace the value and add 1 to the version.\n'
    '- A rejected update changes nothing.\n'
    '\n'
    '**Return** `{"accepted": [bool], "value": string, "version": int}`.\n'
    '\n'
    'Complete the SQL update loop in the scaffold. This is a sequential trace, not a test of real parallel execution. The judge cannot check SQL syntax or structure.'),
"constraints":["0–200 updates. Versions and expected versions are 0–1000000.","Values are ASCII strings of length 0–100."],
"hints":["Put the expected version in the UPDATE predicate.","Use the affected-row count to produce the Boolean result."],
"starter":REFERENCE[:REFERENCE.index('    results = []')]+'    # TODO: execute conditional updates and return accepted/value/version.\n    raise NotImplementedError\n',
"reference":REFERENCE,
"java":'''public Object solve(Map<String,Object> d) { String value=s(d.get("value")); long version=lng(d.get("version")); List<Object> results=new ArrayList<>(); for(Object raw: arr(d.get("updates"))) {Map<String,Object> op=obj(raw); boolean ok=lng(op.get("expected"))==version; results.add(ok); if(ok) {value=s(op.get("value")); version++;}} return map("accepted",results,"value",value,"version",version); }''',
"approach":"Use one conditional UPDATE per proposal, with the version increment in the same statement. The one-row table makes processing O(U), plus output storage O(U). Real conflicts may require a new read and a business decision; blindly retrying an old value can still discard intent.",
"cases":CASES,"generated":[{"value":"seed"+str(i),"version":i,"updates":[op(rng.randrange(0,i+12),"value"+str(j)) for j in range(25)]} for i in range(24)],
"mutations":[{"name":"accepts stale versions","old":"AND version = ?","new":"AND version >= ?"}],
"sources":["https://www.sqlite.org/lang_update.html","https://docs.python.org/3.11/library/sqlite3.html"]}
