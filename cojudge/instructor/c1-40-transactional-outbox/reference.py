import sqlite3

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

# Supplied CoJudge adapter. Implement solve(data) above.
import json

class Solution:
    def run(self, payload: str) -> str:
        return json.dumps(solve(json.loads(payload)), ensure_ascii=True, allow_nan=False)
