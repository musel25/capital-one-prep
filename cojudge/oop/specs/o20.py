"""Original exercise: a config file parser class (tox-style INI)."""
from cojudge.oop.steps import call, case, error, get, new, obj, op, ref

TOX = "[tox]\nenvlist = py311, lint\n\n[testenv]\ndeps =\n    pytest\n    coverage\ncommands = pytest -q\n"

SPEC = {
    "number": 20, "slug": "ini-config-parser", "title": "Complete an INI config parser class",
    "difficulty": "Hard", "time": 45, "level": 5,
    "prerequisites": "Levels 1–4. Properties, `__contains__`, and exceptions.",
    "learn": """A parser class reads text once, in `__init__`, and turns it into a clean data
structure. The other methods only answer questions about that structure. If the text is invalid,
raise in `__init__`: then no half-built object exists.

Parse line by line with a little **state**: the current section and the last key. Decide what
each line is in a fixed order, because some rules overlap. For example, an indented line is a
continuation even when it contains `=`.

```python
for line in text.split("\\n"):
    stripped = line.strip()
    if not stripped or stripped[0] in "#;":
        continue            # blank or comment
    ...
```

`str.partition("=")` splits at the **first** `=` only, so a value can contain `=`. Python's
`configparser` module handles real INI files; here you write the rules yourself, so you control
every detail.""",
    "scenario": """A test runner reads its settings from a `tox.ini`-style file. A value can span
several indented lines, for example a list of dependencies. The runner must reject a broken file
with a clear error instead of running with wrong settings.""",
    "task": """Write `IniConfig`. Split the text on `"\\n"` and classify each line in this order:

1. **Blank or comment:** after stripping spaces and tabs, the line is empty or starts with `#`
   or `;`. Ignore it. It does not end a value.
2. **Continuation:** the line starts with a space or a tab. Append its stripped text to the value
   of the last key in the current section, separated by `"\\n"`. If that value is empty, the text
   replaces it. Without a previous key in this section, raise `ValueError`.
3. **Section header:** the stripped line starts with `[` and ends with `]`. The name is the text
   between them, stripped. An empty or repeated name raises `ValueError`.
4. **Key line:** the line contains `=`. The key is the stripped text before the first `=`; the
   value is the stripped text after it. A key before any section, an empty key, or a repeated key
   in the same section raises `ValueError`.
5. Anything else raises `ValueError`.

Methods:

- `IniConfig(text)`: parse as above.
- `sections`: read-only property. The section names in file order.
- `keys(section)`: the keys of the section in file order. Unknown section: `KeyError`.
- `get(section, key, default=None)`: the value, or `default` if the section or key is missing.
- `get_list(section, key)`: split the value on newlines and commas, strip each item, drop empty
  items. Missing section or key: `KeyError`.
- `section in config`: `True` if the section exists.""",
    "constraints": ["Text has at most 60 lines and contains no carriage returns.", "At most 30 steps per test."],
    "hints": ["Reset the last key to `None` when a new section starts.",
              "Store a dictionary `section → {key: value}`. Python dictionaries keep file order."],
    "starter": '''class IniConfig:
    def __init__(self, text: str):
        raise NotImplementedError

    @property
    def sections(self) -> list[str]:
        raise NotImplementedError

    def keys(self, section: str) -> list[str]:
        raise NotImplementedError

    def get(self, section: str, key: str, default=None):
        raise NotImplementedError

    def get_list(self, section: str, key: str) -> list[str]:
        raise NotImplementedError

    def __contains__(self, section: object) -> bool:
        raise NotImplementedError
''',
    "reference": '''import re


class IniConfig:
    def __init__(self, text: str):
        self._data: dict[str, dict[str, str]] = {}
        section = key = None
        for number, line in enumerate(text.split("\\n"), start=1):
            stripped = line.strip(" \\t")
            if not stripped or stripped[0] in "#;":
                continue
            if line[0] in " \\t":
                if key is None:
                    raise ValueError(f"line {number}: continuation without a key")
                current = self._data[section][key]
                self._data[section][key] = f"{current}\\n{stripped}" if current else stripped
            elif stripped.startswith("[") and stripped.endswith("]"):
                name = stripped[1:-1].strip(" \\t")
                if not name or name in self._data:
                    raise ValueError(f"line {number}: empty or repeated section {name!r}")
                self._data[name] = {}
                section, key = name, None
            elif "=" in line:
                name, _, value = line.partition("=")
                name = name.strip(" \\t")
                if section is None or not name or name in self._data[section]:
                    raise ValueError(f"line {number}: invalid key {name!r}")
                self._data[section][name] = value.strip(" \\t")
                key = name
            else:
                raise ValueError(f"line {number}: cannot parse {line!r}")

    @property
    def sections(self) -> list[str]:
        return list(self._data)

    def keys(self, section: str) -> list[str]:
        return list(self._data[section])

    def get(self, section: str, key: str, default=None):
        return self._data.get(section, {}).get(key, default)

    def get_list(self, section: str, key: str) -> list[str]:
        items = re.split(r"[\\n,]", self._data[section][key])
        return [item.strip(" \\t") for item in items if item.strip(" \\t")]

    def __contains__(self, section: object) -> bool:
        return section in self._data
''',
    "facts": ["property IniConfig sections"],
    "java": '''static class Ini implements Obj {
    LinkedHashMap<String,LinkedHashMap<String,String>> data = new LinkedHashMap<>();
    public String type() { return "IniConfig"; }
}
static String trimST(String s) { int a = 0, b = s.length(); while (a < b && (s.charAt(a) == ' ' || s.charAt(a) == '\\t')) a++; while (b > a && (s.charAt(b - 1) == ' ' || s.charAt(b - 1) == '\\t')) b--; return s.substring(a, b); }
static Ini parse(String text) {
    Ini ini = new Ini(); String section = null, key = null;
    for (String line : text.split("\\n", -1)) {
        String st = trimST(line);
        if (st.isEmpty() || st.charAt(0) == '#' || st.charAt(0) == ';') continue;
        if (line.charAt(0) == ' ' || line.charAt(0) == '\\t') {
            if (key == null) throw err("ValueError");
            String cur = ini.data.get(section).get(key);
            ini.data.get(section).put(key, cur.isEmpty() ? st : cur + "\\n" + st);
        } else if (st.startsWith("[") && st.endsWith("]") && st.length() >= 2) {
            String name = trimST(st.substring(1, st.length() - 1));
            if (name.isEmpty() || ini.data.containsKey(name)) throw err("ValueError");
            ini.data.put(name, new LinkedHashMap<>()); section = name; key = null;
        } else if (line.contains("=")) {
            int eq = line.indexOf('=');
            String name = trimST(line.substring(0, eq));
            if (section == null || name.isEmpty() || ini.data.get(section).containsKey(name)) throw err("ValueError");
            ini.data.get(section).put(name, trimST(line.substring(eq + 1))); key = name;
        } else throw err("ValueError");
    }
    return ini;
}
Object step(Map<String,Object> op) {
    String d = s(op.get("do"));
    if (d.equals("new")) return parse(s(arg(op, 0, "text", MISSING)));
    if (d.equals("op")) return ((Ini) val(op.get("right"))).data.containsKey(val(op.get("left")));
    Ini ini = (Ini) target(op);
    if (d.equals("get") && s(op.get("attr")).equals("sections")) return new ArrayList<Object>(ini.data.keySet());
    if (d.equals("call")) {
        String m = s(op.get("method")); List<Object> a = args(op);
        if (m.equals("keys")) { if (!ini.data.containsKey(s(a.get(0)))) throw err("KeyError"); return new ArrayList<Object>(ini.data.get(s(a.get(0))).keySet()); }
        if (m.equals("get")) {
            Object fallback = a.size() > 2 ? a.get(2) : kwargs(op).getOrDefault("default", null);
            LinkedHashMap<String,String> sec = ini.data.get(s(a.get(0)));
            return sec != null && sec.containsKey(s(a.get(1))) ? sec.get(s(a.get(1))) : fallback;
        }
        if (m.equals("get_list")) {
            LinkedHashMap<String,String> sec = ini.data.get(s(a.get(0)));
            if (sec == null || !sec.containsKey(s(a.get(1)))) throw err("KeyError");
            List<Object> out = new ArrayList<>();
            for (String item : sec.get(s(a.get(1))).split("[\\n,]", -1)) if (!trimST(item).isEmpty()) out.add(trimST(item));
            return out;
        }
    }
    throw err("AttributeError");
}
''',
    "approach": """The constructor walks the lines once with two pieces of state: the current
section and the last key. The fixed order of the checks resolves overlaps: comments first, then
indentation, then headers, then `=`. Any unclassified line raises, so a broken file never creates
an object. The query methods read the nested dictionaries; `get_list` splits on both separators
with one regular expression. Parsing is O(total text length).""",
    "example_notes": [
        "The indented lines continue deps. The empty value after = is replaced by the first line, so deps is pytest + newline + coverage.",
        "get_list splits on commas and newlines. get returns the default for a missing key.",
        "A key before any section is invalid, so the constructor raises ValueError.",
    ],
    "cases": [
        case("tox file with a continuation",
             (new("IniConfig", TOX, save="c"), obj("IniConfig")), (get("c", "sections"), ["tox", "testenv"]),
             (call("c", "get", "testenv", "deps"), "pytest\ncoverage"), (call("c", "keys", "testenv"), ["deps", "commands"])),
        case("lists and defaults",
             (new("IniConfig", TOX, save="c"), obj("IniConfig")), (call("c", "get_list", "tox", "envlist"), ["py311", "lint"]),
             (call("c", "get_list", "testenv", "deps"), ["pytest", "coverage"]), (call("c", "get", "tox", "skip", "no"), "no"),
             (op("testenv", "in", ref("c")), True)),
        case("key before a section",
             (new("IniConfig", "name = x\n[a]\n"), error("ValueError")),),
        case("comments and blank lines",
             (new("IniConfig", "# top\n; also\n[a]\n  # indented comment\nx = 1\n\n   \ny = 2\n", save="c"), obj("IniConfig")),
             (call("c", "keys", "a"), ["x", "y"]), (call("c", "get", "a", "y"), "2")),
        case("continuation after a blank line and a comment",
             (new("IniConfig", "[a]\nx = one\n\n# note\n  two\n", save="c"), obj("IniConfig")), (call("c", "get", "a", "x"), "one\ntwo")),
        case("continuation errors",
             (new("IniConfig", "  orphan\n[a]\n"), error("ValueError")), (new("IniConfig", "[a]\n  orphan\n"), error("ValueError")),
             (new("IniConfig", "[a]\nx = 1\n[b]\n  lost\n"), error("ValueError"))),
        case("section rules",
             (new("IniConfig", "[a]\n[a]\n"), error("ValueError")), (new("IniConfig", "[ ]\n"), error("ValueError")),
             (new("IniConfig", "[ spaced name ]\nk=v\n", save="c"), obj("IniConfig")), (get("c", "sections"), ["spaced name"])),
        case("key rules",
             (new("IniConfig", "[a]\nx = 1\nx = 2\n"), error("ValueError")), (new("IniConfig", "[a]\n = 1\n"), error("ValueError")),
             (new("IniConfig", "[a]\njust text\n"), error("ValueError")),
             (new("IniConfig", "[a]\nx = 1\n[b]\nx = 2\n", save="c"), obj("IniConfig")), (call("c", "get", "b", "x"), "2")),
        case("value with = and empty value",
             (new("IniConfig", "[db]\nurl = postgres://u@h/db?sslmode=require\nempty =\n", save="c"), obj("IniConfig")),
             (call("c", "get", "db", "url"), "postgres://u@h/db?sslmode=require"), (call("c", "get", "db", "empty"), ""),
             (call("c", "get_list", "db", "empty"), [])),
        case("indented line with = is a continuation",
             (new("IniConfig", "[env]\nsetenv =\n    A = 1\n    B = 2\n", save="c"), obj("IniConfig")),
             (call("c", "keys", "env"), ["setenv"]), (call("c", "get_list", "env", "setenv"), ["A = 1", "B = 2"])),
        case("missing lookups",
             (new("IniConfig", "[a]\nx = 1\n", save="c"), obj("IniConfig")), (call("c", "keys", "b"), error("KeyError")),
             (call("c", "get", "b", "x"), None), (call("c", "get_list", "a", "y"), error("KeyError")),
             (call("c", "get_list", "b", "x"), error("KeyError")), (op("b", "in", ref("c")), False)),
        case("tabs, mixed separators, and an empty file",
             (new("IniConfig", "[t]\nitems = a,, b\n\tc , d\n\t\n", save="c"), obj("IniConfig")),
             (call("c", "get", "t", "items"), "a,, b\nc , d"), (call("c", "get_list", "t", "items"), ["a", "b", "c", "d"]),
             (new("IniConfig", "", save="e"), obj("IniConfig")), (get("e", "sections"), [])),
    ],
    "generate": lambda rng: (lambda lines: (
        [new("IniConfig", "\n".join(lines), save="c")]
        + [rng.choice([get("c", "sections"), call("c", "keys", rng.choice(["s1", "s2", "zz"])),
                       call("c", "get", rng.choice(["s1", "s2"]), rng.choice(["k1", "k2", "k3"]), "?"),
                       call("c", "get_list", rng.choice(["s1", "s2"]), rng.choice(["k1", "k2"])),
                       op(rng.choice(["s1", "s2", "s3"]), "in", ref("c"))])
           for _ in range(rng.randint(3, 8))]))(
        [rng.choice(["[s1]", "[s2]", "k1 = a, b", "k2 =", "  x", "\ty, z", "# c", "", "k3 = v=w", "  ", "bad line", "[s1]"])
         for _ in range(rng.randint(1, 9))]),
    "mutations": [
        {"name": "empty value keeps a leading newline", "old": 'f"{current}\\n{stripped}" if current else stripped',
         "new": 'f"{current}\\n{stripped}"'},
        {"name": "continuation checked after the key rule", "old": "            if line[0] in \" \\t\":\n",
         "new": "            if line[0] in \" \\t\" and \"=\" not in line:\n"},
        {"name": "repeated keys replace", "old": "if section is None or not name or name in self._data[section]:",
         "new": "if section is None or not name:"},
        {"name": "key kept after a new section", "old": "section, key = name, None", "new": "section = name"},
    ],
    "sources": ["https://docs.python.org/3.11/library/stdtypes.html#str.partition",
                "https://docs.python.org/3.11/library/configparser.html"],
}
