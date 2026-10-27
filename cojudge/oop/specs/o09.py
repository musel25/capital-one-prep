"""Original exercise: a karma user class whose instances interact."""
from cojudge.oop.steps import builtin, call, case, error, get, new, obj, op, ref

SPEC = {
    "number": 9, "slug": "karma-user", "title": "Karma app: objects that interact",
    "difficulty": "Medium", "time": 30, "level": 2,
    "prerequisites": "Exercises 01–08. Properties, `__str__`, and instance state.",
    "learn": """Objects often change **other** objects. In `alice.thank(bob)`, the method runs on
`alice`, but it updates `bob`'s state. Inside a class, a method may read and change the private
attributes of another instance of the same class.

Use `is` to test identity: `other is self` is `True` only for the same object, even when two
users have equal names.

`__lt__(self, other)` defines `<`. When it exists, `sorted(users)` works. To sort by several
keys, give `sorted` a key function that returns a tuple, for example
`key=lambda name: (-points[name], name)` for points high to low, then names A to Z.""",
    "scenario": """A team chat has a "thank you" button. A thank-you gives 1 to 3 karma points to a
colleague. Each profile shows the karma total and the top fans: the people who gave the most
points. Nobody can thank themselves.""",
    "task": """Write the class `KarmaUser`.

- `KarmaUser(name)`: store `name`. A user starts with no karma.
- `thank(other, points=1)`: `other` receives `points` from this user. `points` is an integer
  from 1 to 3; otherwise raise `ValueError`. If `other` is this same object, raise `ValueError`.
  Return `None`.
- `karma`: read-only property. The total points this user received.
- `given`: read-only property. The total points this user gave.
- `fans`: read-only property. The names of everyone who thanked this user, once each. Sort by
  the total points they gave this user, high to low, then by name A to Z.
- `str(user)` returns `"<name>: <karma> karma from <n> fans"`. Use `fan` instead of `fans`
  when `n` is 1.
- `a < b` is `True` when `a` has less karma than `b`.

User names in one test are unique.""",
    "constraints": ["At most 10 users and 60 steps per test."],
    "hints": ["Keep a dictionary on the receiver: giver name → total points.",
              "Validate both arguments before you change any state."],
    "starter": '''class KarmaUser:
    def __init__(self, name: str):
        raise NotImplementedError

    def thank(self, other: "KarmaUser", points: int = 1) -> None:
        raise NotImplementedError

    @property
    def karma(self) -> int:
        raise NotImplementedError

    @property
    def given(self) -> int:
        raise NotImplementedError

    @property
    def fans(self) -> list[str]:
        raise NotImplementedError

    def __str__(self) -> str:
        raise NotImplementedError

    def __lt__(self, other: "KarmaUser") -> bool:
        raise NotImplementedError
''',
    "reference": '''class KarmaUser:
    def __init__(self, name: str):
        self.name = name
        self._received: dict[str, int] = {}
        self._given = 0

    def thank(self, other: "KarmaUser", points: int = 1) -> None:
        if other is self:
            raise ValueError("users cannot thank themselves")
        if isinstance(points, bool) or not isinstance(points, int) or not 1 <= points <= 3:
            raise ValueError("points must be an integer from 1 to 3")
        other._received[self.name] = other._received.get(self.name, 0) + points
        self._given += points

    @property
    def karma(self) -> int:
        return sum(self._received.values())

    @property
    def given(self) -> int:
        return self._given

    @property
    def fans(self) -> list[str]:
        return sorted(self._received, key=lambda name: (-self._received[name], name))

    def __str__(self) -> str:
        count = len(self._received)
        return f"{self.name}: {self.karma} karma from {count} {'fan' if count == 1 else 'fans'}"

    def __lt__(self, other: "KarmaUser") -> bool:
        return self.karma < other.karma
''',
    "facts": ["property KarmaUser karma", "property KarmaUser given", "property KarmaUser fans"],
    "java": '''static class User implements Obj {
    String name; long given; Map<String,Long> received = new LinkedHashMap<>();
    public String type() { return "KarmaUser"; }
    long karma() { long t = 0; for (long v : received.values()) t += v; return t; }
}
Object step(Map<String,Object> op) {
    String d = s(op.get("do"));
    if (d.equals("new")) { User u = new User(); u.name = s(arg(op, 0, "name", MISSING)); return u; }
    if (d.equals("op")) {
        User l = (User) val(op.get("left")), r = (User) val(op.get("right"));
        if (s(op.get("op")).equals("<")) return l.karma() < r.karma();
        if (s(op.get("op")).equals(">")) return l.karma() > r.karma();
        throw err("TypeError");
    }
    User u = (User) target(op);
    if (d.equals("call") && s(op.get("method")).equals("thank")) {
        Object other = arg(op, 0, "other", MISSING), points = arg(op, 1, "points", 1L);
        if (other == u) throw err("ValueError");
        if (!isInt(points) || lng(points) < 1 || lng(points) > 3) throw err("ValueError");
        User o = (User) other;
        o.received.merge(u.name, lng(points), Long::sum); u.given += lng(points);
        return null;
    }
    if (d.equals("get")) {
        String a = s(op.get("attr"));
        if (a.equals("name")) return u.name;
        if (a.equals("karma")) return u.karma();
        if (a.equals("given")) return u.given;
        if (a.equals("fans")) {
            List<String> names = new ArrayList<>(u.received.keySet());
            names.sort((x, y) -> u.received.get(x).equals(u.received.get(y)) ? x.compareTo(y) : Long.compare(u.received.get(y), u.received.get(x)));
            return new ArrayList<Object>(names);
        }
    }
    if (d.equals("str")) { int n = u.received.size(); return u.name + ": " + u.karma() + " karma from " + n + (n == 1 ? " fan" : " fans"); }
    throw err("AttributeError");
}
''',
    "approach": """The receiver keeps a dictionary from giver to total points, so `karma` is a sum
and `fans` is a sort with the key `(-points, name)`. `thank` validates identity and points before
it changes either user, so a rejected thank-you leaves both unchanged. `__lt__` compares karma,
which makes `sorted(users)` order users from least to most karma.""",
    "example_notes": [
        "Bo receives 2 + 1 points from two people. Ann gave 2.",
        "fans sorts by points given, high to low. Cy and Di both gave 3, so the tie is broken by name.",
        "A self-thank and 4 points are rejected. Nothing changes.",
    ],
    "cases": [
        case("thanks change two users",
             (new("KarmaUser", "Ann", save="a"), obj("KarmaUser")), (new("KarmaUser", "Bo", save="b"), obj("KarmaUser")),
             (new("KarmaUser", "Cy", save="c"), obj("KarmaUser")), (call("a", "thank", ref("b"), 2), None),
             (call("c", "thank", ref("b")), None), (get("b", "karma"), 3), (get("a", "given"), 2)),
        case("fans sorted by points then name",
             (new("KarmaUser", "Zed", save="z"), obj("KarmaUser")), (new("KarmaUser", "Di", save="d"), obj("KarmaUser")),
             (new("KarmaUser", "Cy", save="c"), obj("KarmaUser")), (new("KarmaUser", "Al", save="a"), obj("KarmaUser")),
             (call("d", "thank", ref("z"), 3), None), (call("a", "thank", ref("z"), 1), None), (call("c", "thank", ref("z"), 3), None),
             (get("z", "fans"), ["Cy", "Di", "Al"])),
        case("invalid thank-yous change nothing",
             (new("KarmaUser", "Ann", save="a"), obj("KarmaUser")), (new("KarmaUser", "Bo", save="b"), obj("KarmaUser")),
             (call("a", "thank", ref("a")), error("ValueError")), (call("a", "thank", ref("b"), 4), error("ValueError")),
             (get("b", "karma"), 0), (get("a", "given"), 0)),
        case("str with singular and plural",
             (new("KarmaUser", "Ann", save="a"), obj("KarmaUser")), (new("KarmaUser", "Bo", save="b"), obj("KarmaUser")),
             (new("KarmaUser", "Cy", save="c"), obj("KarmaUser")), (builtin("str", "a"), "Ann: 0 karma from 0 fans"),
             (call("b", "thank", ref("a"), 3), None), (builtin("str", "a"), "Ann: 3 karma from 1 fan"),
             (call("c", "thank", ref("a")), None), (builtin("str", "a"), "Ann: 4 karma from 2 fans")),
        case("repeated thanks add up for one fan",
             (new("KarmaUser", "Ann", save="a"), obj("KarmaUser")), (new("KarmaUser", "Bo", save="b"), obj("KarmaUser")),
             (call("a", "thank", ref("b"), 1), None), (call("a", "thank", ref("b"), 3), None), (get("b", "fans"), ["Ann"]),
             (builtin("str", "b"), "Bo: 4 karma from 1 fan"), (get("a", "karma"), 0)),
        case("points bounds and types",
             (new("KarmaUser", "Ann", save="a"), obj("KarmaUser")), (new("KarmaUser", "Bo", save="b"), obj("KarmaUser")),
             (call("a", "thank", ref("b"), 0), error("ValueError")), (call("a", "thank", ref("b"), True), error("ValueError")),
             (call("a", "thank", ref("b"), 1.5), error("ValueError")), (call("a", "thank", ref("b"), points=3), None),
             (get("b", "karma"), 3)),
        case("same name is not the same object",
             (new("KarmaUser", "Sam", save="a"), obj("KarmaUser")), (new("KarmaUser", "Sam", save="b"), obj("KarmaUser")),
             (call("a", "thank", ref("b")), None), (get("b", "karma"), 1)),
        case("compare users by karma",
             (new("KarmaUser", "Ann", save="a"), obj("KarmaUser")), (new("KarmaUser", "Bo", save="b"), obj("KarmaUser")),
             (op(ref("a"), "<", ref("b")), False), (call("a", "thank", ref("b"), 2), None),
             (op(ref("a"), "<", ref("b")), True), (op(ref("b"), "<", ref("a")), False)),
        case("mutual thanks",
             (new("KarmaUser", "Ann", save="a"), obj("KarmaUser")), (new("KarmaUser", "Bo", save="b"), obj("KarmaUser")),
             (call("a", "thank", ref("b"), 2), None), (call("b", "thank", ref("a"), 3), None),
             (get("a", "karma"), 3), (get("a", "given"), 2), (get("b", "karma"), 2), (get("b", "given"), 3)),
        case("fan order changes with more points",
             (new("KarmaUser", "T", save="t"), obj("KarmaUser")), (new("KarmaUser", "Bea", save="b"), obj("KarmaUser")),
             (new("KarmaUser", "Abe", save="a"), obj("KarmaUser")), (call("b", "thank", ref("t"), 2), None),
             (call("a", "thank", ref("t"), 1), None), (get("t", "fans"), ["Bea", "Abe"]),
             (call("a", "thank", ref("t"), 2), None), (get("t", "fans"), ["Abe", "Bea"])),
        case("read-only karma",
             (new("KarmaUser", "Ann", save="a"), obj("KarmaUser")), ({"do": "set", "obj": "a", "attr": "karma", "value": 100}, error("AttributeError")),
             (get("a", "karma"), 0), (get("a", "fans"), [])),
        case("keyword target",
             (new("KarmaUser", name="Ann", save="a"), obj("KarmaUser")), (new("KarmaUser", "Bo", save="b"), obj("KarmaUser")),
             (call("a", "thank", other=ref("b"), points=2), None), (get("b", "fans"), ["Ann"]), (get("b", "karma"), 2)),
    ],
    "generate": lambda rng: (lambda names: (
        [new("KarmaUser", n, save=n) for n in names]
        + [rng.choice([call(rng.choice(names), "thank", {"ref": rng.choice(names)}, rng.choice([1, 2, 3, 3, 0, 4])),
                       get(rng.choice(names), "fans"), get(rng.choice(names), "karma"), builtin("str", rng.choice(names)),
                       get(rng.choice(names), "given"), op({"ref": rng.choice(names)}, "<", {"ref": rng.choice(names)})])
           for _ in range(rng.randint(6, 18))]))(rng.sample(["Ann", "Bo", "Cy", "Di", "Ed"], rng.randint(2, 5))),
    "mutations": [
        {"name": "self-thanks allowed", "old": "        if other is self:\n            raise ValueError(\"users cannot thank themselves\")\n", "new": ""},
        {"name": "fan ties not sorted by name", "old": "key=lambda name: (-self._received[name], name)",
         "new": "key=lambda name: -self._received[name]"},
        {"name": "always plural", "old": "'fan' if count == 1 else 'fans'", "new": "'fans'"},
        {"name": "points recorded on the giver", "old": "other._received[self.name] = other._received.get(self.name, 0) + points",
         "new": "self._received[other.name] = self._received.get(other.name, 0) + points"},
    ],
    "sources": ["https://docs.python.org/3.11/reference/expressions.html#is-not",
                "https://docs.python.org/3.11/howto/sorting.html#key-functions"],
}
