"""Original exercise: keep state in an instance, with a custom exception."""
from cojudge.oop.steps import call, case, check, error, get, new, obj

SPEC = {
    "number": 6, "slug": "promo-rotation-state", "title": "No promo twice: keep state in a class",
    "difficulty": "Easy", "time": 25, "level": 2,
    "prerequisites": "Level 1. Properties and returning copies of lists.",
    "learn": """An object remembers things between method calls. Create that state in `__init__`,
on `self`. Two common mistakes share state between objects:

- A **class attribute** such as `used = []` directly in the class body. All instances share that
  one list.
- A **mutable default argument** such as `def __init__(self, used=[])`. Python creates that list
  once, when it defines the function.

You can define your own exception: `class NoPromosLeft(Exception): pass`. A caller can then
catch exactly that error. `dict.fromkeys(items)` removes duplicates and keeps the first-seen
order, because dictionaries keep insertion order.""",
    "scenario": """An online shop gives each visitor a promo code from a campaign list. A visitor must
never get the same code twice. Each visitor's session has its own rotation object, so two
visitors never affect each other.""",
    "task": """Write the exception `NoPromosLeft` (a subclass of `Exception`) and the class
`PromoRotation`.

- `PromoRotation(codes)`: `codes` is a list of strings. Keep the first occurrence of each code,
  in the given order. Use your own copy of the list.
- `draw()`: mark and return the first code in order that is not used yet. When every code is
  used, raise `NoPromosLeft`.
- `skip(code)`: mark `code` as used without returning it. An unknown code raises `ValueError`.
  A code that is already used does not change anything. Return `None`.
- `used`: read-only property. A new list of the used codes, in the order they were marked.
- `remaining`: read-only property. The number of codes that are not used.
- `reset()`: mark every code as not used. Return `None`.

Every rotation has its own state.""",
    "constraints": ["At most 30 codes and 60 steps per test.", "Codes are non-empty strings."],
    "hints": ["Keep one list of unique codes and one list of used codes.",
              "Create both lists in `__init__`, not in the class body or a default argument."],
    "starter": '''class NoPromosLeft(Exception):
    pass


class PromoRotation:
    def __init__(self, codes: list[str]):
        raise NotImplementedError

    def draw(self) -> str:
        raise NotImplementedError

    def skip(self, code: str) -> None:
        raise NotImplementedError

    @property
    def used(self) -> list[str]:
        raise NotImplementedError

    @property
    def remaining(self) -> int:
        raise NotImplementedError

    def reset(self) -> None:
        raise NotImplementedError
''',
    "reference": '''class NoPromosLeft(Exception):
    pass


class PromoRotation:
    def __init__(self, codes: list[str]):
        self._codes = list(dict.fromkeys(codes))
        self._used: list[str] = []

    def draw(self) -> str:
        for code in self._codes:
            if code not in self._used:
                self._used.append(code)
                return code
        raise NoPromosLeft("every code has been used")

    def skip(self, code: str) -> None:
        if code not in self._codes:
            raise ValueError(f"unknown code: {code!r}")
        if code not in self._used:
            self._used.append(code)

    @property
    def used(self) -> list[str]:
        return list(self._used)

    @property
    def remaining(self) -> int:
        return len(self._codes) - len(self._used)

    def reset(self) -> None:
        self._used.clear()
''',
    "facts": ["subclass NoPromosLeft Exception", "property PromoRotation used", "property PromoRotation remaining"],
    "java": '''static class Rotation implements Obj {
    List<String> codes = new ArrayList<>(), used = new ArrayList<>();
    public String type() { return "PromoRotation"; }
}
Object step(Map<String,Object> op) {
    String d = s(op.get("do"));
    Object t = target(op);
    if (d.equals("new")) {
        Rotation r = new Rotation();
        for (Object c : arr(arg(op, 0, "codes", MISSING))) if (!r.codes.contains(s(c))) r.codes.add(s(c));
        return r;
    }
    if (t instanceof List && d.equals("call") && s(op.get("method")).equals("append")) { arr(t).add(args(op).get(0)); return null; }
    Rotation r = (Rotation) t;
    if (d.equals("get")) {
        String a = s(op.get("attr"));
        if (a.equals("used")) return new ArrayList<Object>(r.used);
        if (a.equals("remaining")) return (long) (r.codes.size() - r.used.size());
    }
    if (d.equals("call")) {
        String m = s(op.get("method"));
        if (m.equals("draw")) {
            for (String c : r.codes) if (!r.used.contains(c)) { r.used.add(c); return c; }
            throw err("NoPromosLeft");
        }
        if (m.equals("skip")) {
            String c = s(args(op).get(0));
            if (!r.codes.contains(c)) throw err("ValueError");
            if (!r.used.contains(c)) r.used.add(c);
            return null;
        }
        if (m.equals("reset")) { r.used.clear(); return null; }
    }
    throw err("AttributeError");
}
''',
    "approach": """Both lists live on `self`, so each rotation is independent. `dict.fromkeys`
removes duplicates in order and also copies the input. `draw` scans in order and raises the
custom exception at the end. For n codes, `draw` is O(n²) with a list membership test; a set of
used codes next to the ordered list makes it O(n).""",
    "example_notes": [
        "draw returns codes in order. The duplicate A is ignored, so there are only two codes.",
        "After the last code, draw raises the custom NoPromosLeft exception.",
        "Two rotations do not share state. A class-level list would show B1 as used in the second one.",
    ],
    "cases": [
        case("draw in order without duplicates",
             (new("PromoRotation", ["A", "B", "A"], save="r"), obj("PromoRotation")), (call("r", "draw"), "A"),
             (get("r", "remaining"), 1), (get("r", "used"), ["A"])),
        case("exhausted rotation",
             (new("PromoRotation", ["X"], save="r"), obj("PromoRotation")), (call("r", "draw"), "X"),
             (call("r", "draw"), error("NoPromosLeft")), (get("r", "remaining"), 0)),
        case("rotations are independent",
             (new("PromoRotation", ["B1", "B2"], save="a"), obj("PromoRotation")), (call("a", "draw"), "B1"),
             (new("PromoRotation", ["B1", "B2"], save="b"), obj("PromoRotation")), (get("b", "used"), []),
             (call("b", "draw"), "B1")),
        case("skip changes the next draw",
             (new("PromoRotation", ["A", "B", "C"], save="r"), obj("PromoRotation")), (call("r", "skip", "A"), None),
             (call("r", "draw"), "B"), (get("r", "used"), ["A", "B"])),
        case("skip unknown and repeated",
             (new("PromoRotation", ["A", "B"], save="r"), obj("PromoRotation")), (call("r", "skip", "Z"), error("ValueError")),
             (call("r", "skip", "B"), None), (call("r", "skip", "B"), None), (get("r", "used"), ["B"]),
             (get("r", "remaining"), 1)),
        case("skip in the middle keeps order",
             (new("PromoRotation", ["A", "B", "C"], save="r"), obj("PromoRotation")), (call("r", "skip", "B"), None),
             (call("r", "draw"), "A"), (call("r", "draw"), "C"), (call("r", "draw"), error("NoPromosLeft")),
             (get("r", "used"), ["B", "A", "C"])),
        case("reset",
             (new("PromoRotation", ["A", "B"], save="r"), obj("PromoRotation")), (call("r", "draw"), "A"),
             (call("r", "draw"), "B"), (call("r", "reset"), None), (get("r", "remaining"), 2), (call("r", "draw"), "A")),
        case("empty campaign",
             (new("PromoRotation", [], save="r"), obj("PromoRotation")), (get("r", "remaining"), 0),
             (call("r", "draw"), error("NoPromosLeft")), (call("r", "skip", "A"), error("ValueError"))),
        case("used is a copy",
             (new("PromoRotation", ["A", "B"], save="r"), obj("PromoRotation")), (call("r", "draw"), "A"),
             (get("r", "used", save="u"), ["A"]), (call("u", "append", "B"), None), (call("r", "draw"), "B"),
             (get("r", "used"), ["A", "B"])),
        case("many duplicates",
             (new("PromoRotation", ["Q", "Q", "R", "Q", "R", "S"], save="r"), obj("PromoRotation")),
             (get("r", "remaining"), 3), (call("r", "draw"), "Q"), (call("r", "draw"), "R"), (call("r", "draw"), "S")),
        case("codes are case sensitive",
             (new("PromoRotation", ["save10", "SAVE10"], save="r"), obj("PromoRotation")), (get("r", "remaining"), 2),
             (call("r", "skip", "SAVE10"), None), (call("r", "draw"), "save10")),
        case("structure and independent exhaustion",
             (check("subclass", "NoPromosLeft", of="Exception"), True),
             (new("PromoRotation", ["A"], save="a"), obj("PromoRotation")), (new("PromoRotation", ["A"], save="b"), obj("PromoRotation")),
             (call("a", "draw"), "A"), (call("b", "draw"), "A"), (call("a", "draw"), error("NoPromosLeft"))),
    ],
    "generate": lambda rng: (lambda codes: (
        [new("PromoRotation", codes, save="a"), new("PromoRotation", codes[::-1], save="b")]
        + [rng.choice([call(rng.choice("ab"), "draw"), call(rng.choice("ab"), "skip", rng.choice(codes + ["NOPE"])),
                       get(rng.choice("ab"), "used"), get(rng.choice("ab"), "remaining"), call(rng.choice("ab"), "reset")])
           for _ in range(rng.randint(5, 16))]))(
        [rng.choice(["P1", "P2", "P3", "P4", "P5", "P6"]) for _ in range(rng.randint(0, 7))]),
    "mutations": [
        {"name": "shared default list",
         "old": "    def __init__(self, codes: list[str]):\n        self._codes = list(dict.fromkeys(codes))\n        self._used: list[str] = []\n",
         "new": "    def __init__(self, codes: list[str], used=[]):\n        self._codes = list(dict.fromkeys(codes))\n        self._used = used\n"},
        {"name": "duplicates kept", "old": "list(dict.fromkeys(codes))", "new": "list(codes)"},
        {"name": "skip records repeats", "old": "        if code not in self._used:\n            self._used.append(code)\n",
         "new": "        self._used.append(code)\n"},
        {"name": "used returned directly", "old": "return list(self._used)", "new": "return self._used"},
    ],
    "sources": ["https://docs.python.org/3.11/tutorial/classes.html#class-and-instance-variables",
                "https://docs.python.org/3.11/tutorial/errors.html#user-defined-exceptions"],
}
