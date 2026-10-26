"""Atomic transfer exercise; instructor content stays in this source pack."""
import random

REFERENCE = '''import sqlite3

def solve(data: dict) -> dict:
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE accounts (id TEXT PRIMARY KEY, balance INTEGER NOT NULL CHECK(balance >= 0))")
    db.executemany("INSERT INTO accounts VALUES (?, ?)", data["balances"].items())
    db.commit()
    results = []
    for op in data["transfers"]:
        try:
            db.execute("BEGIN")
            changed = db.execute("UPDATE accounts SET balance = balance - ? WHERE id = ? AND balance >= ?", (op["amount"], op["from"], op["amount"])).rowcount
            if not changed:
                db.rollback()
                results.append("insufficient")
                continue
            if op["fail"]:
                raise RuntimeError("injected after debit")
            db.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (op["amount"], op["to"]))
            db.commit()
            results.append("ok")
        except RuntimeError:
            db.rollback()  # undo the debit
            results.append("failed")
    balances = dict(db.execute("SELECT id, balance FROM accounts ORDER BY id"))
    db.close()
    return {"results": results, "balances": balances}
'''

def t(a=1, fail=False, source="a", target="b"):
    return {"from": source, "to": target, "amount": a, "fail": fail}

def case(balances, transfers, results, final, label):
    return {"input": {"balances": balances, "transfers": transfers}, "expected": {"results": results, "balances": final}, "label": label}

CASES = [
    case({"a": 10, "b": 0}, [t(4)], ["ok"], {"a": 6, "b": 4}, "transfer commits both entries"),
    case({"a": 10, "b": 0}, [t(4, True)], ["failed"], {"a": 10, "b": 0}, "failure restores debit"),
    case({"a": 3, "b": 2}, [t(4)], ["insufficient"], {"a": 3, "b": 2}, "insufficient funds change neither balance"),
    case({}, [], [], {}, "empty ledger"),
    case({"a": 8}, [], [], {"a": 8}, "account without transfers"),
    case({"a": 5, "b": 1}, [t(5)], ["ok"], {"a": 0, "b": 6}, "exact balance"),
    case({"a": 0, "b": 0}, [t()], ["insufficient"], {"a": 0, "b": 0}, "zero balance"),
    case({"a": 5, "b": 0}, [t(5, True), t(5)], ["failed", "ok"], {"a": 0, "b": 5}, "retry after rollback"),
    case({"a": 5, "b": 0}, [t(4), t(2)], ["ok", "insufficient"], {"a": 1, "b": 4}, "prior commit survives rejection"),
    case({"a": 5, "b": 0}, [t(5), t(3, False, "b", "a")], ["ok", "ok"], {"a": 3, "b": 2}, "reverse transfer"),
    case({"a": 1, "b": 9, "c": 4}, [t(2, True), t(3, False, "c", "b")], ["insufficient", "ok"], {"a": 1, "b": 12, "c": 1}, "validation precedes fault and isolates accounts"),
    case({"a": 10, "b": 0}, [t(2), t(3, True), t(7)], ["ok", "failed", "ok"], {"a": 1, "b": 9}, "rollback preserves earlier commit"),
]
rng = random.Random(36)
GENERATED = [{"balances": {"a": i + 20, "b": i, "c": 0}, "transfers": [t(rng.randint(1, 30), rng.choice([True, False]), *rng.sample(["a", "b", "c"], 2)) for _ in range(18)]} for i in range(24)]
SPEC = {
    "number": 36, "slug": "atomic-transfer-rollback", "title": "Repair an atomic SQL transfer", "difficulty": "Medium", "time": 30,
    "prerequisites": "SQL UPDATE, parameterized statements, and Python exceptions.",
    "learn": "A transfer changes two balances. Both changes must commit, or neither change must remain. A transaction groups these writes into one unit. Commit only after the debit and credit succeed. Roll back if an exception occurs between them. A conditional debit can check the available balance and subtract the amount in one statement. Its affected-row count tells you whether the debit occurred. Setup writes also need a commit before you start an explicit transaction. This exercise injects a failure after the debit. The starter catches that failure but commits the partial transfer. Repair that transaction boundary and preserve earlier successful transfers.",
    "task": "Repair the faulty `solve(data)` implementation. `balances` maps account IDs to initial integer balances. `transfers` is an ordered list of objects with `from`, `to`, positive `amount`, and Boolean `fail`. Both IDs exist and differ. First reject a transfer that lacks funds with `insufficient`. Otherwise debit the source. If `fail` is true, roll back and return `failed`. Otherwise credit the destination, commit, and return `ok`. Each transfer has its own transaction. Return `{results: [...], balances: {...}}` with one status per transfer and final balances. Use the supplied in-memory SQLite setup. The output judge cannot verify SQL use.",
    "constraints": ["0–100 accounts and 0–200 transfers.", "IDs are nonempty ASCII strings. Initial balances are 0–1000000; amounts are 1–1000000.", "Failures are injected exceptions, not actual concurrent operations."],
    "hints": ["A caught exception does not undo an earlier SQL statement.", "The exception handler must end the current transaction without retaining its writes."],
    "starter": REFERENCE.replace("db.rollback()  # undo the debit", "db.commit()  # BUG: commits only the debit"), "reference": REFERENCE,
    "java": '''public Object solve(Map<String,Object> d) {
        Map<String,Object> balances = new TreeMap<>(obj(d.get("balances"))); List<Object> results = new ArrayList<>();
        for(Object raw: arr(d.get("transfers"))) { Map<String,Object> op=obj(raw); String a=s(op.get("from")), z=s(op.get("to")); long amount=lng(op.get("amount")), before=lng(balances.get(a));
            if(before<amount) results.add("insufficient"); else if(b(op.get("fail"))) results.add("failed"); else { balances.put(a,before-amount); balances.put(z,lng(balances.get(z))+amount); results.add("ok"); }
        } return map("results",results,"balances",balances);
    }''',
    "approach": "Run a conditional debit and credit inside one explicit SQLite transaction. Roll back the injected failure. Each transfer uses indexed account lookups; setup and output are O(A log A), with O(A + T) output storage. The Java model applies the same state transition independently. Production systems also need isolation, durable storage, and recovery checks; this task does not test concurrent clients.",
    "cases": CASES, "generated": GENERATED,
    "mutations": [{"name": "commits partial debit after exception", "old": "db.rollback()  # undo the debit", "new": "db.commit()  # wrong partial commit"}],
    "sources": ["https://docs.python.org/3.11/library/sqlite3.html", "https://www.sqlite.org/lang_transaction.html"],
}
