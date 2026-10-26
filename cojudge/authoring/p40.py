import random
REFERENCE='''import sqlite3

def solve(data: dict) -> dict:
    db = sqlite3.connect(":memory:")
    db.executescript("CREATE TABLE orders(id TEXT PRIMARY KEY, amount INTEGER); CREATE TABLE outbox(id TEXT PRIMARY KEY, amount INTEGER);")
    results = []
    for op in data["orders"]:
        existing = db.execute("SELECT amount FROM orders WHERE id = ?", (op["id"],)).fetchone()
        if existing is not None:
            results.append("replay" if existing[0] == op["amount"] else "conflict")
            continue
        try:
            with db:
                db.execute("INSERT INTO orders VALUES (?, ?)", (op["id"], op["amount"]))
                if op["fail"] == "business":
                    raise RuntimeError("after order")
                db.execute("INSERT INTO outbox VALUES (?, ?)", (op["id"], op["amount"]))
                if op["fail"] == "event":
                    raise RuntimeError("after event")
            results.append("ok")
        except RuntimeError:
            results.append("failed")
    orders = [list(row) for row in db.execute("SELECT id, amount FROM orders ORDER BY id")]
    events = [list(row) for row in db.execute("SELECT id, amount FROM outbox ORDER BY id")]
    db.close()
    return {"results": results, "orders": orders, "events": events}
'''
def o(id="a",amount=2,fail="none"):return {"id":id,"amount":amount,"fail":fail}
def c(ops,status,rows,label):return {"input":{"orders":ops},"expected":{"results":status,"orders":rows,"events":[r[:] for r in rows]},"label":label}
CASES=[c([o()],["ok"],[["a",2]],"business record and event commit"),c([o(fail="business")],["failed"],[],"failure between writes"),c([o(),o()],["ok","replay"],[["a",2]],"retry creates no duplicate event"),c([],[],[],"empty input"),c([o(fail="event")],["failed"],[],"failure after event rolls back both"),c([o(fail="business"),o()],["failed","ok"],[["a",2]],"retry after business failure"),c([o(fail="event"),o(amount=5)],["failed","ok"],[["a",5]],"failed payload reserves no ID"),c([o(),o(amount=3)],["ok","conflict"],[["a",2]],"changed replay payload"),c([o("b",4),o("a",3)],["ok","ok"],[["a",3],["b",4]],"output order differs from commit order"),c([o(),o(fail="event")],["ok","replay"],[["a",2]],"replay ignores fault"),c([o(),o(amount=7,fail="business")],["ok","conflict"],[["a",2]],"conflict ignores fault"),c([o("a",1),o("b",2,"business"),o("c",3),o("b",2)],["ok","failed","ok","ok"],[["a",1],["b",2],["c",3]],"failure isolation and recovery")]
rng=random.Random(40)
SPEC={"number":40,"slug":"transactional-outbox","title":"Write an order and its outbox event atomically","difficulty":"Hard","time":30,
"prerequisites":"SQL transactions, primary keys, and idempotent requests.",
"learn":"A business write and a message publish cannot normally share a local database transaction. A transactional outbox stores the intended event beside the business record instead. One database transaction inserts both rows. A separate worker can later publish committed outbox rows and retry delivery. This task covers the producer boundary only. A failure after either insert must leave neither row behind. A repeated order ID with the same amount must not create another event. A repeated ID with a different amount is a conflict. Atomic outbox insertion prevents missing event records, but it does not itself guarantee exactly one delivery to consumers.",
"task":"`orders` is an ordered list of `{id, amount, fail}`. `fail` is `none`, `business` (after inserting the order), or `event` (after inserting its outbox row). A committed ID returns `replay` for the same amount or `conflict` for a different amount; do not evaluate the fault for these requests. For a new ID, insert order and outbox rows in one SQLite transaction. Return `failed` and roll back on either injected fault; otherwise return `ok`. Return `{results: [...], orders: [[id, amount], ...], events: [[id, amount], ...]}` with both tables sorted by ASCII ID. Use the supplied schema. There is no publisher or network call. The output judge cannot enforce SQL use.",
"constraints":["0–200 orders. IDs are nonempty ASCII strings of length at most 30.","Amounts are integer minor units from 1 to 1000000.","The trace is sequential; it does not test real concurrent transactions."],"hints":["Put both INSERT statements in the same transaction.","A rolled-back ID can be used by a later request."],
"starter":REFERENCE[:REFERENCE.index('    results = []')]+'    # TODO: insert each new order and event in one transaction.\n    raise NotImplementedError\n',"reference":REFERENCE,
"java":'''public Object solve(Map<String,Object> d){Map<String,Long> committed=new TreeMap<>();List<Object> results=new ArrayList<>();for(Object raw:arr(d.get("orders"))){Map<String,Object> op=obj(raw);String id=s(op.get("id"));long amount=lng(op.get("amount"));if(committed.containsKey(id))results.add(committed.get(id)==amount?"replay":"conflict");else if(!s(op.get("fail")).equals("none"))results.add("failed");else{committed.put(id,amount);results.add("ok");}}List<Object> orders=new ArrayList<>(),events=new ArrayList<>();for(String id:committed.keySet()){orders.add(list(id,committed.get(id)));events.add(list(id,committed.get(id)));}return map("results",results,"orders",orders,"events",events);}''',
"approach":"Use two parameterized inserts inside one transaction context. Check committed IDs for replay and conflict. For N requests, indexed lookups and inserts cost O(N log N), with O(N) space. A real publisher still needs retries, delivery tracking, and consumers that handle duplicate messages.",
"cases":CASES,"generated":[{"orders":[o(rng.choice(["a","b","c","d","e"]),rng.randint(1,9),rng.choice(["none","business","event"])) for _ in range(i+8)]} for i in range(24)],
"mutations":[{"name":"commits business record before event","old":"if op[\"fail\"] == \"business\":","new":"db.commit()  # incorrect early commit\n                if op[\"fail\"] == \"business\":"}],"sources":["https://www.sqlite.org/lang_transaction.html","https://docs.python.org/3.11/library/sqlite3.html"]}
