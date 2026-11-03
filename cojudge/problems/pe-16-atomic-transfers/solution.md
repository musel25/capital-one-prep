## How it works

Check all conditions before you change a balance. Then make both changes together. In a real database you get the same guarantee from a transaction: both updates are saved, or neither is.

## Common mistakes

- Rejecting a transfer of the exact balance.
- Subtracting from the source when the target does not exist.
- Adding to the target without subtracting from the source.

## Solution

```python
def apply_transfers(balances, transfers):
    accounts = dict(balances)
    accepted = []
    for transfer in transfers:
        source, target, amount = transfer["from"], transfer["to"], transfer["amount"]
        ok = source in accounts and target in accounts and accounts[source] >= amount
        if ok:
            accounts[source] -= amount
            accounts[target] += amount
        accepted.append(ok)
    return {"accepted": accepted, "balances": accounts}
```

The judge also accepts this version with a real SQLite transaction. `with db:` commits both updates together, or rolls both back on an error:

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
