"""Original exercise: keep state in a class and make its instances callable."""
from cojudge.oop.steps import builtin, case, check, error, get, invoke, new, obj

SPEC = {
    "number": 7, "slug": "callable-throttle", "title": "Make an instance callable",
    "difficulty": "Medium", "time": 30, "level": 2,
    "prerequisites": "Exercise 06. Instance state.",
    "learn": """`__call__` lets you call an object like a function: `throttle(12)` runs
`throttle.__call__(12)`. A callable object is useful when a "function" must remember something
between calls, and you also want to inspect that memory or configure it.

```python
class Counter:
    def __init__(self):
        self.count = 0

    def __call__(self):
        self.count += 1
        return self.count
```

`callable(obj)` is `True` when the object has `__call__`. A `collections.deque` is a good
container for a sliding window: append new items on the right, and `popleft()` old items.""",
    "scenario": """An API gateway limits each client to a number of requests in a time window, for
example 3 requests in any 10 seconds. The gateway calls the client's throttle object with the
current time for each request. The object answers `True` (allow) or `False` (reject).""",
    "task": """Write the class `Throttle`.

- `Throttle(limit, window)`: both are integers. A value below 1 raises `ValueError`.
- `throttle(now)`: `now` is an integer time in seconds. Times never decrease from one call to the
  next. The window for this call holds the times `t` of accepted calls with
  `now - window < t <= now`. If the window holds fewer than `limit` calls, accept: record `now`
  and return `True`. Otherwise return `False`. A rejected call is **not** recorded.
- `accepted` and `rejected`: read-only properties. The number of calls that returned `True` and
  `False`.
- `repr(throttle)` returns `Throttle(limit=3, window=10)` with the real values.""",
    "constraints": ["Times are from 0 to 1,000,000.", "At most 80 steps per test."],
    "hints": ["Before you decide, remove recorded times that are `<= now - window`.",
              "A call exactly `window` seconds after an accepted call is outside that call's window."],
    "starter": '''class Throttle:
    def __init__(self, limit: int, window: int):
        raise NotImplementedError

    def __call__(self, now: int) -> bool:
        raise NotImplementedError

    @property
    def accepted(self) -> int:
        raise NotImplementedError

    @property
    def rejected(self) -> int:
        raise NotImplementedError

    def __repr__(self) -> str:
        raise NotImplementedError
''',
    "reference": '''from collections import deque


class Throttle:
    def __init__(self, limit: int, window: int):
        if limit < 1 or window < 1:
            raise ValueError("limit and window must be at least 1")
        self.limit = limit
        self.window = window
        self._times: deque[int] = deque()
        self._accepted = 0
        self._rejected = 0

    def __call__(self, now: int) -> bool:
        while self._times and self._times[0] <= now - self.window:
            self._times.popleft()
        if len(self._times) < self.limit:
            self._times.append(now)
            self._accepted += 1
            return True
        self._rejected += 1
        return False

    @property
    def accepted(self) -> int:
        return self._accepted

    @property
    def rejected(self) -> int:
        return self._rejected

    def __repr__(self) -> str:
        return f"Throttle(limit={self.limit}, window={self.window})"
''',
    "facts": ["callable Throttle", "property Throttle accepted", "property Throttle rejected"],
    "java": '''static class Throttle implements Obj {
    long limit, window, accepted, rejected; ArrayDeque<Long> times = new ArrayDeque<>();
    public String type() { return "Throttle"; }
}
Object step(Map<String,Object> op) {
    String d = s(op.get("do"));
    if (d.equals("new")) {
        Throttle t = new Throttle();
        t.limit = lng(arg(op, 0, "limit", MISSING)); t.window = lng(arg(op, 1, "window", MISSING));
        if (t.limit < 1 || t.window < 1) throw err("ValueError");
        return t;
    }
    Throttle t = (Throttle) target(op);
    if (d.equals("invoke")) {
        long now = lng(args(op).get(0));
        while (!t.times.isEmpty() && t.times.peekFirst() <= now - t.window) t.times.pollFirst();
        if (t.times.size() < t.limit) { t.times.addLast(now); t.accepted++; return true; }
        t.rejected++; return false;
    }
    if (d.equals("get")) {
        String a = s(op.get("attr"));
        if (a.equals("accepted")) return t.accepted;
        if (a.equals("rejected")) return t.rejected;
        if (a.equals("limit")) return t.limit;
        if (a.equals("window")) return t.window;
    }
    if (d.equals("repr")) return "Throttle(limit=" + t.limit + ", window=" + t.window + ")";
    throw err("AttributeError");
}
''',
    "approach": """The deque holds only accepted times inside the current window. Each call first
removes expired times from the left, then compares the remaining count with the limit. Every time
enters and leaves the deque once, so a call costs amortized O(1), and memory is O(limit).
Rejected calls are counted but not stored, so a burst of rejections cannot extend a block.""",
    "example_notes": [
        "Limit 2 in 10 seconds: calls at 0 and 1 pass, the call at 5 is rejected.",
        "At time 10 the call from time 0 is outside the window (10 - 10 < t is false for t = 0). One slot is free.",
        "Rejected calls are not recorded, so they do not keep the client blocked.",
    ],
    "cases": [
        case("limit reached",
             (new("Throttle", 2, 10, save="t"), obj("Throttle")), (invoke("t", 0), True), (invoke("t", 1), True),
             (invoke("t", 5), False)),
        case("window boundary",
             (new("Throttle", 2, 10, save="t"), obj("Throttle")), (invoke("t", 0), True), (invoke("t", 1), True),
             (invoke("t", 10), True), (invoke("t", 10), False), (invoke("t", 11), True)),
        case("rejected calls are not recorded",
             (new("Throttle", 1, 5, save="t"), obj("Throttle")), (invoke("t", 0), True), (invoke("t", 4), False),
             (invoke("t", 5), True), (get("t", "rejected"), 1), (get("t", "accepted"), 2)),
        case("invalid configuration",
             (new("Throttle", 0, 10), error("ValueError")), (new("Throttle", 3, 0), error("ValueError")),
             (new("Throttle", -1, -1), error("ValueError"))),
        case("repr and counters start at zero",
             (new("Throttle", 3, 60, save="t"), obj("Throttle")), (builtin("repr", "t"), "Throttle(limit=3, window=60)"),
             (get("t", "accepted"), 0), (get("t", "rejected"), 0)),
        case("same timestamp burst",
             (new("Throttle", 3, 1, save="t"), obj("Throttle")), (invoke("t", 7), True), (invoke("t", 7), True),
             (invoke("t", 7), True), (invoke("t", 7), False), (invoke("t", 8), True)),
        case("window of one second",
             (new("Throttle", 1, 1, save="t"), obj("Throttle")), (invoke("t", 0), True), (invoke("t", 1), True),
             (invoke("t", 1), False), (invoke("t", 2), True)),
        case("sliding, not fixed buckets",
             (new("Throttle", 2, 10, save="t"), obj("Throttle")), (invoke("t", 8), True), (invoke("t", 9), True),
             (invoke("t", 11), False), (invoke("t", 18), True), (invoke("t", 18), False), (invoke("t", 19), True)),
        case("long gap clears the window",
             (new("Throttle", 2, 100, save="t"), obj("Throttle")), (invoke("t", 0), True), (invoke("t", 0), True),
             (invoke("t", 50), False), (invoke("t", 1000000), True), (invoke("t", 1000000), True), (invoke("t", 1000000), False)),
        case("two throttles are independent",
             (new("Throttle", 1, 10, save="a"), obj("Throttle")), (new("Throttle", 1, 10, save="b"), obj("Throttle")),
             (invoke("a", 0), True), (invoke("b", 0), True), (invoke("a", 1), False), (get("b", "rejected"), 0)),
        case("counters are read-only",
             (new("Throttle", 1, 1, save="t"), obj("Throttle")), ({"do": "set", "obj": "t", "attr": "accepted", "value": 5}, error("AttributeError")),
             (get("t", "accepted"), 0)),
        case("structure",
             (new("Throttle", window=5, limit=2, save="t"), obj("Throttle")), (check("callable", "t"), True),
             (builtin("repr", "t"), "Throttle(limit=2, window=5)"), (check("property", "Throttle", "accepted"), True)),
    ],
    "generate": lambda rng: (lambda limit, window: (lambda times: (
        [new("Throttle", limit, window, save="t")]
        + [invoke("t", now) for now in times] + [get("t", "accepted"), get("t", "rejected")]))(
        sorted(rng.randint(0, window * 4) for _ in range(rng.randint(3, 25)))))(
        rng.randint(1, 4), rng.choice([1, 2, 5, 10, 30])),
    "mutations": [
        {"name": "boundary call still in the window", "old": "self._times[0] <= now - self.window",
         "new": "self._times[0] < now - self.window"},
        {"name": "rejected calls are recorded", "old": "        self._rejected += 1\n        return False\n",
         "new": "        self._times.append(now)\n        self._rejected += 1\n        return False\n"},
        {"name": "limit off by one", "old": "if len(self._times) < self.limit:", "new": "if len(self._times) <= self.limit:"},
    ],
    "sources": ["https://docs.python.org/3.11/reference/datamodel.html#object.__call__",
                "https://docs.python.org/3.11/library/collections.html#collections.deque"],
}
