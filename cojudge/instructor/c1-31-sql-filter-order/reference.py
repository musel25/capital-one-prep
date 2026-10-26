import sqlite3

def solve(data):
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    try:
        connection.execute("CREATE TABLE transfers(id INTEGER PRIMARY KEY, owner TEXT NOT NULL, amount INTEGER NOT NULL, posted INTEGER NOT NULL)")
        connection.executemany("INSERT INTO transfers VALUES (?, ?, ?, ?)", [(r["id"], r["owner"], r["amount"], r["posted"]) for r in data["rows"]])
        return [dict(r) for r in select_rows(connection, data["owner"], data["minimum"], data["limit"])]
    finally:
        connection.close()

def select_rows(connection, owner, minimum, limit):
    return connection.execute("SELECT id, amount FROM transfers WHERE owner = ? AND posted = 1 AND amount >= ? ORDER BY amount DESC, id ASC LIMIT ?", (owner, minimum, limit)).fetchall()

# Supplied CoJudge adapter. Implement solve(data) above.
import json

class Solution:
    def run(self, payload: str) -> str:
        return json.dumps(solve(json.loads(payload)), ensure_ascii=True, allow_nan=False)
