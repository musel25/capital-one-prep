"""Original exercise: cooperative multiple inheritance and the MRO."""
from cojudge.oop.steps import call, case, check, get, new, obj, put

SPEC = {
    "number": 12, "slug": "mro-formatters", "title": "Multiple inheritance and the MRO",
    "difficulty": "Hard", "time": 35, "level": 3,
    "prerequisites": "Exercises 10–11. `super()` and class attributes.",
    "learn": """A class can have several base classes: `class Alert(Shout, Tag, Trim)`. Python puts
all classes in one line, the **method resolution order** (MRO). See it with `Alert.__mro__`.
The MRO keeps each class before its bases, and keeps the order that you list the bases in.

`super()` does **not** mean "my base class". It means "the next class in the MRO of the
object's type". So in an `Alert` object, `super()` inside `Shout` calls `Tag`, although `Shout`
does not inherit from `Tag`. When every class calls `super()`, all of them run in MRO order. This
is **cooperative** multiple inheritance:

```python
class Base:
    def name(self): return "base"
class A(Base):
    def name(self): return "a>" + super().name()
class B(Base):
    def name(self): return "b>" + super().name()
class C(A, B): pass
C().name()   # "a>b>base"  (MRO: C, A, B, Base, object)
```

A class that does not call `super()` stops the chain: the classes after it never run.""",
    "scenario": """A monitoring system formats messages before it sends them. Small formatter
classes each do one thing: trim spaces, add a tag, or shout. Message types combine them with
multiple inheritance, so every new combination is one short class definition.""",
    "task": """The starter gives the base class `Formatter`, where `format(text)` returns `text`.
Do not change it. Write these classes. Every `format` method must call `super().format(...)`
exactly once:

- `Trim(Formatter)`: pass `text.strip()` to the next `format` and return its result.
- `Shout(Formatter)`: take the result of the next `format(text)`, convert it to uppercase, and
  add `"!"`.
- `Tag(Formatter)`: class attribute `tag = "info"`. Return `"[<tag>] "` followed by the result of
  the next `format(text)`. Read the tag from `self.tag`.
- `Alert(Shout, Tag, Trim)`: class attribute `tag = "alert"`. No `format` method of its own.
- `Note(Tag, Trim)`: no new attributes or methods.

Example: `Alert().format("  disk full ")` runs `Shout`, `Tag`, `Trim`, then `Formatter`, and
returns `"[ALERT] DISK FULL!"`.""",
    "constraints": ["Texts are ASCII.", "At most 30 steps per test."],
    "hints": ["Write the class headers with the bases in exactly the order given; the order decides the MRO.",
              "`Shout` changes the text after `super().format(text)` returns; `Trim` changes it before."],
    "starter": '''class Formatter:
    def format(self, text: str) -> str:
        return text


class Trim(Formatter):
    def format(self, text: str) -> str:
        raise NotImplementedError


class Shout(Formatter):
    def format(self, text: str) -> str:
        raise NotImplementedError


class Tag(Formatter):
    def format(self, text: str) -> str:
        raise NotImplementedError


# Write Alert and Note here.
''',
    "reference": '''class Formatter:
    def format(self, text: str) -> str:
        return text


class Trim(Formatter):
    def format(self, text: str) -> str:
        return super().format(text.strip())


class Shout(Formatter):
    def format(self, text: str) -> str:
        return super().format(text).upper() + "!"


class Tag(Formatter):
    tag = "info"

    def format(self, text: str) -> str:
        return f"[{self.tag}] " + super().format(text)


class Alert(Shout, Tag, Trim):
    tag = "alert"


class Note(Tag, Trim):
    pass
''',
    "facts": ["mro Alert Alert,Shout,Tag,Trim,Formatter,object", "mro Note Note,Tag,Trim,Formatter,object",
              "mro Trim Trim,Formatter,object", "subclass Alert Tag", "subclass Alert Trim", "subclass Note Trim"],
    "java": '''static final Map<String,String[]> MRO = Map.of(
    "Formatter", new String[]{"Formatter"}, "Trim", new String[]{"Trim", "Formatter"},
    "Shout", new String[]{"Shout", "Formatter"}, "Tag", new String[]{"Tag", "Formatter"},
    "Alert", new String[]{"Alert", "Shout", "Tag", "Trim", "Formatter"},
    "Note", new String[]{"Note", "Tag", "Trim", "Formatter"});
static class F implements Obj {
    String kind, tag;
    public String type() { return kind; }
    F(String kind) { this.kind = kind; this.tag = kind.equals("Alert") ? "alert" : "info"; }
    String format(int i, String text) {
        switch (MRO.get(kind)[i]) {
            case "Trim": return format(i + 1, text.strip());
            case "Shout": return format(i + 1, text).toUpperCase() + "!";
            case "Tag": return "[" + tag + "] " + format(i + 1, text);
            case "Formatter": return text;
            default: return format(i + 1, text);
        }
    }
}
Object step(Map<String,Object> op) {
    String d = s(op.get("do"));
    Object t = target(op);
    if (d.equals("new")) return new F((String) t);
    if (t instanceof String && d.equals("get") && s(op.get("attr")).equals("tag")) {
        if (t.equals("Alert")) return "alert";
        if (t.equals("Tag") || t.equals("Note")) return "info";
    }
    F f = (F) t;
    if (d.equals("call") && s(op.get("method")).equals("format")) return f.format(0, s(args(op).get(0)));
    if (d.equals("set") && s(op.get("attr")).equals("tag")) { f.tag = s(val(op.get("value"))); return null; }
    if (d.equals("get") && s(op.get("attr")).equals("tag") && Arrays.asList(MRO.get(f.kind)).contains("Tag")) return f.tag;
    throw err("AttributeError");
}
''',
    "approach": """Each mixin does one step and calls `super().format`, so the classes form one
chain in MRO order. For `Alert` the MRO is Alert, Shout, Tag, Trim, Formatter: `Shout` waits for
the rest of the chain and then uppercases everything, including the tag. `Trim` strips before it
passes the text on. `Tag` reads `self.tag`, which finds `Alert.tag` first. If one class returned
a value without `super()`, every class after it in the MRO would be skipped.""",
    "example_notes": [
        "MRO Alert → Shout → Tag → Trim → Formatter. Trim strips, Tag adds [alert], Shout uppercases all of it.",
        "Note has the MRO Note → Tag → Trim → Formatter. It inherits tag = \"info\" from Tag.",
        "The MRO of Alert, as class names. The order of the bases in the class header decides it.",
    ],
    "cases": [
        case("alert chain",
             (new("Alert", save="a"), obj("Alert")), (call("a", "format", "  disk full "), "[ALERT] DISK FULL!")),
        case("note chain",
             (new("Note", save="n"), obj("Note")), (call("n", "format", " backup done  "), "[info] backup done")),
        case("alert mro",
             (check("mro", "Alert"), ["Alert", "Shout", "Tag", "Trim", "Formatter", "object"])),
        case("single formatters",
             (new("Trim", save="t"), obj("Trim")), (call("t", "format", "  hi "), "hi"),
             (new("Shout", save="s"), obj("Shout")), (call("s", "format", " hi "), " HI !"),
             (new("Tag", save="g"), obj("Tag")), (call("g", "format", "hi"), "[info] hi")),
        case("note mro and tag",
             (check("mro", "Note"), ["Note", "Tag", "Trim", "Formatter", "object"]), (get("Note", "tag"), "info"),
             (get("Alert", "tag"), "alert")),
        case("instance tag overrides the class",
             (new("Alert", save="a"), obj("Alert")), (put("a", "tag", "db"), None), (call("a", "format", "slow"), "[DB] SLOW!"),
             (new("Alert", save="b"), obj("Alert")), (call("b", "format", "slow"), "[ALERT] SLOW!")),
        case("empty and space-only text",
             (new("Alert", save="a"), obj("Alert")), (call("a", "format", ""), "[ALERT] !"),
             (new("Note", save="n"), obj("Note")), (call("n", "format", "   "), "[info] ")),
        case("inner spaces are kept",
             (new("Note", save="n"), obj("Note")), (call("n", "format", "  a  b  "), "[info] a  b"),
             (new("Alert", save="a"), obj("Alert")), (call("a", "format", "\tx y\n"), "[ALERT] X Y!")),
        case("base formatter",
             (new("Formatter", save="f"), obj("Formatter")), (call("f", "format", "  As Is  "), "  As Is  ")),
        case("subclass relations",
             (check("subclass", "Alert", of="Tag"), True), (check("subclass", "Alert", of="Trim"), True),
             (check("subclass", "Note", of="Shout"), False), (check("subclass", "Trim", of="Tag"), False)),
        case("case of the input",
             (new("Alert", save="a"), obj("Alert")), (call("a", "format", "Mixed Case 42"), "[ALERT] MIXED CASE 42!"),
             (new("Note", save="n"), obj("Note")), (call("n", "format", "Mixed Case"), "[info] Mixed Case")),
        case("note tag change and trim mro",
             (new("Note", save="n"), obj("Note")), (put("n", "tag", "ops"), None), (call("n", "format", " ok "), "[ops] ok"),
             (check("mro", "Trim"), ["Trim", "Formatter", "object"])),
    ],
    "generate": lambda rng: (
        [new(rng.choice(["Alert", "Note", "Trim", "Shout", "Tag"]), save="f")]
        + ([put("f", "tag", rng.choice(["x", "warn", "Db"]))] if rng.random() < 0.2 else [])
        + [call("f", "format", rng.choice(["", " ", "a", " Disk ", "low  memory ", "  CPU 99% ", "ok\n", "\tTabbed"]))
           for _ in range(rng.randint(1, 4))]),
    "mutations": [
        {"name": "shout skips the chain", "old": 'return super().format(text).upper() + "!"', "new": 'return text.upper() + "!"'},
        {"name": "wrong base order", "old": "class Alert(Shout, Tag, Trim):", "new": "class Alert(Tag, Shout, Trim):"},
        {"name": "tag read from the class", "old": 'f"[{self.tag}] "', "new": 'f"[{Tag.tag}] "'},
    ],
    "sources": ["https://docs.python.org/3.11/library/functions.html#super",
                "https://docs.python.org/3.11/tutorial/classes.html#multiple-inheritance"],
}
