"""Original exercise: a ranking class with stable tie-breaking."""
from cojudge.oop.steps import builtin, call, case, error, new, obj, op, ref

SPEC = {
    "number": 21, "slug": "ninja-leaderboard", "title": "Ninja rankings: a leaderboard class",
    "difficulty": "Medium", "time": 35, "level": 5,
    "prerequisites": "Levels 1–4. Dunder methods `__len__`, `__contains__`, and `__str__`.",
    "learn": """A leaderboard must be **fair** when scores are equal. A common rule: the player who
reached the score first ranks higher. To apply it, store a sequence number with each best score
and sort by `(-score, sequence)`.

```python
order = sorted(best, key=lambda name: (-best[name][0], best[name][1]))
```

Python's sort is **stable**, but stability alone is not enough here, because a dictionary keeps
the order in which a key was **first** inserted, not when its best score changed. The explicit
sequence number makes the rule independent of storage order.

`__len__` makes `len(board)` work, and `__contains__` makes `"Kai" in board` work. For a large
board, the `bisect` module keeps a list sorted while you insert; here a sort per query is fast
enough.""",
    "scenario": """A dojo app runs weekly training challenges. Each ninja can submit many times; only
their best score counts. The home screen shows the top of the board, and every ninja can look
up their own rank.""",
    "task": """Write the class `Leaderboard`.

- `Leaderboard(size)`: `size` is the number of places shown by `top` and `str`. Below 1 raises
  `ValueError`.
- `submit(name, score)`: `score` is an integer. If `name` is new, or `score` is **higher** than
  their best, store it as their best and return `True`. Otherwise return `False` and change
  nothing.
- **Ranking order:** best score, high to low. For equal best scores, the ninja who **reached** that
  best score earlier ranks higher.
- `rank(name)`: the 1-based position among **all** ninjas. Unknown name: `KeyError`.
- `top(n=None)`: a list of `(name, score)` pairs for the first `n` places, but never more than
  `size`. With no `n`, use `size`. The driver shows pairs as lists.
- `len(board)`: the number of ninjas. `name in board`: `True` if the ninja submitted.
- `str(board)`: one line per place in `top()`, joined with `"\\n"`, each `"<place>. <name>
  <score>"`. An empty board is `""`.""",
    "constraints": ["Scores are from -1,000 to 1,000,000.", "At most 60 steps per test."],
    "hints": ["Store `name → (best_score, sequence)` and increase the sequence on every accepted submission.",
              "A submission equal to the best is not an improvement: it must not move the ninja down."],
    "starter": '''class Leaderboard:
    def __init__(self, size: int):
        raise NotImplementedError

    def submit(self, name: str, score: int) -> bool:
        raise NotImplementedError

    def rank(self, name: str) -> int:
        raise NotImplementedError

    def top(self, n: int | None = None) -> list[tuple[str, int]]:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

    def __contains__(self, name: object) -> bool:
        raise NotImplementedError

    def __str__(self) -> str:
        raise NotImplementedError
''',
    "reference": '''class Leaderboard:
    def __init__(self, size: int):
        if size < 1:
            raise ValueError("size must be at least 1")
        self.size = size
        self._best: dict[str, tuple[int, int]] = {}
        self._sequence = 0

    def submit(self, name: str, score: int) -> bool:
        current = self._best.get(name)
        if current is not None and score <= current[0]:
            return False
        self._sequence += 1
        self._best[name] = (score, self._sequence)
        return True

    def _ordered(self) -> list[str]:
        return sorted(self._best, key=lambda name: (-self._best[name][0], self._best[name][1]))

    def rank(self, name: str) -> int:
        if name not in self._best:
            raise KeyError(name)
        return self._ordered().index(name) + 1

    def top(self, n: int | None = None) -> list[tuple[str, int]]:
        limit = self.size if n is None else min(n, self.size)
        return [(name, self._best[name][0]) for name in self._ordered()[:limit]]

    def __len__(self) -> int:
        return len(self._best)

    def __contains__(self, name: object) -> bool:
        return name in self._best

    def __str__(self) -> str:
        return "\\n".join(f"{place}. {name} {score}" for place, (name, score) in enumerate(self.top(), start=1))
''',
    "facts": [],
    "java": '''static class Board implements Obj {
    long size, seq; LinkedHashMap<String,long[]> best = new LinkedHashMap<>();
    public String type() { return "Leaderboard"; }
    List<String> ordered() {
        List<String> names = new ArrayList<>(best.keySet());
        names.sort((a, b) -> best.get(a)[0] != best.get(b)[0] ? Long.compare(best.get(b)[0], best.get(a)[0]) : Long.compare(best.get(a)[1], best.get(b)[1]));
        return names;
    }
    List<Object> top(long n) {
        List<Object> out = new ArrayList<>(); List<String> o = ordered();
        for (int i = 0; i < Math.min(Math.min(n, size), o.size()); i++) out.add(list(o.get(i), best.get(o.get(i))[0]));
        return out;
    }
}
Object step(Map<String,Object> op) {
    String d = s(op.get("do"));
    if (d.equals("new")) { Board b = new Board(); b.size = lng(arg(op, 0, "size", MISSING)); if (b.size < 1) throw err("ValueError"); return b; }
    if (d.equals("op")) return ((Board) val(op.get("right"))).best.containsKey(val(op.get("left")));
    Board b = (Board) target(op);
    if (d.equals("len")) return (long) b.best.size();
    if (d.equals("str")) {
        List<String> lines = new ArrayList<>(); int place = 1;
        for (Object pair : b.top(b.size)) lines.add((place++) + ". " + arr(pair).get(0) + " " + arr(pair).get(1));
        return String.join("\\n", lines);
    }
    if (d.equals("call")) {
        String m = s(op.get("method")); List<Object> a = args(op);
        if (m.equals("submit")) {
            String name = s(a.get(0)); long score = lng(a.get(1));
            if (b.best.containsKey(name) && score <= b.best.get(name)[0]) return false;
            b.best.put(name, new long[]{score, ++b.seq}); return true;
        }
        if (m.equals("rank")) { String name = s(a.get(0)); if (!b.best.containsKey(name)) throw err("KeyError"); return (long) b.ordered().indexOf(name) + 1; }
        if (m.equals("top")) return b.top(a.isEmpty() || a.get(0) == null ? b.size : lng(a.get(0)));
    }
    throw err("AttributeError");
}
''',
    "approach": """Each ninja maps to `(best, sequence)`. An accepted submission takes the next
sequence number, so "reached earlier" is a plain integer comparison, and an equal resubmission is
rejected before it can change that number. Every query sorts by `(-best, sequence)`: O(n log n)
per query and O(1) per submission. A heavy-traffic board would keep the order incrementally with
`bisect` or a balanced tree.""",
    "example_notes": [
        "Only the best score counts. Kai's 70 is lower than 90, so submit returns False.",
        "Ana and Bo both have 50. Ana reached 50 first, so she ranks higher.",
        "top never shows more than size places. rank counts every ninja.",
    ],
    "cases": [
        case("best score counts",
             (new("Leaderboard", 3, save="b"), obj("Leaderboard")), (call("b", "submit", "Kai", 90), True),
             (call("b", "submit", "Kai", 70), False), (call("b", "top"), [["Kai", 90]])),
        case("ties go to the earlier ninja",
             (new("Leaderboard", 3, save="b"), obj("Leaderboard")), (call("b", "submit", "Bo", 40), True),
             (call("b", "submit", "Ana", 50), True), (call("b", "submit", "Bo", 50), True),
             (call("b", "top"), [["Ana", 50], ["Bo", 50]]), (call("b", "rank", "Bo"), 2)),
        case("size limits top",
             (new("Leaderboard", 2, save="b"), obj("Leaderboard")), (call("b", "submit", "A", 1), True),
             (call("b", "submit", "B", 2), True), (call("b", "submit", "C", 3), True),
             (call("b", "top", 5), [["C", 3], ["B", 2]]), (call("b", "rank", "A"), 3)),
        case("equal resubmission does not move",
             (new("Leaderboard", 5, save="b"), obj("Leaderboard")), (call("b", "submit", "X", 10), True),
             (call("b", "submit", "Y", 10), True), (call("b", "submit", "X", 10), False), (call("b", "rank", "X"), 1)),
        case("str",
             (new("Leaderboard", 2, save="b"), obj("Leaderboard")), (builtin("str", "b"), ""), (call("b", "submit", "Kai", 7), True),
             (call("b", "submit", "Mei", 9), True), (call("b", "submit", "Ren", 8), True), (builtin("str", "b"), "1. Mei 9\n2. Ren 8")),
        case("len and in",
             (new("Leaderboard", 1, save="b"), obj("Leaderboard")), (builtin("len", "b"), 0), (call("b", "submit", "A", 5), True),
             (call("b", "submit", "A", 6), True), (call("b", "submit", "B", 1), True), (builtin("len", "b"), 2),
             (op("B", "in", ref("b")), True), (op("Z", "in", ref("b")), False)),
        case("invalid size and unknown rank",
             (new("Leaderboard", 0), error("ValueError")), (new("Leaderboard", 1, save="b"), obj("Leaderboard")),
             (call("b", "rank", "ghost"), error("KeyError"))),
        case("negative and zero scores",
             (new("Leaderboard", 3, save="b"), obj("Leaderboard")), (call("b", "submit", "A", -5), True),
             (call("b", "submit", "B", 0), True), (call("b", "submit", "A", -1), True), (call("b", "top"), [["B", 0], ["A", -1]])),
        case("improvement moves up past a tie",
             (new("Leaderboard", 3, save="b"), obj("Leaderboard")), (call("b", "submit", "A", 20), True),
             (call("b", "submit", "B", 30), True), (call("b", "submit", "C", 30), True), (call("b", "submit", "A", 30), True),
             (call("b", "top"), [["B", 30], ["C", 30], ["A", 30]]), (call("b", "submit", "C", 31), True), (call("b", "rank", "C"), 1)),
        case("top with small n",
             (new("Leaderboard", 3, save="b"), obj("Leaderboard")), (call("b", "submit", "A", 1), True),
             (call("b", "submit", "B", 2), True), (call("b", "top", 1), [["B", 2]]), (call("b", "top", 0), [])),
        case("empty board",
             (new("Leaderboard", 4, save="b"), obj("Leaderboard")), (call("b", "top"), []), (builtin("len", "b"), 0)),
        case("str respects size",
             (new("Leaderboard", 1, save="b"), obj("Leaderboard")), (call("b", "submit", "Lin", 3), True),
             (call("b", "submit", "Kim", 4), True), (builtin("str", "b"), "1. Kim 4"), (call("b", "rank", "Lin"), 2)),
    ],
    "generate": lambda rng: (lambda names: (
        [new("Leaderboard", rng.randint(1, 4), save="b")]
        + [rng.choice([call("b", "submit", rng.choice(names), rng.choice([0, 10, 10, 20, 30, rng.randint(-5, 40)])),
                       call("b", "submit", rng.choice(names), rng.choice([10, 20])), call("b", "rank", rng.choice(names)),
                       call("b", "top"), call("b", "top", rng.randint(0, 5)), builtin("str", "b"), builtin("len", "b")])
           for _ in range(rng.randint(6, 20))]))(["Kai", "Mei", "Ren", "Aya", "Jin"]),
    "mutations": [
        {"name": "equal score accepted", "old": "score <= current[0]", "new": "score < current[0]"},
        {"name": "ties by name", "old": "key=lambda name: (-self._best[name][0], self._best[name][1])",
         "new": "key=lambda name: (-self._best[name][0], name)"},
        {"name": "top ignores size", "old": "limit = self.size if n is None else min(n, self.size)",
         "new": "limit = self.size if n is None else n"},
        {"name": "lower score replaces best", "old": "if current is not None and score <= current[0]:", "new": "if current is not None and score == current[0]:"},
    ],
    "sources": ["https://docs.python.org/3.11/howto/sorting.html", "https://docs.python.org/3.11/library/bisect.html"],
}
