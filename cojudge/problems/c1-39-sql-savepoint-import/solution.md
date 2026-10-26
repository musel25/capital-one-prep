## Approach

Create a savepoint for each insert, roll back row failures, and commit or roll back the outer batch. With R total rows and S stored rows, indexed inserts cost O(R log(S + R)); storage is O(S + R), including output. Production imports need logging and explicit policies for unexpected database errors.

## Python implementation

```python
import sqlite3

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

# Supplied CoJudge adapter. Implement solve(data) above.
import json

class Solution:
    def run(self, payload: str) -> str:
        return json.dumps(solve(json.loads(payload)), ensure_ascii=True, allow_nan=False)

```
