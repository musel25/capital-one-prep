## Reference solution

```python
import sqlite3


def apply_transfers(balances, transfers):
    db = sqlite3.connect(":memory:")
    try:
        db.execute("CREATE TABLE balances (account TEXT PRIMARY KEY, cents INTEGER NOT NULL CHECK(cents >= 0))")
        db.executemany("INSERT INTO balances VALUES (?, ?)", balances.items())
        db.commit()
        accepted = []
        for transfer in transfers:
            source_name, target_name = transfer["from"], transfer["to"]
            amount = transfer["amount"]
            with db:
                db.execute("BEGIN")
                source = db.execute("SELECT cents FROM balances WHERE account = ?", (source_name,)).fetchone()
                target = db.execute("SELECT cents FROM balances WHERE account = ?", (target_name,)).fetchone()
                ok = source is not None and target is not None and source[0] >= amount
                if ok:
                    db.execute("UPDATE balances SET cents = cents + ? WHERE account = ?", (-amount, source_name))
                    db.execute("UPDATE balances SET cents = cents + ? WHERE account = ?", (amount, target_name))
                accepted.append(ok)
        remaining = dict(db.execute("SELECT account, cents FROM balances"))
        return {"accepted": accepted, "balances": remaining}
    finally:
        db.close()
```
