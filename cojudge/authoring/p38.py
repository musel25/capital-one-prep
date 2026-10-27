import random
REFERENCE='''import sqlite3

def solve(data: dict) -> dict:
    db = sqlite3.connect(":memory:")
    db.executescript("CREATE TABLE account(balance INTEGER); CREATE TABLE requests(key TEXT PRIMARY KEY, amount INTEGER);")
    db.execute("INSERT INTO account VALUES (?)", (data["balance"],))
    db.commit()
    results = []
    for op in data["credits"]:
        previous = db.execute("SELECT amount FROM requests WHERE key = ?", (op["key"],)).fetchone()
        if previous is not None:
            results.append("replay" if previous[0] == op["amount"] else "conflict")
            continue
        try:
            with db:
                db.execute("INSERT INTO requests VALUES (?, ?)", (op["key"], op["amount"]))
                db.execute("UPDATE account SET balance = balance + ?", (op["amount"],))
                if op["fail"]:
                    raise RuntimeError("injected before commit")
            results.append("ok")
        except RuntimeError:
            results.append("failed")
    balance = db.execute("SELECT balance FROM account").fetchone()[0]
    keys = [row[0] for row in db.execute("SELECT key FROM requests ORDER BY key")]
    db.close()
    return {"results": results, "balance": balance, "keys": keys}
'''
def o(key="k", amount=2, fail=False): return {"key":key,"amount":amount,"fail":fail}
def c(balance,ops,status,end,keys,label):return {"input":{"balance":balance,"credits":ops},"expected":{"results":status,"balance":end,"keys":keys},"label":label}
CASES=[
 c(0,[o()],["ok"],2,["k"],"new credit"),c(0,[o(),o()],["ok","replay"],2,["k"],"retry does not add money"),c(0,[o(),o(amount=3)],["ok","conflict"],2,["k"],"key cannot change amount"),
 c(5,[],[],5,[],"empty requests"),c(0,[o(fail=True)],["failed"],0,[],"failure rolls back key and balance"),c(0,[o(fail=True),o()],["failed","ok"],2,["k"],"failed key can retry"),
 c(1,[o("b",4),o("a",3)],["ok","ok"],8,["a","b"],"independent keys sorted"),c(9,[o("a",1),o("b",1)],["ok","ok"],11,["a","b"],"equal amounts with different keys"),
 c(0,[o(),o(fail=True)],["ok","replay"],2,["k"],"replay precedes fault"),c(0,[o(),o(amount=5,fail=True)],["ok","conflict"],2,["k"],"conflict precedes fault"),
 c(7,[o("a",2),o("b",9,True),o("c",1)],["ok","failed","ok"],10,["a","c"],"prior commits survive later failure"),c(0,[o("k",1,True),o("k",4),o("k",1)],["failed","ok","conflict"],4,["k"],"failed payload does not reserve key"),
]
rng=random.Random(38)
SPEC={"number":38,"slug":"sql-idempotency-key","title":"Commit a credit and its idempotency key","difficulty":"Medium","time":30,
"prerequisites":"Transactions, UNIQUE constraints, and request retries.",
"learn":"A retry can arrive after the first request has already committed. An idempotency key identifies that logical request. Store the key and its payload in a table with a uniqueness constraint. A repeat with the same payload returns a replay result. A repeat with a different payload is a conflict. The key and the business write must share one transaction. Otherwise a crash can record the key without applying the credit, or apply the credit without recording the key. A failed transaction leaves the key available for a later attempt. This task models ordered requests and an injected failure immediately before commit.",
"scenario": ('A wallet service adds credits to an account. Clients retry requests, so each credit has a key. The key and the balance change must be saved in the same transaction. Otherwise a crash could save one without the other.'),
 "example_notes": ['A new key adds 2.', 'The same key again: `replay`, with no second credit.', 'The same key with a different amount: `conflict`.'],
 "task":('**Input:** `data` has:\n'
    '- `balance`: the initial account balance.\n'
    '- `credits`: a list of `{"key": ..., "amount": ..., "fail": ...}`.\n'
    '\n'
    '**Rules:** for each credit, in order:\n'
    '- **Key already committed:** return `replay` if the amount is the same, or `conflict` if it is different. Nothing changes. This check comes before `fail`.\n'
    '- **New key:** in one transaction, insert the key and add the amount. If `fail` is true, roll back both writes and return `failed`. Otherwise commit and return `ok`.\n'
    '\n'
    '**Return** `{"results": [...], "balance": int, "keys": [...]}`. `keys` lists the committed keys in ASCII order.\n'
    '\n'
    'Use the supplied SQLite tables. The judge cannot check SQL use.'),
"constraints":["0–200 credits. Balance is 0–1000000; amounts are 1–1000000.","Keys are nonempty ASCII strings of length at most 30. fail is Boolean.","This ordered trace does not test actual parallel transactions."],
"hints":["A failed operation must not reserve its key.","Keep the INSERT and balance UPDATE inside the same transaction context."],
"starter":REFERENCE[:REFERENCE.index('    results = []')]+'    # TODO: process credits atomically and return results/balance/keys.\n    raise NotImplementedError\n',"reference":REFERENCE,
"java":'''public Object solve(Map<String,Object> d) {long balance=lng(d.get("balance")); Map<String,Long> seen=new TreeMap<>(); List<Object> results=new ArrayList<>(); for(Object raw:arr(d.get("credits"))){Map<String,Object> op=obj(raw); String key=s(op.get("key")); long amount=lng(op.get("amount")); if(seen.containsKey(key)) results.add(seen.get(key)==amount?"replay":"conflict"); else if(b(op.get("fail"))) results.add("failed"); else {seen.put(key,amount); balance+=amount; results.add("ok");}} return map("results",results,"balance",balance,"keys",new ArrayList<>(seen.keySet()));}''',
"approach":"Read a prior key, then use a transaction for the new key and balance update. The unique key is also enforced by SQLite. This ordered model uses O(C log C) work and O(C) storage. A production implementation must handle concurrent uniqueness conflicts and retain keys for an explicit period.",
"cases":CASES,"generated":[{"balance":i,"credits":[o(rng.choice(["a","b","c","d"]),rng.randint(1,7),rng.choice([False,True])) for _ in range(24)]} for i in range(24)],
"mutations":[{"name":"ignores payload conflict","old":"previous[0] == op[\"amount\"]","new":"True"}],"sources":["https://www.sqlite.org/lang_createtable.html","https://docs.python.org/3.11/library/sqlite3.html"]}
