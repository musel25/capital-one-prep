"""Original exercise: static methods on a color class."""
from cojudge.oop.steps import builtin, call, case, check, error, get, new, obj, ref

SPEC = {
    "number": 4, "slug": "color-staticmethod", "title": "Color class with static methods",
    "difficulty": "Easy", "time": 25, "level": 1,
    "prerequisites": "Exercises 01–03. Properties and `__repr__`.",
    "learn": """A **static method** belongs to a class but does not receive `self` or `cls`. Mark it
with `@staticmethod`. Use it for a helper that is related to the class but does not need an
instance. You can call it on the class (`Color.hex_to_rgb("#ff0000")`) or on an instance.

```python
class Temperature:
    @staticmethod
    def c_to_f(celsius):
        return celsius * 9 // 5 + 32
```

Methods of the class can call the helper as `self.c_to_f(...)` or `Temperature.c_to_f(...)`.

Be careful with `int(text, 16)` for validation. It also accepts `"+f"`, `" ff"`, and `"f_f"`.
Check each character yourself when the format is strict.""",
    "scenario": """A design tool stores colors as hex codes such as `#ff8800`. Plugins need to convert
between hex codes and red/green/blue values without creating a color first. The tool also mixes
two colors for gradients.""",
    "task": """Write the class `Color`.

- A **valid hex code** is a string of exactly 7 characters: `#` followed by 6 characters from
  `0-9`, `a-f`, or `A-F`.
- `Color.hex_to_rgb(code)`: **static method**. Return the tuple `(red, green, blue)` of integers.
  An invalid code raises `ValueError`.
- `Color.rgb_to_hex(red, green, blue)`: **static method**. Return `"#rrggbb"` in lowercase. Each
  value must be an `int` (not a `bool`) from 0 to 255; otherwise raise `ValueError`.
- `Color(code)`: an invalid code raises `ValueError`. Store the code in lowercase in the
  attribute `hex`.
- `rgb`: read-only property. Return `(red, green, blue)` for this color.
- `blend(other)`: return a **new** `Color`. Each component is `(mine + theirs) // 2`.
- `repr(color)` returns `Color('#rrggbb')`.

The driver shows tuples as JSON lists.""",
    "constraints": ["At most 40 steps per test."],
    "hints": ["Check `len(code) == 7`, `code[0] == \"#\"`, and each character with `in \"0123456789abcdefABCDEF\"`.",
              "`f\"{value:02x}\"` formats an integer as two lowercase hex digits."],
    "starter": '''class Color:
    def __init__(self, code: str):
        raise NotImplementedError

    @staticmethod
    def hex_to_rgb(code: str) -> tuple[int, int, int]:
        raise NotImplementedError

    @staticmethod
    def rgb_to_hex(red: int, green: int, blue: int) -> str:
        raise NotImplementedError

    @property
    def rgb(self) -> tuple[int, int, int]:
        raise NotImplementedError

    def blend(self, other: "Color") -> "Color":
        raise NotImplementedError

    def __repr__(self) -> str:
        raise NotImplementedError
''',
    "reference": '''HEX_DIGITS = "0123456789abcdefABCDEF"


class Color:
    def __init__(self, code: str):
        self.hex_to_rgb(code)
        self.hex = code.lower()

    @staticmethod
    def hex_to_rgb(code: str) -> tuple[int, int, int]:
        if len(code) != 7 or code[0] != "#" or any(ch not in HEX_DIGITS for ch in code[1:]):
            raise ValueError(f"invalid hex code: {code!r}")
        return tuple(int(code[i:i + 2], 16) for i in (1, 3, 5))

    @staticmethod
    def rgb_to_hex(red: int, green: int, blue: int) -> str:
        for value in (red, green, blue):
            if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= 255:
                raise ValueError(f"invalid component: {value!r}")
        return f"#{red:02x}{green:02x}{blue:02x}"

    @property
    def rgb(self) -> tuple[int, int, int]:
        return self.hex_to_rgb(self.hex)

    def blend(self, other: "Color") -> "Color":
        mixed = [(a + b) // 2 for a, b in zip(self.rgb, other.rgb)]
        return Color(self.rgb_to_hex(*mixed))

    def __repr__(self) -> str:
        return f"Color({self.hex!r})"
''',
    "facts": ["staticmethod Color hex_to_rgb", "staticmethod Color rgb_to_hex", "property Color rgb"],
    "java": '''static class Color implements Obj { String hex; public String type() { return "Color"; } }
static List<Object> toRgb(Object raw) {
    if (!(raw instanceof String)) throw err("TypeError");
    String c = (String) raw;
    if (c.length() != 7 || c.charAt(0) != '#') throw err("ValueError");
    for (char ch : c.substring(1).toCharArray()) if ("0123456789abcdefABCDEF".indexOf(ch) < 0) throw err("ValueError");
    List<Object> out = new ArrayList<>();
    for (int i = 1; i < 7; i += 2) out.add(Long.parseLong(c.substring(i, i + 2), 16));
    return out;
}
static String toHex(List<Object> parts) {
    if (parts.size() != 3) throw err("TypeError");
    StringBuilder sb = new StringBuilder("#");
    for (Object p : parts) {
        if (!isInt(p) || lng(p) < 0 || lng(p) > 255) throw err("ValueError");
        sb.append(String.format("%02x", lng(p)));
    }
    return sb.toString();
}
Object step(Map<String,Object> op) {
    String d = s(op.get("do"));
    Object t = target(op);
    if (d.equals("new")) { Object code = arg(op, 0, "code", MISSING); toRgb(code); Color c = new Color(); c.hex = ((String) code).toLowerCase(); return c; }
    if (d.equals("call")) {
        String m = s(op.get("method"));
        if (m.equals("hex_to_rgb")) return toRgb(args(op).get(0));
        if (m.equals("rgb_to_hex")) return toHex(args(op));
        if (m.equals("blend") && t instanceof Color) {
            List<Object> a = toRgb(((Color) t).hex), b = toRgb(((Color) args(op).get(0)).hex), mixed = new ArrayList<>();
            for (int i = 0; i < 3; i++) mixed.add((lng(a.get(i)) + lng(b.get(i))) / 2);
            Color c = new Color(); c.hex = toHex(mixed); return c;
        }
    }
    Color c = (Color) t;
    if (d.equals("get")) {
        String a = s(op.get("attr"));
        if (a.equals("hex")) return c.hex;
        if (a.equals("rgb")) return toRgb(c.hex);
    }
    if (d.equals("set") && s(op.get("attr")).equals("rgb")) throw err("AttributeError");
    if (d.equals("repr")) return "Color('" + c.hex + "')";
    throw err("AttributeError");
}
''',
    "approach": """`hex_to_rgb` validates every character instead of trusting `int(..., 16)`, which
accepts signs, spaces, and underscores. The constructor reuses it for validation. Both helpers
are static methods: they do not need an instance, and the class and its instances can call them.
`blend` builds the result through `rgb_to_hex`, so it returns a normal, validated `Color`.""",
    "example_notes": [
        "Static methods work on the class without an instance. Tuples appear as JSON lists.",
        "The color stores its code in lowercase. rgb reads it back as numbers.",
        "int(\"f_\", 16) would accept the underscore. A strict check rejects the code.",
    ],
    "cases": [
        case("static conversion on the class",
             (call("Color", "hex_to_rgb", "#ff8000"), [255, 128, 0]), (call("Color", "rgb_to_hex", 0, 128, 255), "#0080ff")),
        case("instance stores lowercase",
             (new("Color", "#FFAA00", save="c"), obj("Color")), (get("c", "hex"), "#ffaa00"), (get("c", "rgb"), [255, 170, 0]),
             (builtin("repr", "c"), "Color('#ffaa00')")),
        case("underscore is not a hex digit",
             (call("Color", "hex_to_rgb", "#ff_f00"), error("ValueError")), (new("Color", "#1_2345"), error("ValueError"))),
        case("wrong length and missing hash",
             (new("Color", "#fff"), error("ValueError")), (new("Color", "ff8800"), error("ValueError")),
             (new("Color", "#ff88001"), error("ValueError")), (new("Color", "x123456"), error("ValueError"))),
        case("signs and spaces are rejected",
             (call("Color", "hex_to_rgb", "#+f+f+f"), error("ValueError")), (call("Color", "hex_to_rgb", "# fffff"), error("ValueError")),
             (call("Color", "hex_to_rgb", "#gggggg"), error("ValueError"))),
        case("component range",
             (call("Color", "rgb_to_hex", 0, 0, 0), "#000000"), (call("Color", "rgb_to_hex", 255, 255, 255), "#ffffff"),
             (call("Color", "rgb_to_hex", 256, 0, 0), error("ValueError")), (call("Color", "rgb_to_hex", 0, -1, 0), error("ValueError"))),
        case("component type",
             (call("Color", "rgb_to_hex", True, 0, 0), error("ValueError")), (call("Color", "rgb_to_hex", 1.0, 0, 0), error("ValueError")),
             (call("Color", "rgb_to_hex", 0, 0, "9"), error("ValueError"))),
        case("blend returns a new color",
             (new("Color", "#ff0000", save="r"), obj("Color")), (new("Color", "#0000ff", save="b"), obj("Color")),
             (call("r", "blend", ref("b"), save="m"), obj("Color")), (builtin("repr", "m"), "Color('#7f007f')"),
             (get("r", "hex"), "#ff0000")),
        case("blend rounds down",
             (new("Color", "#010203", save="a"), obj("Color")), (new("Color", "#020304", save="b"), obj("Color")),
             (call("a", "blend", ref("b"), save="m"), obj("Color")), (get("m", "rgb"), [1, 2, 3])),
        case("static method through an instance",
             (new("Color", "#123456", save="c"), obj("Color")), (call("c", "hex_to_rgb", "#0a0B0c"), [10, 11, 12]),
             (call("c", "rgb_to_hex", 10, 11, 12), "#0a0b0c")),
        case("rgb is read-only",
             (new("Color", "#abcdef", save="c"), obj("Color")), ({"do": "set", "obj": "c", "attr": "rgb", "value": [0, 0, 0]}, error("AttributeError")),
             (get("c", "rgb"), [171, 205, 239])),
        case("structure",
             (check("staticmethod", "Color", "hex_to_rgb"), True), (check("staticmethod", "Color", "rgb_to_hex"), True),
             (check("property", "Color", "rgb"), True), (check("staticmethod", "Color", "blend"), False)),
    ],
    "generate": lambda rng: (lambda codes: (
        [new("Color", rng.choice(codes[:6]), save="a"), new("Color", rng.choice(codes[:6]), save="b")]
        + [rng.choice([call("Color", "hex_to_rgb", rng.choice(codes)),
                       call("Color", "rgb_to_hex", *[rng.choice([0, 7, 128, 255, 256, -2, rng.randint(0, 255)]) for _ in range(3)]),
                       call("a", "blend", ref("b"), save="a"), builtin("repr", "a"), get("b", "rgb"), get("a", "hex")])
           for _ in range(rng.randint(4, 12))]))(
        ["#000000", "#FFFFFF", "#a1B2c3", "#ff8800", "#123abc", "#0F0f0F", "#12345", "#12345g", "123456#",
         "#-12345", "#ff ff0", "#1_2_34"]),
    "mutations": [
        {"name": "int() accepts underscores", "old": "any(ch not in HEX_DIGITS for ch in code[1:])",
         "new": "int(code[1:], 16) < 0"},
        {"name": "uppercase output", "old": 'f"#{red:02x}{green:02x}{blue:02x}"', "new": 'f"#{red:02X}{green:02X}{blue:02X}"'},
        {"name": "hex not normalized", "old": "self.hex = code.lower()", "new": "self.hex = code"},
        {"name": "booleans accepted", "old": "isinstance(value, bool) or ", "new": ""},
    ],
    "sources": ["https://docs.python.org/3.11/library/functions.html#staticmethod"],
}
