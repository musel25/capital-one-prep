## Approach

LEFT JOIN matches on customer id and the paid predicate together. Unmatched customers retain one NULL-filled payment side. Explicit ordering makes results stable. Without indexes, a simple join can require O(c*p) work; SQLite may build an automatic index. Sorting and output depend on the number of resulting rows. This fixture accepts orphan payments to make join behavior visible.

## Python implementation

```python
import sqlite3

def solve(data):
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    try:
        connection.execute("CREATE TABLE customers(id INTEGER PRIMARY KEY, name TEXT NOT NULL)")
        connection.execute("CREATE TABLE payments(id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER NOT NULL, status TEXT NOT NULL)")
        connection.executemany("INSERT INTO customers VALUES (?, ?)", [(r["id"], r["name"]) for r in data["customers"]])
        connection.executemany("INSERT INTO payments VALUES (?, ?, ?, ?)", [(r["id"], r["customer_id"], r["amount"], r["status"]) for r in data["payments"]])
        return [dict(r) for r in report_rows(connection)]
    finally:
        connection.close()

def report_rows(connection):
    return connection.execute("SELECT c.id AS customer_id, c.name AS name, p.id AS payment_id, p.amount AS amount FROM customers AS c LEFT JOIN payments AS p ON p.customer_id = c.id AND p.status = 'paid' ORDER BY c.id ASC, p.id ASC").fetchall()

# Supplied CoJudge adapter. Implement solve(data) above.
import json

class Solution:
    def run(self, payload: str) -> str:
        return json.dumps(solve(json.loads(payload)), ensure_ascii=True, allow_nan=False)

```
