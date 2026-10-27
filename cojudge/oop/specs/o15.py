"""Original exercise: subclass the dict built-in."""
from cojudge.oop.steps import builtin, call, case, check, error, item, new, op, ref, setitem

SPEC = {
    "number": 15, "slug": "case-insensitive-dict", "title": "Subclass the dict built-in",
    "difficulty": "Medium", "time": 30, "level": 4,
    "prerequisites": "Level 3. Inheritance and `super()`.",
    "learn": """You can inherit from a built-in type: `class Headers(dict):`. The object then **is**
a real dictionary: `isinstance(h, dict)` is `True`, and `json.dumps` accepts it.

There is a trap. The built-in `dict` is written in C, and its methods do **not** call each
other. If you override `__setitem__`, then `dict.__init__`, `dict.update`, `dict.get`, and
`dict.setdefault` still skip your code. You must override every method that you need, or route
them through your own code:

```python
class Headers(dict):
    def __init__(self, mapping=None):
        super().__init__()          # start empty
        if mapping is not None:
            self.update(mapping)    # your update, which uses your __setitem__
```

`collections.UserDict` avoids this trap because its methods call each other. In this exercise
you must use `dict` itself, so you learn where the trap is.""",
    "scenario": """An HTTP library stores response headers. Servers send `Content-Type`,
`content-type`, or `CONTENT-TYPE`, and all three mean the same header. Code that reads a header
must find it with any spelling.""",
    "task": """Write `CaseInsensitiveDict`, a subclass of `dict`. All keys are strings. The
dictionary stores every key in **lowercase** and finds keys with any case.

- `CaseInsensitiveDict(mapping=None)`: start with the items of `mapping`, if given. When two keys
  differ only in case, the later value wins.
- `d[key] = value`, `d[key]`, and `key in d`: work with any case. A missing key raises `KeyError`.
- `get(key, default=None)`: like `dict.get`, with any case.
- `update(mapping)`: add or replace each item of `mapping` (a dictionary). Return `None`.
- `pop(key, default)`: remove the key and return its value. If the key is missing, return
  `default` when it is given; otherwise raise `KeyError`.

The driver shows the dictionary as a JSON object with the stored keys.""",
    "constraints": ["Keys are ASCII strings. Values are JSON values.", "At most 40 steps per test."],
    "hints": ["Override `__init__` so it does not pass `mapping` to `dict.__init__`.",
              "For `pop`, use a private sentinel such as `_MISSING = object()` as the default, so `None` can be a real default."],
    "starter": '''class CaseInsensitiveDict(dict):
    def __init__(self, mapping: dict | None = None):
        raise NotImplementedError

    def __setitem__(self, key: str, value) -> None:
        raise NotImplementedError

    def __getitem__(self, key: str):
        raise NotImplementedError

    def __contains__(self, key: object) -> bool:
        raise NotImplementedError

    def get(self, key: str, default=None):
        raise NotImplementedError

    def update(self, mapping: dict) -> None:
        raise NotImplementedError

    def pop(self, key: str, *default):
        raise NotImplementedError
''',
    "reference": '''_MISSING = object()


class CaseInsensitiveDict(dict):
    def __init__(self, mapping: dict | None = None):
        super().__init__()
        if mapping is not None:
            self.update(mapping)

    def __setitem__(self, key: str, value) -> None:
        super().__setitem__(key.lower(), value)

    def __getitem__(self, key: str):
        return super().__getitem__(key.lower())

    def __contains__(self, key: object) -> bool:
        return super().__contains__(key.lower())

    def get(self, key: str, default=None):
        return super().get(key.lower(), default)

    def update(self, mapping: dict) -> None:
        for key, value in mapping.items():
            self[key] = value

    def pop(self, key: str, default=_MISSING):
        if default is _MISSING:
            return super().pop(key.lower())
        return super().pop(key.lower(), default)
''',
    "facts": ["subclass CaseInsensitiveDict dict", "instance CaseInsensitiveDict dict"],
    "java": '''static class CIDict implements Obj {
    LinkedHashMap<String,Object> data = new LinkedHashMap<>();
    public String type() { return "CaseInsensitiveDict"; }
    public Object plain() { return new LinkedHashMap<String,Object>(data); }
    void update(Object mapping) { for (Map.Entry<String,Object> e : obj(mapping).entrySet()) data.put(e.getKey().toLowerCase(), e.getValue()); }
}
Object step(Map<String,Object> op) {
    String d = s(op.get("do"));
    if (d.equals("new")) { CIDict c = new CIDict(); Object m = arg(op, 0, "mapping", null); if (m != null) c.update(m); return c; }
    if (d.equals("op")) {
        Object r = val(op.get("right"));
        return ((CIDict) r).data.containsKey(s(val(op.get("left"))).toLowerCase());
    }
    CIDict c = (CIDict) target(op);
    if (d.equals("item")) { String k = s(val(op.get("key"))).toLowerCase(); if (!c.data.containsKey(k)) throw err("KeyError"); return c.data.get(k); }
    if (d.equals("setitem")) { c.data.put(s(val(op.get("key"))).toLowerCase(), val(op.get("value"))); return null; }
    if (d.equals("len")) return (long) c.data.size();
    if (d.equals("list")) return new ArrayList<Object>(c.data.keySet());
    if (d.equals("call")) {
        String m = s(op.get("method")); List<Object> a = args(op);
        if (m.equals("get")) { String k = s(a.get(0)).toLowerCase(); return c.data.containsKey(k) ? c.data.get(k) : (a.size() > 1 ? a.get(1) : null); }
        if (m.equals("update")) { c.update(a.get(0)); return null; }
        if (m.equals("pop")) {
            String k = s(a.get(0)).toLowerCase();
            if (c.data.containsKey(k)) return c.data.remove(k);
            if (a.size() > 1) return a.get(1);
            throw err("KeyError");
        }
    }
    throw err("AttributeError");
}
''',
    "approach": """Every write goes through `__setitem__`, which lowercases the key. `__init__` starts
with an empty dictionary and then calls this class's `update`, and `update` assigns one item at a
time. Every read method lowercases its key before it calls the `dict` version. Overriding only
`__setitem__` and `__getitem__` would look correct in simple tests but fail for the constructor,
`update`, `get`, `in`, and `pop`, because `dict` methods do not call each other.""",
    "example_notes": [
        "The constructor stores the keys in lowercase. Lookup works with any case.",
        "get, in, and pop also ignore case. dict.get would not call your __getitem__.",
        "Content-Type and content-type are the same key, so the later value replaces the earlier one.",
    ],
    "cases": [
        case("constructor normalizes keys",
             (new("CaseInsensitiveDict", {"Content-Type": "json", "X-Id": "7"}, save="h"), {"content-type": "json", "x-id": "7"}),
             (item("h", "CONTENT-TYPE"), "json")),
        case("get, in, and pop ignore case",
             (new("CaseInsensitiveDict", {"Host": "a.io"}, save="h"), {"host": "a.io"}), (call("h", "get", "HOST"), "a.io"),
             (op("hOsT", "in", ref("h")), True), (call("h", "pop", "HoSt"), "a.io"), (op("host", "in", ref("h")), False)),
        case("later spelling wins",
             (new("CaseInsensitiveDict", {"Content-Type": "html", "content-type": "json"}, save="h"), {"content-type": "json"}),
             (builtin("len", "h"), 1)),
        case("set and read with different case",
             (new("CaseInsensitiveDict", save="h"), {}), (setitem("h", "Accept", "text"), None), (item("h", "accept"), "text"),
             (setitem("h", "ACCEPT", "json"), None), (item("h", "Accept"), "json"), (builtin("len", "h"), 1)),
        case("missing keys",
             (new("CaseInsensitiveDict", {"A": 1}, save="h"), {"a": 1}), (item("h", "b"), error("KeyError")),
             (call("h", "get", "B"), None), (call("h", "get", "B", 0), 0), (call("h", "pop", "B"), error("KeyError")),
             (call("h", "pop", "B", None), None)),
        case("update ignores case",
             (new("CaseInsensitiveDict", {"Age": 30}, save="h"), {"age": 30}), (call("h", "update", {"AGE": 31, "City": "Lyon"}), None),
             (builtin("list", "h"), ["age", "city"]), (item("h", "age"), 31), (call("h", "get", "CITY"), "Lyon")),
        case("it is a real dict",
             (new("CaseInsensitiveDict", {"K": True}, save="h"), {"k": True}), (check("instance", "h", of="dict"), True),
             (check("subclass", "CaseInsensitiveDict", of="dict"), True)),
        case("empty constructor and None mapping",
             (new("CaseInsensitiveDict", None, save="a"), {}), (new("CaseInsensitiveDict", {}, save="b"), {}),
             (op("x", "in", ref("a")), False), (builtin("len", "b"), 0)),
        case("values of any JSON type",
             (new("CaseInsensitiveDict", {"List": [1, 2], "Null": None, "Obj": {"Inner": 1}}, save="h"),
              {"list": [1, 2], "null": None, "obj": {"Inner": 1}}),
             (item("h", "NULL"), None), (op("null", "in", ref("h")), True), (item("h", "obj"), {"Inner": 1})),
        case("pop with a default for an existing key",
             (new("CaseInsensitiveDict", {"Token": "abc"}, save="h"), {"token": "abc"}), (call("h", "pop", "TOKEN", "none"), "abc"),
             (builtin("len", "h"), 0), (call("h", "get", "token", "gone"), "gone")),
        case("insertion order is kept",
             (new("CaseInsensitiveDict", save="h"), {}), (setitem("h", "B", 1), None), (setitem("h", "A", 2), None),
             (setitem("h", "C", 3), None), (setitem("h", "b", 9), None), (builtin("list", "h"), ["b", "a", "c"]),
             (builtin("len", "h"), 3)),
        case("update after pop",
             (new("CaseInsensitiveDict", {"X": 1, "Y": 2}, save="h"), {"x": 1, "y": 2}), (call("h", "pop", "x"), 1),
             (call("h", "update", {"x": 5}), None), (builtin("list", "h"), ["y", "x"]), (item("h", "X"), 5)),
    ],
    "generate": lambda rng: (lambda keys: (
        [new("CaseInsensitiveDict", {rng.choice(keys): rng.randint(0, 9) for _ in range(rng.randint(0, 3))}, save="h")]
        + [rng.choice([setitem("h", rng.choice(keys), rng.randint(0, 99)), item("h", rng.choice(keys)),
                       call("h", "get", rng.choice(keys)), op(rng.choice(keys), "in", ref("h")),
                       call("h", "pop", rng.choice(keys)), call("h", "pop", rng.choice(keys), -1),
                       call("h", "update", {rng.choice(keys): "u"}), builtin("len", "h"), builtin("list", "h")])
           for _ in range(rng.randint(4, 12))]))(["Id", "ID", "id", "Name", "NAME", "Age", "aGe"]),
    "mutations": [
        {"name": "constructor bypasses lowercase", "old": "        super().__init__()\n        if mapping is not None:\n            self.update(mapping)\n",
         "new": "        super().__init__(mapping or {})\n"},
        {"name": "get not overridden", "old": "        return super().get(key.lower(), default)\n", "new": "        return super().get(key, default)\n"},
        {"name": "update bypasses lowercase", "old": "        for key, value in mapping.items():\n            self[key] = value\n",
         "new": "        super().update(mapping)\n"},
        {"name": "contains is case sensitive", "old": "return super().__contains__(key.lower())", "new": "return super().__contains__(key)"},
    ],
    "sources": ["https://docs.python.org/3.11/library/stdtypes.html#mapping-types-dict",
                "https://docs.python.org/3.11/library/collections.html#collections.UserDict"],
}
