"""Original exercise: a read-only computed property."""
from cojudge.oop.steps import call, case, check, error, get, new, obj, put

SPEC = {
    "number": 1, "slug": "countdown-property", "title": "Write a read-only property",
    "difficulty": "Easy", "time": 15, "level": 1,
    "prerequisites": "Functions, f-strings, and a basic class with `__init__`.",
    "learn": """A **property** is a method that you read like an attribute. Put `@property` above a
method, and `timer.display` calls it with no parentheses. Python computes the value each time you
read it, so the result is never out of date. If the class defines no setter, assignment to the
property raises `AttributeError`. That makes the value read-only.

```python
class Box:
    def __init__(self, width):
        self.width = width

    @property
    def area(self):
        return self.width * self.width
```

Use a property for a value that you calculate from other attributes. Do not calculate it once in
`__init__` and store it: a later change to `width` would leave a stale `area`.""",
    "scenario": """A kitchen timer app keeps the remaining time as a number of seconds. The screen
shows the time as minutes and seconds, for example `1:05`. The screen must always match the
current number of seconds.""",
    "task": """Write the class `Countdown`.

- `Countdown(seconds)`: `seconds` is an integer. Store it in the public attribute `seconds`. If it
  is negative, raise `ValueError`.
- `display`: a read-only **property**. Return `"M:SS"`: whole minutes, a colon, and the remaining
  seconds as two digits. Minutes have no padding and can be more than 59. Examples: `0` → `"0:00"`,
  `65` → `"1:05"`, `3600` → `"60:00"`.
- `finished`: a read-only **property**. Return `True` when `seconds` is `0`.
- `tick()`: decrease `seconds` by 1, but never below 0. Return the new value of `seconds`.

Code can assign a new integer to `seconds` at any time. `display` and `finished` must then show
the new value. Assignment to `display` or `finished` raises `AttributeError`.""",
    "constraints": ["`seconds` is an integer from -10 to 1,000,000.", "At most 60 steps per test."],
    "hints": ["Use `divmod(self.seconds, 60)` for the minutes and the remaining seconds.",
              "The format `f\"{n:02d}\"` pads a number to two digits."],
    "starter": '''class Countdown:
    def __init__(self, seconds: int):
        raise NotImplementedError

    @property
    def display(self) -> str:
        raise NotImplementedError

    @property
    def finished(self) -> bool:
        raise NotImplementedError

    def tick(self) -> int:
        raise NotImplementedError
''',
    "reference": '''class Countdown:
    def __init__(self, seconds: int):
        if seconds < 0:
            raise ValueError("seconds must not be negative")
        self.seconds = seconds

    @property
    def display(self) -> str:
        minutes, rest = divmod(self.seconds, 60)
        return f"{minutes}:{rest:02d}"

    @property
    def finished(self) -> bool:
        return self.seconds == 0

    def tick(self) -> int:
        if self.seconds > 0:
            self.seconds -= 1
        return self.seconds
''',
    "facts": ["property Countdown display", "property Countdown finished"],
    "java": '''static class Countdown implements Obj { long seconds; public String type() { return "Countdown"; } }
Object step(Map<String,Object> op) {
    String d = s(op.get("do"));
    if (d.equals("new")) {
        long v = lng(arg(op, 0, "seconds", MISSING));
        if (v < 0) throw err("ValueError");
        Countdown c = new Countdown(); c.seconds = v; return c;
    }
    Countdown c = (Countdown) target(op);
    String a = op.containsKey("attr") ? s(op.get("attr")) : "";
    if (d.equals("get")) {
        if (a.equals("seconds")) return c.seconds;
        if (a.equals("display")) return (c.seconds / 60) + ":" + String.format("%02d", c.seconds % 60);
        if (a.equals("finished")) return c.seconds == 0;
    }
    if (d.equals("set")) {
        if (a.equals("display") || a.equals("finished")) throw err("AttributeError");
        if (a.equals("seconds")) c.seconds = lng(val(op.get("value")));
        return null;
    }
    if (d.equals("call") && s(op.get("method")).equals("tick")) { if (c.seconds > 0) c.seconds--; return c.seconds; }
    throw err("AttributeError");
}
''',
    "approach": """`display` and `finished` are properties, so each read uses the current `seconds`.
`divmod` gives minutes and the remaining seconds, and `:02d` pads the seconds. Neither property
has a setter, so Python rejects assignment with `AttributeError`. Each operation is O(1).""",
    "example_notes": [
        "65 seconds is 1 minute and 5 seconds, so the display is 1:05. The timer is not finished.",
        "After the code sets seconds to 9, display reads the new value. A stored copy would still say 1:00.",
        "A negative start raises ValueError. Assignment to the read-only display raises AttributeError.",
    ],
    "cases": [
        case("basic display",
             (new("Countdown", 65, save="t"), obj("Countdown")), (get("t", "display"), "1:05"),
             (get("t", "finished"), False)),
        case("display follows a changed attribute",
             (new("Countdown", 60, save="t"), obj("Countdown")), (put("t", "seconds", 9), None),
             (get("t", "display"), "0:09")),
        case("invalid start and read-only property",
             (new("Countdown", -1), error("ValueError")), (new("Countdown", 5, save="t"), obj("Countdown")),
             (put("t", "display", "9:99"), error("AttributeError")), (get("t", "display"), "0:05")),
        case("zero is valid and finished",
             (new("Countdown", 0, save="t"), obj("Countdown")), (get("t", "display"), "0:00"),
             (get("t", "finished"), True), (call("t", "tick"), 0), (get("t", "seconds"), 0)),
        case("tick crosses a minute",
             (new("Countdown", 61, save="t"), obj("Countdown")), (call("t", "tick"), 60),
             (get("t", "display"), "1:00"), (call("t", "tick"), 59), (get("t", "display"), "0:59")),
        case("tick reaches zero and stops",
             (new("Countdown", 2, save="t"), obj("Countdown")), (call("t", "tick"), 1), (call("t", "tick"), 0),
             (get("t", "finished"), True), (call("t", "tick"), 0), (get("t", "display"), "0:00")),
        case("minutes are not limited to 59",
             (new("Countdown", 3600, save="a"), obj("Countdown")), (get("a", "display"), "60:00"),
             (new("Countdown", 1000000, save="b"), obj("Countdown")), (get("b", "display"), "16666:40")),
        case("single-digit seconds are padded",
             (new("Countdown", 600, save="t"), obj("Countdown")), (get("t", "display"), "10:00"),
             (put("t", "seconds", 607), None), (get("t", "display"), "10:07")),
        case("finished becomes false after a reset",
             (new("Countdown", 1, save="t"), obj("Countdown")), (call("t", "tick"), 0), (get("t", "finished"), True),
             (put("t", "seconds", 30), None), (get("t", "finished"), False), (get("t", "display"), "0:30")),
        case("two timers keep separate state",
             (new("Countdown", 10, save="a"), obj("Countdown")), (new("Countdown", 20, save="b"), obj("Countdown")),
             (call("a", "tick"), 9), (get("b", "seconds"), 20), (get("a", "display"), "0:09")),
        case("finished is read-only",
             (new("Countdown", 3, save="t"), obj("Countdown")), (put("t", "finished", True), error("AttributeError")),
             (get("t", "finished"), False)),
        case("keyword argument and structure",
             (new("Countdown", seconds=59, save="t"), obj("Countdown")), (get("t", "display"), "0:59"),
             (check("property", "Countdown", "display"), True), (check("property", "Countdown", "finished"), True)),
    ],
    "generate": lambda rng: (
        [new("Countdown", rng.choice([-3, 0, 1, 59, 60, 61, 119, 3599, 3600, rng.randint(0, 99999)]), save="t")]
        + [rng.choice([call("t", "tick"), get("t", "display"), get("t", "finished"),
                       put("t", "seconds", rng.randint(0, 7200)), get("t", "seconds")])
           for _ in range(rng.randint(3, 12))]),
    "mutations": [
        {"name": "seconds are not padded", "old": 'f"{minutes}:{rest:02d}"', "new": 'f"{minutes}:{rest}"'},
        {"name": "zero is rejected", "old": "if seconds < 0:", "new": "if seconds <= 0:"},
        {"name": "tick goes below zero", "old": "if self.seconds > 0:", "new": "if True:"},
    ],
    "sources": ["https://docs.python.org/3.11/library/functions.html#property"],
}
