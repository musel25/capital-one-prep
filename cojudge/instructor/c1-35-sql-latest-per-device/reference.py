import sqlite3

def solve(data):
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    try:
        connection.execute("CREATE TABLE readings(id INTEGER PRIMARY KEY, device TEXT NOT NULL, ts INTEGER NOT NULL, value INTEGER)")
        connection.executemany("INSERT INTO readings VALUES (?, ?, ?, ?)", [(r["id"], r["device"], r["ts"], r["value"]) for r in data["rows"]])
        return [dict(r) for r in latest_rows(connection, data["cutoff"])]
    finally:
        connection.close()

def latest_rows(connection, cutoff):
    return connection.execute("WITH ranked AS (SELECT device, id, ts, value, ROW_NUMBER() OVER (PARTITION BY device ORDER BY ts DESC, id DESC) AS position FROM readings WHERE ts <= ?) SELECT device, id, ts, value FROM ranked WHERE position = 1 ORDER BY device ASC", (cutoff,)).fetchall()

# Supplied CoJudge adapter. Implement solve(data) above.
import json

class Solution:
    def run(self, payload: str) -> str:
        return json.dumps(solve(json.loads(payload)), ensure_ascii=True, allow_nan=False)
