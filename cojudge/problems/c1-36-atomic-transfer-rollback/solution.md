## Approach

Run a conditional debit and credit inside one explicit SQLite transaction. Roll back the injected failure. Each transfer uses indexed account lookups; setup and output are O(A log A), with O(A + T) output storage. The Java model applies the same state transition independently. Production systems also need isolation, durable storage, and recovery checks; this task does not test concurrent clients.

## Python implementation

```python
import sqlite3

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

# Supplied CoJudge adapter. Implement solve(data) above.
import json

class Solution:
    def run(self, payload: str) -> str:
        return json.dumps(solve(json.loads(payload)), ensure_ascii=True, allow_nan=False)

```
