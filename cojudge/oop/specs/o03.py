"""Original exercise: a property setter that enforces rules and keeps history."""
from cojudge.oop.steps import call, case, check, error, get, new, obj, put

SPEC = {
    "number": 3, "slug": "score-property", "title": "Write a score property with rules",
    "difficulty": "Easy", "time": 20, "level": 1,
    "prerequisites": "Exercises 01–02. Properties and setters.",
    "learn": """A setter is the single gate for a value. It can check the **type** and the
**range** of the new value and raise the right exception:

- `TypeError` when the value has the wrong type, for example a string instead of an integer.
- `ValueError` when the type is right but the value is not allowed, for example `-5`.

In Python, `True` and `False` are instances of `int`. Exclude them with an explicit check:
`isinstance(value, bool) or not isinstance(value, int)`.

When a property returns a list that the object owns, return a **copy** (`list(self._items)`).
Otherwise the caller can change the object's internal state without going through your rules.""",
    "scenario": """A quiz app shows each player's current score, their best score, and a score history
chart. The score comes from a network message, so it can have the wrong type. The history
chart must show exactly the scores that the app accepted.""",
    "task": """Write the class `Player`.

- `Player(name)`: store `name`. The score starts at `0`.
- `score`: property with a setter. A new score must be an `int` that is not a `bool`; otherwise
  raise `TypeError`. A negative score raises `ValueError`. A rejected value changes nothing.
- `best`: read-only property. The highest score that was ever accepted (`0` at the start).
- `history`: read-only property. A **new list** of every accepted score in order, starting with
  the initial `0`. A change to the returned list must not change the player.
- `reset()`: set the score to `0` through the same rules. It is recorded in the history. `best`
  does not change. Return `None`.

The same score can be accepted twice; record it each time.""",
    "constraints": ["Scores in the tests are from -100 to 10,000, or a wrong type.",
                    "At most 40 steps per test."],
    "hints": ["Check the type before you compare the value with 0.",
              "`return list(self._history)` returns a copy."],
    "starter": '''class Player:
    def __init__(self, name: str):
        raise NotImplementedError

    @property
    def score(self) -> int:
        raise NotImplementedError

    @score.setter
    def score(self, value: int) -> None:
        raise NotImplementedError

    @property
    def best(self) -> int:
        raise NotImplementedError

    @property
    def history(self) -> list[int]:
        raise NotImplementedError

    def reset(self) -> None:
        raise NotImplementedError
''',
    "reference": '''class Player:
    def __init__(self, name: str):
        self.name = name
        self._score = 0
        self._best = 0
        self._history = [0]

    @property
    def score(self) -> int:
        return self._score

    @score.setter
    def score(self, value: int) -> None:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("score must be an integer")
        if value < 0:
            raise ValueError("score must not be negative")
        self._score = value
        self._best = max(self._best, value)
        self._history.append(value)

    @property
    def best(self) -> int:
        return self._best

    @property
    def history(self) -> list[int]:
        return list(self._history)

    def reset(self) -> None:
        self.score = 0
''',
    "facts": ["property Player score", "property Player best", "property Player history"],
    "java": '''static class Player implements Obj {
    String name; long score = 0, best = 0; List<Object> history = new ArrayList<>(List.of(0L));
    public String type() { return "Player"; }
    void setScore(Object v) {
        if (!isInt(v)) throw err("TypeError");
        long x = lng(v);
        if (x < 0) throw err("ValueError");
        score = x; best = Math.max(best, x); history.add(x);
    }
}
Object step(Map<String,Object> op) {
    String d = s(op.get("do"));
    if (d.equals("new")) { Player p = new Player(); p.name = s(arg(op, 0, "name", MISSING)); return p; }
    Object t = target(op);
    if (t instanceof List && d.equals("call") && s(op.get("method")).equals("append")) { arr(t).add(args(op).get(0)); return null; }
    if (t instanceof List && d.equals("len")) return (long) arr(t).size();
    Player p = (Player) t;
    String a = op.containsKey("attr") ? s(op.get("attr")) : "";
    if (d.equals("get")) {
        if (a.equals("name")) return p.name;
        if (a.equals("score")) return p.score;
        if (a.equals("best")) return p.best;
        if (a.equals("history")) return new ArrayList<>(p.history);
        throw err("AttributeError");
    }
    if (d.equals("set")) {
        if (a.equals("best") || a.equals("history")) throw err("AttributeError");
        if (a.equals("score")) p.setScore(val(op.get("value")));
        if (a.equals("name")) p.name = s(val(op.get("value")));
        return null;
    }
    if (d.equals("call") && s(op.get("method")).equals("reset")) { p.setScore(0L); return null; }
    throw err("AttributeError");
}
''',
    "approach": """The setter checks the type, then the range, and only then changes three fields.
`reset` goes through the setter, so it is recorded like any other accepted score. `history`
returns a copy, so the caller cannot bypass the rules. Each operation is O(1) except `history`,
which is O(n) for the copy.""",
    "example_notes": [
        "Two accepted scores. best keeps 50 after the score drops to 20. history starts with the initial 0.",
        "A string raises TypeError, a negative number raises ValueError. Neither is recorded.",
        "The test appends 999 to the returned list. The player's history must not change.",
    ],
    "cases": [
        case("accepted scores and best",
             (new("Player", "Ana", save="p"), obj("Player")), (put("p", "score", 50), None),
             (put("p", "score", 20), None), (get("p", "best"), 50), (get("p", "history"), [0, 50, 20])),
        case("wrong type and negative value",
             (new("Player", "Ana", save="p"), obj("Player")), (put("p", "score", "10"), error("TypeError")),
             (put("p", "score", -1), error("ValueError")), (get("p", "score"), 0), (get("p", "history"), [0])),
        case("history is a copy",
             (new("Player", "Ana", save="p"), obj("Player")), (put("p", "score", 5), None),
             (get("p", "history", save="h"), [0, 5]), (call("h", "append", 999), None),
             (get("p", "history"), [0, 5])),
        case("booleans are rejected",
             (new("Player", "Ben", save="p"), obj("Player")), (put("p", "score", True), error("TypeError")),
             (put("p", "score", False), error("TypeError")), (get("p", "history"), [0])),
        case("floats and null are rejected",
             (new("Player", "Ben", save="p"), obj("Player")), (put("p", "score", 2.5), error("TypeError")),
             (put("p", "score", None), error("TypeError")), (put("p", "score", [1]), error("TypeError")),
             (get("p", "score"), 0)),
        case("reset is recorded and keeps best",
             (new("Player", "Cy", save="p"), obj("Player")), (put("p", "score", 300), None),
             (call("p", "reset"), None), (get("p", "score"), 0), (get("p", "best"), 300),
             (get("p", "history"), [0, 300, 0])),
        case("zero and repeats are recorded",
             (new("Player", "Di", save="p"), obj("Player")), (put("p", "score", 0), None),
             (put("p", "score", 7), None), (put("p", "score", 7), None), (get("p", "history"), [0, 0, 7, 7])),
        case("best rises only",
             (new("Player", "Ed", save="p"), obj("Player")), (put("p", "score", 10), None),
             (put("p", "score", 40), None), (put("p", "score", 30), None), (get("p", "best"), 40),
             (put("p", "score", 10000), None), (get("p", "best"), 10000)),
        case("read-only properties",
             (new("Player", "Fay", save="p"), obj("Player")), (put("p", "best", 99), error("AttributeError")),
             (put("p", "history", []), error("AttributeError")), (get("p", "best"), 0)),
        case("rejections between valid scores",
             (new("Player", "Gus", save="p"), obj("Player")), (put("p", "score", 3), None),
             (put("p", "score", -3), error("ValueError")), (put("p", "score", "x"), error("TypeError")),
             (put("p", "score", 4), None), (get("p", "history"), [0, 3, 4]), (get("p", "score"), 4)),
        case("two players are independent",
             (new("Player", "A", save="a"), obj("Player")), (new("Player", "B", save="b"), obj("Player")),
             (put("a", "score", 8), None), (get("b", "history"), [0]), (get("b", "best"), 0)),
        case("structure",
             (check("property", "Player", "score"), True), (check("property", "Player", "best"), True),
             (check("property", "Player", "history"), True), (new("Player", name="Hal", save="p"), obj("Player")),
             (get("p", "name"), "Hal")),
    ],
    "generate": lambda rng: (
        [new("Player", "P", save="p")]
        + [rng.choice([put("p", "score", rng.choice([rng.randint(0, 500), -rng.randint(1, 9), "7", True, 1.5, 0])),
                       get("p", "best"), get("p", "history"), get("p", "score"), call("p", "reset")])
           for _ in range(rng.randint(4, 14))]),
    "mutations": [
        {"name": "booleans accepted", "old": "isinstance(value, bool) or ", "new": ""},
        {"name": "history returned directly", "old": "return list(self._history)", "new": "return self._history"},
        {"name": "best follows the latest score", "old": "max(self._best, value)", "new": "value"},
        {"name": "reset bypasses the setter", "old": "        self.score = 0\n", "new": "        self._score = 0\n"},
    ],
    "sources": ["https://docs.python.org/3.11/library/functions.html#property",
                "https://docs.python.org/3.11/library/functions.html#isinstance"],
}
