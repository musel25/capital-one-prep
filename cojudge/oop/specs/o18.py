"""Original exercise: write a context manager class."""
from cojudge.oop.steps import call, case, error, get, new, obj, ref, with_

SPEC = {
    "number": 18, "slug": "batch-context-manager", "title": "Write a context manager",
    "difficulty": "Medium", "time": 35, "level": 4,
    "prerequisites": "Level 3 and exercises 15–17. Properties and exceptions.",
    "learn": """A `with` block calls two methods on an object:

```python
with batch as b:      # b = batch.__enter__()
    b.add(50)
# batch.__exit__(exc_type, exc_value, traceback) runs here, always
```

- `__enter__(self)` runs at the start. Its return value is bound by `as`. Often it returns `self`.
- `__exit__(self, exc_type, exc, tb)` runs at the end, **also when the block raises**. If the
  block ended normally, all three arguments are `None`. If the block raised, they describe the
  exception.
- If `__exit__` returns a true value, the exception is suppressed. Return `False` (or `None`) to
  let it continue. Suppressing errors by accident hides bugs.
- `__exit__` can raise its own exception, for example when a final check fails.

This is how files close themselves and how database transactions commit or roll back.""",
    "scenario": """A banking back office groups several balance changes into one batch. Either the
whole batch is applied, or none of it. If the code in the batch fails, or the result would make
the balance negative, nothing changes.""",
    "task": """Write `Account` and `Batch`.

- `Account(balance)`: a negative `balance` raises `ValueError`. Store it in `balance`.
- `Batch(account)`: a batch can be used in **one** `with` block.
  - `__enter__`: return the batch. If the batch was already entered once, raise `RuntimeError`.
  - `add(amount)`: stage an amount. It is only allowed inside the `with` block; otherwise raise
    `RuntimeError`. `amount` must be a non-zero `int` (not a `bool`); otherwise `ValueError`. A
    rejected amount is not staged. Return `None`.
  - `pending`: read-only property. The sum of the staged amounts.
  - `committed`: read-only property. `True` after the batch was applied.
  - `__exit__`: the staged amounts are cleared in every case.
    - If the block raised, apply nothing and do **not** suppress the exception.
    - Otherwise, if `balance + pending` is negative, apply nothing and raise `ValueError`.
    - Otherwise add the sum to `account.balance` and mark the batch as committed.

The driver runs `with` blocks for you; see "How the tests work".""",
    "constraints": ["Amounts are at most 10^9 in absolute value.", "At most 40 steps per test, including the steps inside blocks."],
    "hints": ["Keep a small state: `\"new\"`, `\"open\"`, then `\"committed\"` or `\"discarded\"`.",
              "`__exit__` should `return False` explicitly after it handles an exception."],
    "starter": '''class Account:
    def __init__(self, balance: int):
        raise NotImplementedError


class Batch:
    def __init__(self, account: Account):
        raise NotImplementedError

    def __enter__(self) -> "Batch":
        raise NotImplementedError

    def add(self, amount: int) -> None:
        raise NotImplementedError

    @property
    def pending(self) -> int:
        raise NotImplementedError

    @property
    def committed(self) -> bool:
        raise NotImplementedError

    def __exit__(self, exc_type, exc, tb) -> bool:
        raise NotImplementedError
''',
    "reference": '''class Account:
    def __init__(self, balance: int):
        if balance < 0:
            raise ValueError("balance must not be negative")
        self.balance = balance


class Batch:
    def __init__(self, account: Account):
        self.account = account
        self._staged: list[int] = []
        self._state = "new"

    def __enter__(self) -> "Batch":
        if self._state != "new":
            raise RuntimeError("a batch can be used only once")
        self._state = "open"
        return self

    def add(self, amount: int) -> None:
        if self._state != "open":
            raise RuntimeError("add is only allowed inside the with block")
        if isinstance(amount, bool) or not isinstance(amount, int) or amount == 0:
            raise ValueError("amount must be a non-zero integer")
        self._staged.append(amount)

    @property
    def pending(self) -> int:
        return sum(self._staged)

    @property
    def committed(self) -> bool:
        return self._state == "committed"

    def __exit__(self, exc_type, exc, tb) -> bool:
        total, self._staged = sum(self._staged), []
        if exc_type is not None:
            self._state = "discarded"
            return False
        if self.account.balance + total < 0:
            self._state = "discarded"
            raise ValueError("the batch would make the balance negative")
        self.account.balance += total
        self._state = "committed"
        return False
''',
    "facts": ["property Batch pending", "property Batch committed"],
    "java": '''static class Account implements Obj { long balance; public String type() { return "Account"; } }
static class Batch implements Obj {
    Account account; List<Long> staged = new ArrayList<>(); String state = "new";
    public String type() { return "Batch"; }
    long pending() { long t = 0; for (long v : staged) t += v; return t; }
    public Object enter() { if (!state.equals("new")) throw err("RuntimeError"); state = "open"; return this; }
    public boolean exit(String error) {
        long total = pending(); staged.clear();
        if (error != null) { state = "discarded"; return false; }
        if (account.balance + total < 0) { state = "discarded"; throw err("ValueError"); }
        account.balance += total; state = "committed"; return false;
    }
}
Object step(Map<String,Object> op) {
    String d = s(op.get("do"));
    Object t = target(op);
    if (d.equals("new")) {
        if (t.equals("Account")) { Account a = new Account(); a.balance = lng(arg(op, 0, "balance", MISSING)); if (a.balance < 0) throw err("ValueError"); return a; }
        Batch b = new Batch(); b.account = (Account) arg(op, 0, "account", MISSING); return b;
    }
    if (t instanceof Account) {
        if (d.equals("get") && s(op.get("attr")).equals("balance")) return ((Account) t).balance;
        throw err("AttributeError");
    }
    Batch b = (Batch) t;
    if (d.equals("call") && s(op.get("method")).equals("add")) {
        if (!b.state.equals("open")) throw err("RuntimeError");
        Object v = args(op).get(0);
        if (!isInt(v) || lng(v) == 0) throw err("ValueError");
        b.staged.add(lng(v)); return null;
    }
    if (d.equals("get")) {
        String a = s(op.get("attr"));
        if (a.equals("pending")) return b.pending();
        if (a.equals("committed")) return b.state.equals("committed");
    }
    throw err("AttributeError");
}
''',
    "approach": """The batch is a small state machine: new, open, then committed or discarded.
`__exit__` always clears the staged amounts first, then chooses one outcome. With an exception
in the block it discards and returns `False`, so the original exception continues. Without one,
it checks the final balance once and either raises or applies the total in a single assignment,
so the account never shows a partial batch.""",
    "example_notes": [
        "Two staged amounts are applied together when the block ends normally: 100 + 50 - 30 = 120.",
        "The block raises RuntimeError. __exit__ discards the staged 500 and does not suppress the error.",
        "The batch would make the balance -10, so __exit__ raises ValueError and the balance stays 20.",
    ],
    "cases": [
        case("commit on success",
             (new("Account", 100, save="acc"), obj("Account")), (new("Batch", ref("acc"), save="b"), obj("Batch")),
             (with_("b", [{"do": "call", "obj": "b", "method": "add", "args": [50]},
                          {"do": "call", "obj": "b", "method": "add", "args": [-30]}]), {"body": [None, None], "error": None}),
             (get("acc", "balance"), 120), (get("b", "committed"), True)),
        case("error in the block discards",
             (new("Account", 100, save="acc"), obj("Account")), (new("Batch", ref("acc"), save="b"), obj("Batch")),
             (with_("b", [{"do": "call", "obj": "b", "method": "add", "args": [500]}], raise_="RuntimeError"),
              {"body": [None], "error": "RuntimeError"}),
             (get("acc", "balance"), 100), (get("b", "committed"), False)),
        case("overdraft at exit",
             (new("Account", 20, save="acc"), obj("Account")), (new("Batch", ref("acc"), save="b"), obj("Batch")),
             (with_("b", [{"do": "call", "obj": "b", "method": "add", "args": [-30]}]), {"body": [None], "error": "ValueError"}),
             (get("acc", "balance"), 20), (get("b", "pending"), 0)),
        case("pending inside the block and enter returns the batch",
             (new("Account", 0, save="acc"), obj("Account")), (new("Batch", ref("acc"), save="b"), obj("Batch")),
             (with_("b", [{"do": "call", "obj": "x", "method": "add", "args": [7]},
                          {"do": "call", "obj": "x", "method": "add", "args": [8]},
                          {"do": "get", "obj": "x", "attr": "pending"}], as_="x"), {"body": [None, None, 15], "error": None}),
             (get("acc", "balance"), 15), (get("b", "pending"), 0)),
        case("add outside the block",
             (new("Account", 10, save="acc"), obj("Account")), (new("Batch", ref("acc"), save="b"), obj("Batch")),
             (call("b", "add", 5), error("RuntimeError")),
             (with_("b", [{"do": "call", "obj": "b", "method": "add", "args": [5]}]), {"body": [None], "error": None}),
             (call("b", "add", 5), error("RuntimeError")), (get("acc", "balance"), 15)),
        case("a batch is used once",
             (new("Account", 10, save="acc"), obj("Account")), (new("Batch", ref("acc"), save="b"), obj("Batch")),
             (with_("b", []), {"body": [], "error": None}),
             (with_("b", [{"do": "call", "obj": "b", "method": "add", "args": [1]}]), {"body": [], "error": "RuntimeError"}),
             (get("acc", "balance"), 10), (get("b", "committed"), True)),
        case("invalid amounts inside the block",
             (new("Account", 10, save="acc"), obj("Account")), (new("Batch", ref("acc"), save="b"), obj("Batch")),
             (with_("b", [{"do": "call", "obj": "b", "method": "add", "args": [0]},
                          {"do": "call", "obj": "b", "method": "add", "args": [True]},
                          {"do": "call", "obj": "b", "method": "add", "args": [2.5]},
                          {"do": "call", "obj": "b", "method": "add", "args": [4]}]),
              {"body": [{"error": "ValueError"}, {"error": "ValueError"}, {"error": "ValueError"}, None], "error": None}),
             (get("acc", "balance"), 14)),
        case("exact zero balance is allowed",
             (new("Account", 30, save="acc"), obj("Account")), (new("Batch", ref("acc"), save="b"), obj("Batch")),
             (with_("b", [{"do": "call", "obj": "b", "method": "add", "args": [-30]}]), {"body": [None], "error": None}),
             (get("acc", "balance"), 0), (get("b", "committed"), True)),
        case("discarded batch cannot be reused",
             (new("Account", 5, save="acc"), obj("Account")), (new("Batch", ref("acc"), save="b"), obj("Batch")),
             (with_("b", [], raise_="KeyError"), {"body": [], "error": "KeyError"}),
             (with_("b", []), {"body": [], "error": "RuntimeError"}), (get("acc", "balance"), 5)),
        case("two batches on one account",
             (new("Account", 50, save="acc"), obj("Account")), (new("Batch", ref("acc"), save="b1"), obj("Batch")),
             (new("Batch", ref("acc"), save="b2"), obj("Batch")),
             (with_("b1", [{"do": "call", "obj": "b1", "method": "add", "args": [-40]}]), {"body": [None], "error": None}),
             (with_("b2", [{"do": "call", "obj": "b2", "method": "add", "args": [-40]}]), {"body": [None], "error": "ValueError"}),
             (get("acc", "balance"), 10)),
        case("invalid account and an empty batch",
             (new("Account", -1), error("ValueError")), (new("Account", 0, save="acc"), obj("Account")),
             (new("Batch", ref("acc"), save="b"), obj("Batch")), (get("b", "committed"), False),
             (with_("b", []), {"body": [], "error": None}), (get("b", "committed"), True), (get("acc", "balance"), 0)),
        case("intermediate negative sum is fine",
             (new("Account", 10, save="acc"), obj("Account")), (new("Batch", ref("acc"), save="b"), obj("Batch")),
             (with_("b", [{"do": "call", "obj": "b", "method": "add", "args": [-50]},
                          {"do": "call", "obj": "b", "method": "add", "args": [45]}]), {"body": [None, None], "error": None}),
             (get("acc", "balance"), 5)),
    ],
    "generate": lambda rng: (lambda balance: (
        [new("Account", balance, save="acc"), new("Batch", ref("acc"), save="b")]
        + ([{"do": "call", "obj": "b", "method": "add", "args": [1]}] if rng.random() < 0.2 else [])
        + [with_("b", [{"do": "call", "obj": "b", "method": "add", "args": [rng.choice([-40, -10, -1, 0, 1, 25, 60, True])]}
                       for _ in range(rng.randint(0, 4))]
                 + ([{"do": "get", "obj": "b", "attr": "pending"}] if rng.random() < 0.5 else []),
                 raise_=rng.choice([None, None, None, "RuntimeError", "KeyError"]))]
        + ([with_("b", [])] if rng.random() < 0.2 else [])
        + [get("acc", "balance"), get("b", "committed"), get("b", "pending")]))(rng.randint(0, 80)),
    "mutations": [
        {"name": "suppresses exceptions", "old": '            self._state = "discarded"\n            return False\n',
         "new": '            self._state = "discarded"\n            return True\n'},
        {"name": "applies on error", "old": '        if exc_type is not None:\n            self._state = "discarded"\n            return False\n', "new": ""},
        {"name": "overdraft not checked", "old": "if self.account.balance + total < 0:", "new": "if False:"},
        {"name": "reusable batch", "old": 'if self._state != "new":', "new": 'if self._state == "open":'},
    ],
    "sources": ["https://docs.python.org/3.11/reference/datamodel.html#context-managers",
                "https://docs.python.org/3.11/reference/compound_stmts.html#the-with-statement"],
}
