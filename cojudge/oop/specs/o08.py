"""Original exercise: write a frozen, ordered data class."""
from cojudge.oop.steps import builtin, call, case, check, error, get, new, obj, op, put, ref

SPEC = {
    "number": 8, "slug": "product-dataclass", "title": "Write your own data class",
    "difficulty": "Medium", "time": 30, "level": 2,
    "prerequisites": "Exercises 01–07. `__init__`, `__repr__`, and `__eq__`.",
    "learn": """`@dataclass` writes the boring methods for you. You list the fields with type
annotations, and Python generates `__init__`, `__repr__`, and `__eq__`:

```python
from dataclasses import dataclass

@dataclass(frozen=True, order=True)
class Point:
    x: int
    y: int = 0
```

- `frozen=True` makes instances read-only: assignment raises `FrozenInstanceError`.
- `order=True` adds `<`, `<=`, `>`, `>=`. They compare the fields as a tuple, in definition order.
- `__post_init__(self)` runs after the generated `__init__`. Validate or convert fields there.
  In a frozen class, change a field with `object.__setattr__(self, "name", value)`.
- `dataclasses.replace(obj, x=5)` returns a copy with some fields changed. It calls `__init__`
  again, so `__post_init__` validates the copy too.""",
    "scenario": """A shop catalog keeps products as values: two products with the same fields are the
same product, and a product never changes after creation. A price change creates a new product.
Lists of products must sort by name, then price.""",
    "task": """Write `Product` as a `@dataclass` with `frozen=True` and `order=True`.

- Fields, in this order: `name: str`, `price_cents: int`, `tags: tuple[str, ...] = ()`.
- `__post_init__`: an empty `name` or a negative `price_cents` raises `ValueError`. Convert
  `tags` to a tuple, because callers can pass a list.
- The generated methods give the rest:
  - `repr` is `Product(name='Pen', price_cents=150, tags=('office',))`.
  - `==` compares all fields. `<` compares `(name, price_cents, tags)`.
  - Assignment to any field raises `FrozenInstanceError`.
- `with_discount(percent)`: `percent` is an integer from 0 to 100; otherwise raise `ValueError`.
  Return a **new** product with price `price_cents * (100 - percent) // 100`. The original does
  not change.""",
    "constraints": ["Names and tags are ASCII letters and spaces.", "At most 40 steps per test."],
    "hints": ["Python's repr for a one-element tuple has a trailing comma: `('office',)`. The dataclass repr does this for you.",
              "Use `dataclasses.replace` in `with_discount`."],
    "starter": '''from dataclasses import dataclass, replace


class Product:
    # Make this a frozen, ordered dataclass with the fields name, price_cents, and tags.

    def __post_init__(self) -> None:
        raise NotImplementedError

    def with_discount(self, percent: int) -> "Product":
        raise NotImplementedError
''',
    "reference": '''from dataclasses import dataclass, replace


@dataclass(frozen=True, order=True)
class Product:
    name: str
    price_cents: int
    tags: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("name must not be empty")
        if self.price_cents < 0:
            raise ValueError("price must not be negative")
        object.__setattr__(self, "tags", tuple(self.tags))

    def with_discount(self, percent: int) -> "Product":
        if not 0 <= percent <= 100:
            raise ValueError("percent must be from 0 to 100")
        return replace(self, price_cents=self.price_cents * (100 - percent) // 100)
''',
    "facts": ["dataclass Product"],
    "java": '''static class Product implements Obj {
    String name; long price; List<String> tags = new ArrayList<>();
    public String type() { return "Product"; }
    Product(String name, long price, List<Object> tags) {
        if (name.isEmpty() || price < 0) throw err("ValueError");
        this.name = name; this.price = price; for (Object t : tags) this.tags.add(s(t));
    }
    String repr() {
        StringBuilder t = new StringBuilder("(");
        for (int i = 0; i < tags.size(); i++) t.append(i > 0 ? ", " : "").append("'").append(tags.get(i)).append("'");
        t.append(tags.size() == 1 ? ",)" : ")");
        return "Product(name='" + name + "', price_cents=" + price + ", tags=" + t + ")";
    }
    int compare(Product o) {
        int c = name.compareTo(o.name);
        if (c != 0) return c;
        if (price != o.price) return Long.compare(price, o.price);
        for (int i = 0; i < Math.min(tags.size(), o.tags.size()); i++) { c = tags.get(i).compareTo(o.tags.get(i)); if (c != 0) return c; }
        return Integer.compare(tags.size(), o.tags.size());
    }
}
Object step(Map<String,Object> op) {
    String d = s(op.get("do"));
    if (d.equals("new")) return new Product(s(arg(op, 0, "name", MISSING)), lng(arg(op, 1, "price_cents", MISSING)), arr(arg(op, 2, "tags", list())));
    if (d.equals("op")) {
        Object l = val(op.get("left")), r = val(op.get("right")); String sym = s(op.get("op"));
        if (!(l instanceof Product && r instanceof Product)) {
            if (sym.equals("==")) return false;
            if (sym.equals("!=")) return true;
            throw err("TypeError");
        }
        int c = ((Product) l).compare((Product) r);
        switch (sym) { case "==": return c == 0; case "!=": return c != 0; case "<": return c < 0;
                       case "<=": return c <= 0; case ">": return c > 0; default: return c >= 0; }
    }
    Product p = (Product) target(op);
    if (d.equals("get")) {
        String a = s(op.get("attr"));
        if (a.equals("name")) return p.name;
        if (a.equals("price_cents")) return p.price;
        if (a.equals("tags")) return new ArrayList<Object>(p.tags);
    }
    if (d.equals("set")) throw err("FrozenInstanceError");
    if (d.equals("repr")) return p.repr();
    if (d.equals("call") && s(op.get("method")).equals("with_discount")) {
        long pct = lng(args(op).get(0));
        if (pct < 0 || pct > 100) throw err("ValueError");
        return new Product(p.name, p.price * (100 - pct) / 100, new ArrayList<Object>(p.tags));
    }
    throw err("AttributeError");
}
''',
    "approach": """The decorator generates `__init__`, `__repr__`, `__eq__`, the four ordering
methods, and `__hash__` (because the class is frozen and has `eq`). `__post_init__` validates and
converts `tags` with `object.__setattr__`, the documented way around `frozen`. `with_discount`
uses `replace`, which runs `__post_init__` again on the copy.""",
    "example_notes": [
        "The generated repr lists every field. The list of tags becomes a tuple with a trailing comma.",
        "Products are read-only: assignment raises FrozenInstanceError. with_discount returns a new product.",
        "order=True compares name first, then price. Equal fields mean equal products.",
    ],
    "cases": [
        case("generated repr with tuple tags",
             (new("Product", "Pen", 150, ["office"], save="p"), obj("Product")),
             (builtin("repr", "p"), "Product(name='Pen', price_cents=150, tags=('office',))"), (get("p", "tags"), ["office"])),
        case("frozen with a discount copy",
             (new("Product", "Mug", 1000, save="p"), obj("Product")), (put("p", "price_cents", 1), error("FrozenInstanceError")),
             (call("p", "with_discount", 25, save="q"), obj("Product")), (get("q", "price_cents"), 750), (get("p", "price_cents"), 1000)),
        case("ordering and equality",
             (new("Product", "Cup", 500, save="a"), obj("Product")), (new("Product", "Cup", 300, save="b"), obj("Product")),
             (new("Product", "Bowl", 900, save="c"), obj("Product")), (op(ref("b"), "<", ref("a")), True),
             (op(ref("c"), "<", ref("b")), True), (op(ref("a"), "==", ref("b")), False)),
        case("validation in post_init",
             (new("Product", "", 100), error("ValueError")), (new("Product", "Pen", -1), error("ValueError")),
             (new("Product", "Free", 0, save="f"), obj("Product")), (get("f", "tags"), [])),
        case("repr with zero and two tags",
             (new("Product", "Lamp", 2500, save="a"), obj("Product")), (builtin("repr", "a"), "Product(name='Lamp', price_cents=2500, tags=())"),
             (new("Product", "Desk", 9000, ["home", "office"], save="b"), obj("Product")),
             (builtin("repr", "b"), "Product(name='Desk', price_cents=9000, tags=('home', 'office'))")),
        case("equal values are equal",
             (new("Product", "Pen", 150, ["a"], save="x"), obj("Product")), (new("Product", "Pen", 150, ["a"], save="y"), obj("Product")),
             (op(ref("x"), "==", ref("y")), True), (op(ref("x"), "<=", ref("y")), True), (op(ref("x"), "<", ref("y")), False)),
        case("tags break ties",
             (new("Product", "Pen", 150, ["blue"], save="x"), obj("Product")), (new("Product", "Pen", 150, ["red"], save="y"), obj("Product")),
             (op(ref("x"), "<", ref("y")), True), (op(ref("y"), ">", ref("x")), True), (op(ref("x"), "!=", ref("y")), True)),
        case("discount bounds and rounding",
             (new("Product", "Gum", 99, save="p"), obj("Product")), (call("p", "with_discount", 0, save="a"), obj("Product")),
             (get("a", "price_cents"), 99), (call("p", "with_discount", 100, save="b"), obj("Product")), (get("b", "price_cents"), 0),
             (call("p", "with_discount", 33, save="c"), obj("Product")), (get("c", "price_cents"), 66)),
        case("invalid discount",
             (new("Product", "Gum", 99, save="p"), obj("Product")), (call("p", "with_discount", 101), error("ValueError")),
             (call("p", "with_discount", -5), error("ValueError"))),
        case("discount keeps other fields",
             (new("Product", "Bag", 2000, ["travel"], save="p"), obj("Product")), (call("p", "with_discount", 50, save="q"), obj("Product")),
             (builtin("repr", "q"), "Product(name='Bag', price_cents=1000, tags=('travel',))")),
        case("every field is frozen and comparison with other types",
             (new("Product", "Ink", 300, save="p"), obj("Product")), (put("p", "name", "Toner"), error("FrozenInstanceError")),
             (put("p", "tags", []), error("FrozenInstanceError")), (op(ref("p"), "==", "Ink"), False), (op(ref("p"), "<", 5), error("TypeError"))),
        case("keywords and structure",
             (new("Product", price_cents=40, name="Clip", save="p"), obj("Product")), (check("dataclass", "Product"), True),
             (builtin("repr", "p"), "Product(name='Clip', price_cents=40, tags=())")),
    ],
    "generate": lambda rng: (lambda names: (
        [new("Product", rng.choice(names), rng.randint(0, 500), rng.sample(["red", "blue", "eco"], rng.randint(0, 2)), save=v) for v in "ab"]
        + [rng.choice([op(ref("a"), rng.choice(["<", "<=", "==", ">"]), ref("b")), builtin("repr", rng.choice("ab")),
                       call(rng.choice("ab"), "with_discount", rng.choice([0, 10, 50, 99, 100, 120]), save=rng.choice("ab")),
                       put("a", "price_cents", 1), get("b", "price_cents"),
                       new("Product", rng.choice(names + [""]), rng.choice([-1, 0, 250]), save="b")])
           for _ in range(rng.randint(4, 12))]))(["Pen", "Pad", "Ink", "Pen Set"]),
    "mutations": [
        {"name": "tags not converted to a tuple", "old": '        object.__setattr__(self, "tags", tuple(self.tags))\n', "new": ""},
        {"name": "zero price rejected", "old": "if self.price_cents < 0:", "new": "if self.price_cents <= 0:"},
        {"name": "discount rounds the wrong way", "old": "self.price_cents * (100 - percent) // 100",
         "new": "-(-self.price_cents * (100 - percent) // 100)"},
        {"name": "price before name", "old": "    name: str\n    price_cents: int\n", "new": "    price_cents: int\n    name: str\n"},
    ],
    "sources": ["https://docs.python.org/3.11/library/dataclasses.html"],
}
