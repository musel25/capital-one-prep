"""Original exercise: subclass the list built-in with validation."""
from cojudge.oop.steps import builtin, call, case, check, error, get, item, new, setitem

SPEC = {
    "number": 16, "slug": "validated-list", "title": "Subclass the list built-in",
    "difficulty": "Medium", "time": 30, "level": 4,
    "prerequisites": "Exercise 15. Subclassing `dict` and its trap.",
    "learn": """`list` has the same trap as `dict`: its methods do not call each other. `extend`,
`insert`, the constructor, and `lst[i] = x` all skip an overridden `append`. A validated list
must check every way in.

**All-or-nothing:** when one value in `extend([5, 200])` is invalid, the list must not keep the
`5`. Check every value first, then add them all. A half-finished change is a common bug in
real systems.

```python
def extend(self, values):
    values = [self._check(v) for v in values]   # may raise; nothing changed yet
    super().extend(values)
```

`list(values)` first is also important, because `values` can be an iterator that you can read
only once.""",
    "scenario": """A grading tool stores exam scores for one class. A score is a whole number from
0 to 100. The tool imports scores from files, so one bad value must not corrupt the list. The
list must still behave like a normal Python list for the rest of the code.""",
    "task": """Write `Scores`, a subclass of `list`. A **valid score** is an `int` (not a `bool`) from
0 to 100. A value with the wrong type raises `TypeError`. An integer outside 0–100 raises
`ValueError`.

- `Scores(values=())`: validate every value. Invalid values raise as above.
- `append(value)`, `insert(index, value)`, and `scores[index] = value` (integer index): validate
  the value first, then behave like `list`.
- `extend(values)`: all-or-nothing. If any value is invalid, raise and add nothing.
- `average`: read-only property. `sum // len`. An empty list raises `ValueError`.
- `top(n)`: return a plain list of the `n` highest scores, highest first.

Other `list` behavior (indexing, `len`, `sorted`) works as usual. The driver shows the object as
a JSON list.""",
    "constraints": ["At most 50 values and 40 steps per test."],
    "hints": ["Write one `_check(value)` helper and call it from every method that adds a value.",
              "In `__setitem__`, validate the value before you call `super().__setitem__`."],
    "starter": '''class Scores(list):
    def __init__(self, values=()):
        raise NotImplementedError

    def append(self, value: int) -> None:
        raise NotImplementedError

    def extend(self, values) -> None:
        raise NotImplementedError

    def insert(self, index: int, value: int) -> None:
        raise NotImplementedError

    def __setitem__(self, index: int, value: int) -> None:
        raise NotImplementedError

    @property
    def average(self) -> int:
        raise NotImplementedError

    def top(self, n: int) -> list[int]:
        raise NotImplementedError
''',
    "reference": '''class Scores(list):
    def __init__(self, values=()):
        super().__init__()
        self.extend(values)

    @staticmethod
    def _check(value: int) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"a score must be an integer, not {type(value).__name__}")
        if not 0 <= value <= 100:
            raise ValueError(f"a score must be from 0 to 100, not {value}")
        return value

    def append(self, value: int) -> None:
        super().append(self._check(value))

    def extend(self, values) -> None:
        values = [self._check(v) for v in values]
        super().extend(values)

    def insert(self, index: int, value: int) -> None:
        super().insert(index, self._check(value))

    def __setitem__(self, index: int, value: int) -> None:
        super().__setitem__(index, self._check(value))

    @property
    def average(self) -> int:
        if not self:
            raise ValueError("no scores")
        return sum(self) // len(self)

    def top(self, n: int) -> list[int]:
        return sorted(self, reverse=True)[:n]
''',
    "facts": ["subclass Scores list", "instance Scores list", "property Scores average"],
    "java": '''static class Scores implements Obj {
    List<Object> data = new ArrayList<>();
    public String type() { return "Scores"; }
    public Object plain() { return new ArrayList<Object>(data); }
    static Object check(Object v) {
        if (!isInt(v)) throw err("TypeError");
        if (lng(v) < 0 || lng(v) > 100) throw err("ValueError");
        return lng(v);
    }
    void extend(Object values) { List<Object> ok = new ArrayList<>(); for (Object v : arr(values)) ok.add(check(v)); data.addAll(ok); }
    int index(long i) { long n = data.size(); long k = i < 0 ? i + n : i; if (k < 0 || k >= n) throw err("IndexError"); return (int) k; }
}
Object step(Map<String,Object> op) {
    String d = s(op.get("do"));
    if (d.equals("new")) { Scores s = new Scores(); s.extend(arg(op, 0, "values", list())); return s; }
    Scores sc = (Scores) target(op);
    if (d.equals("len")) return (long) sc.data.size();
    if (d.equals("list")) return new ArrayList<Object>(sc.data);
    if (d.equals("sorted")) { List<Object> out = new ArrayList<>(sc.data); out.sort((a, b) -> Long.compare(lng(a), lng(b))); return out; }
    if (d.equals("item")) return sc.data.get(sc.index(lng(val(op.get("key")))));
    if (d.equals("setitem")) { Object v = Scores.check(val(op.get("value"))); sc.data.set(sc.index(lng(val(op.get("key")))), v); return null; }
    if (d.equals("get") && s(op.get("attr")).equals("average")) {
        if (sc.data.isEmpty()) throw err("ValueError");
        long sum = 0; for (Object v : sc.data) sum += lng(v); return sum / sc.data.size();
    }
    if (d.equals("call")) {
        String m = s(op.get("method")); List<Object> a = args(op);
        if (m.equals("append")) { sc.data.add(Scores.check(a.get(0))); return null; }
        if (m.equals("extend")) { sc.extend(a.get(0)); return null; }
        if (m.equals("insert")) {
            Object v = Scores.check(a.get(1)); long n = sc.data.size(), i = lng(a.get(0));
            long k = i < 0 ? Math.max(0, i + n) : Math.min(i, n);
            sc.data.add((int) k, v); return null;
        }
        if (m.equals("top")) {
            List<Object> out = new ArrayList<>(sc.data); out.sort((x, y) -> Long.compare(lng(y), lng(x)));
            return new ArrayList<Object>(out.subList(0, (int) Math.max(0, Math.min(lng(a.get(0)), out.size()))));
        }
    }
    throw err("AttributeError");
}
''',
    "approach": """One `_check` helper holds the rule, and every entry point calls it: the
constructor (through `extend`), `append`, `insert`, and item assignment. `extend` builds the
validated list before it changes anything, so an invalid value leaves the list unchanged.
`average` uses integer division. `top` sorts a copy in O(n log n).""",
    "example_notes": [
        "Values are validated, then the object behaves like a list. 80 + 95 + 70 = 245, and 245 // 3 = 81.",
        "extend is all-or-nothing: 200 is invalid, so the 50 is not added either.",
        "A string raises TypeError. True is a bool, so it is rejected although bool is a subclass of int.",
    ],
    "cases": [
        case("valid list and average",
             (new("Scores", [80, 95], save="s"), [80, 95]), (call("s", "append", 70), None), (get("s", "average"), 81),
             (call("s", "top", 2), [95, 80])),
        case("extend is all-or-nothing",
             (new("Scores", [10], save="s"), [10]), (call("s", "extend", [50, 200]), error("ValueError")),
             (builtin("list", "s"), [10]), (builtin("len", "s"), 1)),
        case("wrong types",
             (new("Scores", save="s"), []), (call("s", "append", "90"), error("TypeError")), (call("s", "append", True), error("TypeError")),
             (call("s", "append", 9.5), error("TypeError")), (builtin("list", "s"), [])),
        case("constructor validates",
             (new("Scores", [1, 2, 101]), error("ValueError")), (new("Scores", [1, None]), error("TypeError")),
             (new("Scores", [0, 100], save="s"), [0, 100])),
        case("insert validates",
             (new("Scores", [10, 30], save="s"), [10, 30]), (call("s", "insert", 1, 20), None), (call("s", "insert", 0, -1), error("ValueError")),
             (builtin("list", "s"), [10, 20, 30])),
        case("item assignment validates",
             (new("Scores", [10, 20], save="s"), [10, 20]), (setitem("s", 0, 100), None), (setitem("s", 1, 101), error("ValueError")),
             (setitem("s", -1, False), error("TypeError")), (builtin("list", "s"), [100, 20])),
        case("index errors after a valid value",
             (new("Scores", [10], save="s"), [10]), (setitem("s", 5, 50), error("IndexError")), (item("s", -1), 10),
             (item("s", 3), error("IndexError"))),
        case("empty average",
             (new("Scores", save="s"), []), (get("s", "average"), error("ValueError")), (call("s", "top", 3), [])),
        case("top with ties and large n",
             (new("Scores", [50, 90, 50, 70], save="s"), [50, 90, 50, 70]), (call("s", "top", 3), [90, 70, 50]),
             (call("s", "top", 10), [90, 70, 50, 50]), (call("s", "top", 0), []), (builtin("list", "s"), [50, 90, 50, 70])),
        case("normal list behavior",
             (new("Scores", [3, 1, 2], save="s"), [3, 1, 2]), (builtin("sorted", "s"), [1, 2, 3]), (builtin("len", "s"), 3),
             (check("instance", "s", of="list"), True)),
        case("valid extend",
             (new("Scores", save="s"), []), (call("s", "extend", [0, 100, 55]), None), (get("s", "average"), 51),
             (call("s", "extend", []), None), (builtin("list", "s"), [0, 100, 55])),
        case("insert positions",
             (new("Scores", [5], save="s"), [5]), (call("s", "insert", -1, 4), None), (call("s", "insert", 99, 6), None),
             (builtin("list", "s"), [4, 5, 6]), (check("subclass", "Scores", of="list"), True)),
    ],
    "generate": lambda rng: (lambda pool: (
        [new("Scores", [rng.randint(0, 100) for _ in range(rng.randint(0, 5))], save="s")]
        + [rng.choice([call("s", "append", rng.choice(pool)), call("s", "extend", rng.sample(pool, rng.randint(0, 3))),
                       call("s", "insert", rng.randint(-3, 5), rng.choice(pool)), setitem("s", rng.randint(-2, 4), rng.choice(pool)),
                       get("s", "average"), call("s", "top", rng.randint(0, 4)), builtin("list", "s")])
           for _ in range(rng.randint(4, 12))]))([0, 1, 50, 99, 100, 101, -1, "7", True, 3.0, 42, 88]),
    "mutations": [
        {"name": "extend adds the valid part", "old": "        values = [self._check(v) for v in values]\n        super().extend(values)\n",
         "new": "        for v in values:\n            super().append(self._check(v))\n"},
        {"name": "constructor skips validation", "old": "        super().__init__()\n        self.extend(values)\n",
         "new": "        super().__init__(values)\n"},
        {"name": "booleans accepted", "old": "isinstance(value, bool) or ", "new": ""},
        {"name": "item assignment not validated", "old": "super().__setitem__(index, self._check(value))", "new": "super().__setitem__(index, value)"},
    ],
    "sources": ["https://docs.python.org/3.11/library/stdtypes.html#lists",
                "https://docs.python.org/3.11/library/collections.html#collections.UserList"],
}
