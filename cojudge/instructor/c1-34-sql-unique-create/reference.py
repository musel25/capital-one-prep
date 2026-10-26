import sqlite3

def solve(data):
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    try:
        connection.execute("CREATE TABLE accounts(username TEXT PRIMARY KEY NOT NULL, quota INTEGER NOT NULL)")
        connection.executemany("INSERT INTO accounts VALUES (?, ?)", [(r["username"], r["quota"]) for r in data["initial"]])
        responses = [create_account(connection, r["username"], r["quota"]) for r in data["requests"]]
        rows = [dict(r) for r in connection.execute("SELECT username, quota FROM accounts ORDER BY username ASC")]
        return {"responses": responses, "accounts": rows}
    finally:
        connection.close()

def create_account(connection, username, quota):
    cursor = connection.execute("INSERT INTO accounts(username, quota) VALUES (?, ?) ON CONFLICT(username) DO NOTHING", (username, quota))
    record = dict(connection.execute("SELECT username, quota FROM accounts WHERE username = ?", (username,)).fetchone())
    status = 201 if cursor.rowcount == 1 else (200 if record["quota"] == quota else 409)
    return {"status": status, "record": record}

# Supplied CoJudge adapter. Implement solve(data) above.
import json

class Solution:
    def run(self, payload: str) -> str:
        return json.dumps(solve(json.loads(payload)), ensure_ascii=True, allow_nan=False)
