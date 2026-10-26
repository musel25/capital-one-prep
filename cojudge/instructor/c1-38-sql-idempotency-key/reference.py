import sqlite3

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

# Supplied CoJudge adapter. Implement solve(data) above.
import json

class Solution:
    def run(self, payload: str) -> str:
        return json.dumps(solve(json.loads(payload)), ensure_ascii=True, allow_nan=False)
