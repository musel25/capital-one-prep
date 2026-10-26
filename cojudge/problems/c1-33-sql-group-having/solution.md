## Approach

Filter paid entries, group by account, compute the three aggregates, then apply HAVING. Repeated values are retained. A typical implementation scans n rows and groups with temporary storage; sorting g output groups takes O(g log g). Overall work can be O(n log n), depending on the query plan. Production reports must separately define how unknown amounts affect business decisions.

## Python implementation

```python
import sqlite3

def solve(data):
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    try:
        connection.execute("CREATE TABLE entries(id INTEGER PRIMARY KEY, account TEXT NOT NULL, amount INTEGER, kind TEXT NOT NULL)")
        connection.executemany("INSERT INTO entries VALUES (?, ?, ?, ?)", [(r["id"], r["account"], r["amount"], r["kind"]) for r in data["rows"]])
        return [dict(r) for r in summary_rows(connection, data["minimum_total"], data["minimum_events"])]
    finally:
        connection.close()

def summary_rows(connection, minimum_total, minimum_events):
    return connection.execute("SELECT account, COUNT(*) AS events, COUNT(amount) AS valued, COALESCE(SUM(amount), 0) AS total FROM entries WHERE kind = 'paid' GROUP BY account HAVING COALESCE(SUM(amount), 0) >= ? AND COUNT(*) >= ? ORDER BY total DESC, account ASC", (minimum_total, minimum_events)).fetchall()

# Supplied CoJudge adapter. Implement solve(data) above.
import json

class Solution:
    def run(self, payload: str) -> str:
        return json.dumps(solve(json.loads(payload)), ensure_ascii=True, allow_nan=False)

```
