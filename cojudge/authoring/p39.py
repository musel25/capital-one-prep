import random
REFERENCE='''import sqlite3

def solve(data: dict) -> dict:
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE items(id TEXT PRIMARY KEY, qty INTEGER CHECK(qty >= 0))")
    results = []
    for batch in data["batches"]:
        db.execute("BEGIN")
        statuses = []
        for row in batch["rows"]:
            db.execute("SAVEPOINT item")
            try:
                db.execute("INSERT INTO items VALUES (?, ?)", (row["id"], row["qty"]))
                if row["fail"]:
                    raise RuntimeError("after insert")
                statuses.append("ok")
            except (sqlite3.IntegrityError, RuntimeError) as error:
                db.execute("ROLLBACK TO item")
                statuses.append("invalid" if isinstance(error, sqlite3.IntegrityError) else "failed")
            finally:
                db.execute("RELEASE item")
        if batch["abort"]:
            db.rollback()
        else:
            db.commit()
        results.append({"rows": statuses, "committed": not batch["abort"]})
    rows = [list(row) for row in db.execute("SELECT id, qty FROM items ORDER BY id")]
    db.close()
    return {"batches": results, "rows": rows}
'''
def row(id="a",qty=1,fail=False):return {"id":id,"qty":qty,"fail":fail}
def batch(rows,abort=False):return {"rows":rows,"abort":abort}
def c(batches,statuses,rows,label):return {"input":{"batches":batches},"expected":{"batches":[{"rows":s,"committed":ok} for s,ok in statuses],"rows":rows},"label":label}
CASES=[
 c([batch([row()])],[(["ok"],True)],[["a",1]],"valid item commits"),
 c([batch([row("a"),row("b",-1),row("c",3)])],[(["ok","invalid","ok"],True)],[["a",1],["c",3]],"one invalid item does not cancel batch"),
 c([batch([row()],True)],[(["ok"],False)],[],"outer abort cancels released savepoint"),
 c([],[],[],"no batches"),c([batch([])],[([],True)],[],"empty committed batch"),c([batch([],True)],[([],False)],[],"empty aborted batch"),
 c([batch([row(qty=0)])],[(["ok"],True)],[["a",0]],"zero quantity"),
 c([batch([row(),row(qty=9)])],[(["ok","invalid"],True)],[["a",1]],"duplicate preserves first row"),
 c([batch([row(fail=True),row(qty=2)])],[(["failed","ok"],True)],[["a",2]],"rollback removes failed insert before retry"),
 c([batch([row()]),batch([row(),row("b",2)])],[(["ok"],True),(["invalid","ok"],True)],[["a",1],["b",2]],"duplicate across batches"),
 c([batch([row()],True),batch([row(qty=7)])],[(["ok"],False),(["ok"],True)],[["a",7]],"abort frees identifiers"),
 c([batch([row("z",2)]),batch([row("a",3),row("b",4,True)],True)],[(["ok"],True),(["ok","failed"],False)],[["z",2]],"outer abort preserves prior batch"),
 c([batch([row(qty=-1,fail=True)])],[(["invalid"],True)],[],"constraint failure precedes injected fault"),
]
rng=random.Random(39)
SPEC={"number":39,"slug":"sql-savepoint-import","title":"Isolate failed import rows with savepoints","difficulty":"Hard","time":35,
"prerequisites":"Transactions, constraint failures, and exception handling.",
"learn":"A savepoint marks a position inside a transaction. ROLLBACK TO restores that position without discarding earlier work in the transaction. RELEASE removes the savepoint. It does not make inner changes durable when an outer transaction is still open. This is useful for batch imports: one bad row can fail while other rows remain eligible to commit. The final batch decision still controls all accepted rows. A row can also fail after its insert succeeds. In that case the savepoint must remove that inserted row before the next item runs. Keep row outcomes separate from the final batch commit decision.",
"task":"`batches` is an ordered list of `{rows, abort}`. Each row is `{id, qty, fail}`. Use the supplied SQLite table. Each batch starts an outer transaction. Attempt each row under its own savepoint. A duplicate ID or negative quantity gives `invalid`. Otherwise insert it; if `fail` is true, undo that insert and give `failed`. Successful row attempts give `ok`. Continue after every row failure. If `abort` is true, roll back the whole batch; otherwise commit it. Return `{batches: [{rows: [status, ...], committed: Boolean}, ...], rows: [[id, qty], ...]}`. Row statuses describe attempts even when the batch later aborts. Sort final rows by ASCII ID. Constraint errors take precedence over injected failures. The judge cannot verify SQL use.",
"constraints":["0–30 batches, each with 0–30 rows.","IDs are nonempty ASCII strings. Quantities are -100–1000000. fail and abort are Boolean.","No actual concurrent transactions occur."],"hints":["ROLLBACK TO keeps the outer transaction active.","Release the row savepoint after both success and rollback."],
"starter":REFERENCE[:REFERENCE.index('    results = []')]+'    # TODO: use one outer transaction per batch and one savepoint per row.\n    raise NotImplementedError\n',"reference":REFERENCE,
"java":'''public Object solve(Map<String,Object> d){ Map<String,Object> saved=new TreeMap<>(); List<Object> results=new ArrayList<>(); for(Object raw:arr(d.get("batches"))){Map<String,Object> batch=obj(raw); Map<String,Object> working=new TreeMap<>(saved); List<Object> statuses=new ArrayList<>(); for(Object r:arr(batch.get("rows"))){Map<String,Object> row=obj(r);String id=s(row.get("id"));long qty=lng(row.get("qty"));if(working.containsKey(id)||qty<0)statuses.add("invalid");else if(b(row.get("fail")))statuses.add("failed");else{working.put(id,qty);statuses.add("ok");}}boolean commit=!b(batch.get("abort"));if(commit)saved=working;results.add(map("rows",statuses,"committed",commit));}List<Object> rows=new ArrayList<>();for(String id:saved.keySet())rows.add(list(id,saved.get(id)));return map("batches",results,"rows",rows);}''',
"approach":"Create a savepoint for each insert, roll back row failures, and commit or roll back the outer batch. With R total rows and S stored rows, indexed inserts cost O(R log(S + R)); storage is O(S + R), including output. Production imports need logging and explicit policies for unexpected database errors.",
"cases":CASES,"generated":[{"batches":[batch([row(rng.choice(["a","b","c","d","e"]),rng.randint(-2,8),rng.choice([False,False,True])) for _ in range(i%7+3)],rng.choice([False,True])) for _ in range(4)]} for i in range(24)],
"mutations":[{"name":"releases failed insert without rollback","old":"db.execute(\"ROLLBACK TO item\")","new":"pass  # missing row rollback"}],"sources":["https://www.sqlite.org/lang_savepoint.html","https://docs.python.org/3.11/library/sqlite3.html"]}
