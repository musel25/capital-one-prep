"""Original exercise: alternative constructors with classmethod."""
from cojudge.oop.steps import builtin, call, case, check, error, get, new, obj, op, ref

SPEC = {
    "number": 5, "slug": "duration-alternative-constructors", "title": "Alternative constructors",
    "difficulty": "Medium", "time": 30, "level": 1,
    "prerequisites": "Exercises 01–04. Static methods and `__repr__`.",
    "learn": """A class has one `__init__`, but you often get data in several formats. An
**alternative constructor** is a `@classmethod` that converts one format and then calls the class.
A class method receives the class as its first argument, named `cls` by convention.

```python
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    @classmethod
    def from_text(cls, text):          # "3,4"
        x, y = text.split(",")
        return cls(int(x), int(y))
```

Return `cls(...)`, not `Point(...)`. Then a subclass that calls `from_text` gets an instance of
the subclass. This is how `dict.fromkeys` and `datetime.fromisoformat` work.

`__eq__(self, other)` defines `==`. Return `NotImplemented` for a type that you do not support;
Python then tries the other operand and finally compares identity.""",
    "scenario": """A fitness app records workout durations. The phone sends seconds, the coach types
minutes, and imported files contain text like `1h 5m 30s`. All three must become the same
`Duration` type. A `Lap` is a special duration for one lap of a track.""",
    "task": """Write the class `Duration`. The starter already contains `class Lap(Duration): pass`.
Keep it.

- `Duration(seconds)`: `seconds` is an integer. Negative raises `ValueError`. Store it in the
  attribute `seconds`.
- `from_minutes(minutes)`: **class method**. Return an instance of `cls` with `minutes * 60`
  seconds.
- `from_text(text)`: **class method**. Return an instance of `cls`. The text has one, two, or
  three parts, separated by **single spaces**. Each part is digits followed by one unit: `h`
  (hours), `m` (minutes), or `s` (seconds). The units appear in the order `h`, `m`, `s`, and each
  unit at most once. A part can be larger than one unit, for example `90m`. Any other text raises
  `ValueError`, including an empty string, a sign, a double space, or a repeated unit.
- `str(duration)`: write the duration with hours, minutes (0–59), and seconds (0–59). Show only
  parts that are not zero, in the order `h m s`, separated by spaces, for example `1h 5s`. Zero
  is `0s`.
- `a == b`: `True` when both are `Duration` instances (subclasses too) with the same `seconds`.
  For other types, return `NotImplemented`.""",
    "constraints": ["Values are at most 10,000,000 seconds.", "At most 40 steps per test."],
    "hints": ["Split on `\" \"` (not `split()`), so a double space makes an empty part that you reject.",
              "Keep the index of the last unit and require each new unit to come later in `\"hms\"`."],
    "starter": '''class Duration:
    def __init__(self, seconds: int):
        raise NotImplementedError

    @classmethod
    def from_minutes(cls, minutes: int) -> "Duration":
        raise NotImplementedError

    @classmethod
    def from_text(cls, text: str) -> "Duration":
        raise NotImplementedError

    def __str__(self) -> str:
        raise NotImplementedError

    def __eq__(self, other: object) -> bool:
        raise NotImplementedError


class Lap(Duration):
    pass
''',
    "reference": '''UNITS = {"h": 3600, "m": 60, "s": 1}


class Duration:
    def __init__(self, seconds: int):
        if seconds < 0:
            raise ValueError("a duration cannot be negative")
        self.seconds = seconds

    @classmethod
    def from_minutes(cls, minutes: int) -> "Duration":
        return cls(minutes * 60)

    @classmethod
    def from_text(cls, text: str) -> "Duration":
        total, last = 0, -1
        for part in text.split(" "):
            number, unit = part[:-1], part[-1:]
            if unit not in UNITS or not number.isdigit() or not number.isascii():
                raise ValueError(f"invalid part: {part!r}")
            position = "hms".index(unit)
            if position <= last:
                raise ValueError(f"unit out of order: {part!r}")
            last = position
            total += int(number) * UNITS[unit]
        return cls(total)

    def __str__(self) -> str:
        hours, rest = divmod(self.seconds, 3600)
        minutes, seconds = divmod(rest, 60)
        parts = [f"{n}{u}" for n, u in ((hours, "h"), (minutes, "m"), (seconds, "s")) if n]
        return " ".join(parts) or "0s"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Duration):
            return NotImplemented
        return self.seconds == other.seconds


class Lap(Duration):
    pass
''',
    "facts": ["classmethod Duration from_minutes", "classmethod Duration from_text", "subclass Lap Duration"],
    "java": '''static class Duration implements Obj {
    long seconds; String kind;
    Duration(String kind, long seconds) { if (seconds < 0) throw err("ValueError"); this.kind = kind; this.seconds = seconds; }
    public String type() { return kind; }
}
static long parseText(String text) {
    long total = 0; int last = -1;
    for (String part : text.split(" ", -1)) {
        if (part.length() < 2) throw err("ValueError");
        int position = "hms".indexOf(part.charAt(part.length() - 1));
        String digits = part.substring(0, part.length() - 1);
        if (position < 0 || !digits.matches("[0-9]+") || position <= last) throw err("ValueError");
        last = position;
        total += Long.parseLong(digits) * new long[]{3600, 60, 1}[position];
    }
    return total;
}
Object step(Map<String,Object> op) {
    String d = s(op.get("do"));
    Object t = target(op);
    if (d.equals("new")) return new Duration((String) t, lng(arg(op, 0, "seconds", MISSING)));
    if (d.equals("call") && t instanceof String) {
        String m = s(op.get("method"));
        if (m.equals("from_minutes")) return new Duration((String) t, lng(args(op).get(0)) * 60);
        if (m.equals("from_text")) return new Duration((String) t, parseText(s(args(op).get(0))));
    }
    if (d.equals("op")) {
        Object l = val(op.get("left")), r = val(op.get("right"));
        boolean same = l instanceof Duration && r instanceof Duration ? ((Duration) l).seconds == ((Duration) r).seconds : l == r;
        return s(op.get("op")).equals("==") ? same : !same;
    }
    Duration x = (Duration) t;
    if (d.equals("get") && s(op.get("attr")).equals("seconds")) return x.seconds;
    if (d.equals("str")) {
        long h = x.seconds / 3600, m = x.seconds % 3600 / 60, sec = x.seconds % 60;
        List<String> parts = new ArrayList<>();
        if (h > 0) parts.add(h + "h"); if (m > 0) parts.add(m + "m"); if (sec > 0) parts.add(sec + "s");
        return parts.isEmpty() ? "0s" : String.join(" ", parts);
    }
    throw err("AttributeError");
}
''',
    "approach": """Both class methods convert their input and then call `cls(...)`, so `Lap.from_text`
returns a `Lap`, and validation stays in one place, `__init__`. The parser splits on single
spaces and tracks the last unit's position in `"hms"`, which rejects repeats and wrong order in
one comparison. `isdigit` alone also accepts other Unicode digits, so `isascii` is added.
`__eq__` returns `NotImplemented` for foreign types instead of `False`, which lets Python try the
other operand.""",
    "example_notes": [
        "from_minutes and from_text build the same 5400-second duration. str normalizes 90m to 1h 30m.",
        "Called on Lap, the class methods return a Lap. A hard-coded Duration(...) would return the wrong class.",
        "A double space, a repeated unit, and a wrong order are all rejected.",
    ],
    "cases": [
        case("three formats agree",
             (call("Duration", "from_minutes", 90, save="a"), obj("Duration")), (call("Duration", "from_text", "90m", save="b"), obj("Duration")),
             (op(ref("a"), "==", ref("b")), True), (builtin("str", "b"), "1h 30m"), (get("a", "seconds"), 5400)),
        case("class methods respect the subclass",
             (call("Lap", "from_minutes", 2, save="l"), obj("Lap")), (call("Lap", "from_text", "1m 5s"), obj("Lap")),
             (builtin("str", "l"), "2m")),
        case("invalid text",
             (call("Duration", "from_text", "1h  5m"), error("ValueError")), (call("Duration", "from_text", "5m 5m"), error("ValueError")),
             (call("Duration", "from_text", "5s 1m"), error("ValueError"))),
        case("full text and str",
             (call("Duration", "from_text", "2h 15m 10s", save="d"), obj("Duration")), (get("d", "seconds"), 8110),
             (builtin("str", "d"), "2h 15m 10s")),
        case("str hides zero parts",
             (new("Duration", 3605, save="a"), obj("Duration")), (builtin("str", "a"), "1h 5s"),
             (new("Duration", 0, save="z"), obj("Duration")), (builtin("str", "z"), "0s"),
             (new("Duration", 59, save="s"), obj("Duration")), (builtin("str", "s"), "59s")),
        case("negative seconds",
             (new("Duration", -1), error("ValueError")), (call("Duration", "from_minutes", -2), error("ValueError")),
             (call("Duration", "from_minutes", 0, save="z"), obj("Duration")), (builtin("str", "z"), "0s")),
        case("empty text and bad parts",
             (call("Duration", "from_text", ""), error("ValueError")), (call("Duration", "from_text", "h"), error("ValueError")),
             (call("Duration", "from_text", "-5s"), error("ValueError")), (call("Duration", "from_text", "5x"), error("ValueError")),
             (call("Duration", "from_text", "1.5h"), error("ValueError"))),
        case("spacing and unit rules",
             (call("Duration", "from_text", " 5s"), error("ValueError")), (call("Duration", "from_text", "5s "), error("ValueError")),
             (call("Duration", "from_text", "1h5m"), error("ValueError")), (call("Duration", "from_text", "5 s"), error("ValueError"))),
        case("large parts are normalized",
             (call("Duration", "from_text", "0h 0m 3661s", save="d"), obj("Duration")), (builtin("str", "d"), "1h 1m 1s"),
             (call("Duration", "from_text", "100h", save="e"), obj("Duration")), (builtin("str", "e"), "100h")),
        case("equality across classes",
             (call("Lap", "from_text", "1m", save="l"), obj("Lap")), (new("Duration", 60, save="d"), obj("Duration")),
             (op(ref("l"), "==", ref("d")), True), (op(ref("d"), "==", 60), False), (op(ref("d"), "!=", ref("l")), False)),
        case("unequal durations",
             (new("Duration", 61, save="a"), obj("Duration")), (call("Duration", "from_minutes", 1, save="b"), obj("Duration")),
             (op(ref("a"), "==", ref("b")), False), (op(ref("a"), "!=", ref("b")), True)),
        case("structure",
             (check("classmethod", "Duration", "from_minutes"), True), (check("classmethod", "Duration", "from_text"), True),
             (check("subclass", "Lap", of="Duration"), True), (new("Lap", seconds=7, save="l"), obj("Lap")), (builtin("str", "l"), "7s")),
    ],
    "generate": lambda rng: (lambda texts: (
        [call(rng.choice(["Duration", "Lap"]), "from_minutes", rng.randint(0, 600), save=name) for name in "ab"]
        + [rng.choice([call(rng.choice(["Duration", "Lap"]), "from_text", rng.choice(texts), save="b"),
                       builtin("str", "a"), builtin("str", "b"), op(ref("a"), "==", ref("b")),
                       new("Duration", rng.choice([0, 1, 59, 60, 3599, 3600, 86399, rng.randint(0, 10 ** 6)]), save="a"),
                       get("a", "seconds")])
           for _ in range(rng.randint(4, 12))]))(
        ["1h", "59m 59s", "1h 0m 0s", "0s", "2h 30s", "45m", "7h 7m 7s", "1h 1h", "1m 1h", "1 h", "", "10s 5m",
         "3h  1s", "120s", "0h 60m", "x5s"]),
    "mutations": [
        {"name": "hard-coded class", "old": "        return cls(minutes * 60)\n", "new": "        return Duration(minutes * 60)\n"},
        {"name": "repeated unit accepted", "old": "if position <= last:", "new": "if position < last:"},
        {"name": "zero shown as empty", "old": 'or "0s"', "new": 'or ""'},
        {"name": "split collapses spaces", "old": 'text.split(" ")', "new": "text.split()"},
    ],
    "sources": ["https://docs.python.org/3.11/library/functions.html#classmethod",
                "https://docs.python.org/3.11/library/constants.html#NotImplemented"],
}
