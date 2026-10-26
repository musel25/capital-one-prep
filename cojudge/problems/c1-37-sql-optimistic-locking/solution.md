## Approach

Use one conditional UPDATE per proposal, with the version increment in the same statement. The one-row table makes processing O(U), plus output storage O(U). Real conflicts may require a new read and a business decision; blindly retrying an old value can still discard intent.

## Python implementation

```python
import sqlite3

def solve(data: dict) -> dict:
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE document (id INTEGER PRIMARY KEY, value TEXT, version INTEGER)")
    db.execute("INSERT INTO document VALUES (1, ?, ?)", (data["value"], data["version"]))
    db.commit()
    results = []
    for op in data["updates"]:
        with db:
            count = db.execute("UPDATE document SET value = ?, version = version + 1 WHERE id = 1 AND version = ?", (op["value"], op["expected"])).rowcount
        results.append(count == 1)
    value, version = db.execute("SELECT value, version FROM document WHERE id = 1").fetchone()
    db.close()
    return {"accepted": results, "value": value, "version": version}

# Supplied CoJudge adapter. Implement solve(data) above.
import json

class Solution:
    def run(self, payload: str) -> str:
        return json.dumps(solve(json.loads(payload)), ensure_ascii=True, allow_nan=False)

```
