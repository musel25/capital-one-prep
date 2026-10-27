"""Original exercise: enrich a value class with dunder methods."""
from cojudge.oop.steps import builtin, case, error, get, new, obj, op, ref

SPEC = {
    "number": 17, "slug": "money-dunder-methods", "title": "Enrich a class with dunder methods",
    "difficulty": "Medium", "time": 35, "level": 4,
    "prerequisites": "Exercises 05 and 15–16. `__eq__`, `__repr__`, and `NotImplemented`.",
    "learn": """Python operators call **dunder methods**: `a + b` calls `a.__add__(b)`, `a < b` calls
`a.__lt__(b)`, and `bool(a)` calls `a.__bool__()`. Implement them, and your objects work with
normal Python syntax.

When a method gets an operand that it does not support, it must **return** `NotImplemented` (it
must not raise). Python then tries the reflected method on the other operand, for example
`b.__radd__(a)`. If both return `NotImplemented`, Python raises `TypeError`, or for `==` falls
back to identity. `__rmul__` makes `2 * price` work, not only `price * 2`.

`functools.total_ordering` writes `<=`, `>`, and `>=` for you when you define `__eq__` and
`__lt__`. If you define `__eq__`, define `__hash__` too, or instances are unhashable.

Raise `ValueError` for a supported type with a bad value, such as two different currencies.""",
    "scenario": """An invoicing service adds and compares amounts of money. Amounts are whole cents,
never floats. Adding euros to dollars is a bug that must fail loudly, not silently produce a
wrong total.""",
    "task": """Write the class `Money`.

- `Money(cents, currency)`: `cents` must be an `int` (not a `bool`); otherwise raise `TypeError`.
  `currency` must be three uppercase ASCII letters; otherwise raise `ValueError`.
- `repr`: `Money(1250, 'EUR')`. `str`: `EUR 12.50`. Negative amounts: `EUR -0.05`.
- `a == b`: `True` for the same cents and currency. For a non-`Money` operand, return
  `NotImplemented` (so `money == 5` is `False`). Make `Money` hashable.
- `a < b`, `<=`, `>`, `>=`: compare cents. Different currencies raise `ValueError`. A non-`Money`
  operand gives `TypeError` (return `NotImplemented`).
- `a + b` and `a - b`: a new `Money`. Different currencies raise `ValueError`. A non-`Money`
  operand gives `TypeError`.
- `money * n` and `n * money`: `n` is an `int` (not a `bool`). Other types give `TypeError`.
- `bool(money)` is `False` only for zero cents.""",
    "constraints": ["Amounts are at most 10^12 cents.", "At most 40 steps per test."],
    "hints": ["Use `@functools.total_ordering` and define only `__eq__` and `__lt__`.",
              "Format with `divmod(abs(self.cents), 100)` and add the sign yourself."],
    "starter": '''from functools import total_ordering


class Money:
    def __init__(self, cents: int, currency: str):
        raise NotImplementedError
''',
    "reference": '''from functools import total_ordering
import string


@total_ordering
class Money:
    def __init__(self, cents: int, currency: str):
        if isinstance(cents, bool) or not isinstance(cents, int):
            raise TypeError("cents must be an integer")
        if len(currency) != 3 or any(ch not in string.ascii_uppercase for ch in currency):
            raise ValueError(f"invalid currency: {currency!r}")
        self.cents = cents
        self.currency = currency

    def __repr__(self) -> str:
        return f"Money({self.cents}, {self.currency!r})"

    def __str__(self) -> str:
        units, rest = divmod(abs(self.cents), 100)
        sign = "-" if self.cents < 0 else ""
        return f"{self.currency} {sign}{units}.{rest:02d}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        return (self.cents, self.currency) == (other.cents, other.currency)

    def __hash__(self) -> int:
        return hash((self.cents, self.currency))

    def _same_currency(self, other: "Money") -> None:
        if self.currency != other.currency:
            raise ValueError(f"cannot mix {self.currency} and {other.currency}")

    def __lt__(self, other: "Money") -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        self._same_currency(other)
        return self.cents < other.cents

    def __add__(self, other: "Money") -> "Money":
        if not isinstance(other, Money):
            return NotImplemented
        self._same_currency(other)
        return Money(self.cents + other.cents, self.currency)

    def __sub__(self, other: "Money") -> "Money":
        if not isinstance(other, Money):
            return NotImplemented
        self._same_currency(other)
        return Money(self.cents - other.cents, self.currency)

    def __mul__(self, factor: int) -> "Money":
        if isinstance(factor, bool) or not isinstance(factor, int):
            return NotImplemented
        return Money(self.cents * factor, self.currency)

    __rmul__ = __mul__

    def __bool__(self) -> bool:
        return self.cents != 0
''',
    "facts": [],
    "java": '''static class Money implements Obj {
    long cents; String cur;
    public String type() { return "Money"; }
    Money(Object cents, Object cur) {
        if (!isInt(cents)) throw err("TypeError");
        String c = s(cur);
        if (!c.matches("[A-Z]{3}")) throw err("ValueError");
        this.cents = lng(cents); this.cur = c;
    }
}
static Money same(Money a, Object b) {
    if (!(b instanceof Money)) throw err("TypeError");
    Money m = (Money) b;
    if (!a.cur.equals(m.cur)) throw err("ValueError");
    return m;
}
Object step(Map<String,Object> op) {
    String d = s(op.get("do"));
    if (d.equals("new")) return new Money(arg(op, 0, "cents", MISSING), arg(op, 1, "currency", MISSING));
    if (d.equals("op")) {
        Object l = val(op.get("left")), r = val(op.get("right"));
        String sym = s(op.get("op"));
        if (sym.equals("==") || sym.equals("!=")) {
            boolean eq = l instanceof Money && r instanceof Money ? ((Money) l).cents == ((Money) r).cents && ((Money) l).cur.equals(((Money) r).cur) : l == r;
            return sym.equals("==") ? eq : !eq;
        }
        if (sym.equals("*")) {
            Money m = l instanceof Money ? (Money) l : r instanceof Money ? (Money) r : null;
            Object n = l instanceof Money ? r : l;
            if (m == null || !isInt(n)) throw err("TypeError");
            Money out = new Money(0L, m.cur); out.cents = m.cents * lng(n); return out;
        }
        if (!(l instanceof Money)) throw err("TypeError");
        Money a = (Money) l, b = same(a, r);
        switch (sym) {
            case "+": { Money out = new Money(0L, a.cur); out.cents = a.cents + b.cents; return out; }
            case "-": { Money out = new Money(0L, a.cur); out.cents = a.cents - b.cents; return out; }
            case "<": return a.cents < b.cents;
            case "<=": return a.cents <= b.cents;
            case ">": return a.cents > b.cents;
            case ">=": return a.cents >= b.cents;
        }
        throw err("TypeError");
    }
    Money m = (Money) target(op);
    if (d.equals("repr")) return "Money(" + m.cents + ", '" + m.cur + "')";
    if (d.equals("str")) { long a = Math.abs(m.cents); return m.cur + " " + (m.cents < 0 ? "-" : "") + (a / 100) + "." + String.format("%02d", a % 100); }
    if (d.equals("bool")) return m.cents != 0;
    if (d.equals("get")) { String a = s(op.get("attr")); if (a.equals("cents")) return m.cents; if (a.equals("currency")) return m.cur; }
    throw err("AttributeError");
}
''',
    "approach": """Each operator checks the operand type first and returns `NotImplemented` for
foreign types, so Python produces the standard `TypeError` (or `False` for `==`). Currency
mismatches are a supported type with a wrong value, so they raise `ValueError`. `total_ordering`
derives `<=`, `>`, and `>=` from `__lt__` and `__eq__`. `__rmul__ = __mul__` handles `2 * m`.
`__hash__` matches `__eq__`, so equal amounts work as dictionary keys.""",
    "example_notes": [
        "+ returns a new Money. str shows the currency and two decimal places.",
        "Mixing currencies raises ValueError. Adding a plain number gives TypeError because __add__ returns NotImplemented.",
        "2 * m uses __rmul__. Comparisons with == against a number are False, not an error.",
    ],
    "cases": [
        case("add and format",
             (new("Money", 1250, "EUR", save="a"), obj("Money")), (new("Money", 75, "EUR", save="b"), obj("Money")),
             (op(ref("a"), "+", ref("b"), save="c"), obj("Money")), (builtin("str", "c"), "EUR 13.25"),
             (builtin("repr", "c"), "Money(1325, 'EUR')")),
        case("currency and type errors",
             (new("Money", 100, "EUR", save="e"), obj("Money")), (new("Money", 100, "USD", save="u"), obj("Money")),
             (op(ref("e"), "+", ref("u")), error("ValueError")), (op(ref("e"), "+", 5), error("TypeError"))),
        case("reflected multiply and equality with numbers",
             (new("Money", 199, "GBP", save="m"), obj("Money")), (op(2, "*", ref("m"), save="d"), obj("Money")),
             (builtin("repr", "d"), "Money(398, 'GBP')"), (op(ref("m"), "==", 199), False)),
        case("negative formatting",
             (new("Money", -5, "EUR", save="a"), obj("Money")), (builtin("str", "a"), "EUR -0.05"),
             (new("Money", -12345, "USD", save="b"), obj("Money")), (builtin("str", "b"), "USD -123.45"),
             (new("Money", 0, "JPY", save="z"), obj("Money")), (builtin("str", "z"), "JPY 0.00")),
        case("constructor validation",
             (new("Money", 1.5, "EUR"), error("TypeError")), (new("Money", True, "EUR"), error("TypeError")),
             (new("Money", 1, "eur"), error("ValueError")), (new("Money", 1, "EURO"), error("ValueError")),
             (new("Money", 1, "E1R"), error("ValueError"))),
        case("subtraction",
             (new("Money", 500, "EUR", save="a"), obj("Money")), (new("Money", 800, "EUR", save="b"), obj("Money")),
             (op(ref("a"), "-", ref("b"), save="c"), obj("Money")), (builtin("str", "c"), "EUR -3.00"),
             (op(ref("a"), "-", 1), error("TypeError"))),
        case("ordering",
             (new("Money", 100, "EUR", save="a"), obj("Money")), (new("Money", 200, "EUR", save="b"), obj("Money")),
             (op(ref("a"), "<", ref("b")), True), (op(ref("a"), ">=", ref("b")), False), (op(ref("b"), ">", ref("a")), True),
             (op(ref("a"), "<=", ref("a")), True)),
        case("ordering errors",
             (new("Money", 100, "EUR", save="a"), obj("Money")), (new("Money", 100, "USD", save="u"), obj("Money")),
             (op(ref("a"), "<", ref("u")), error("ValueError")), (op(ref("a"), "<", 100), error("TypeError")),
             (op(ref("a"), ">=", ref("u")), error("ValueError"))),
        case("equality",
             (new("Money", 100, "EUR", save="a"), obj("Money")), (new("Money", 100, "EUR", save="b"), obj("Money")),
             (new("Money", 100, "USD", save="c"), obj("Money")), (op(ref("a"), "==", ref("b")), True),
             (op(ref("a"), "==", ref("c")), False), (op(ref("a"), "!=", ref("c")), True), (op(ref("a"), "!=", "EUR 1.00"), True)),
        case("multiply rules",
             (new("Money", 250, "CHF", save="m"), obj("Money")), (op(ref("m"), "*", 3, save="t"), obj("Money")),
             (builtin("str", "t"), "CHF 7.50"), (op(ref("m"), "*", 1.5), error("TypeError")), (op(ref("m"), "*", True), error("TypeError")),
             (op(ref("m"), "*", ref("m")), error("TypeError"))),
        case("truth value",
             (new("Money", 0, "EUR", save="z"), obj("Money")), (builtin("bool", "z"), False),
             (new("Money", -1, "EUR", save="n"), obj("Money")), (builtin("bool", "n"), True),
             (op(ref("n"), "*", 0, save="k"), obj("Money")), (builtin("bool", "k"), False)),
        case("large amounts stay exact",
             (new("Money", 1000000000000, "USD", save="a"), obj("Money")), (new("Money", 1, "USD", save="b"), obj("Money")),
             (op(ref("a"), "+", ref("b"), save="c"), obj("Money")), (builtin("str", "c"), "USD 10000000000.01"),
             (get("c", "cents"), 1000000000001)),
    ],
    "generate": lambda rng: (
        [new("Money", rng.randint(-500, 5000), rng.choice(["EUR", "EUR", "USD"]), save=v) for v in "ab"]
        + [rng.choice([op(ref("a"), rng.choice(["+", "-", "<", "<=", ">", ">=", "==", "!="]), ref("b"), save="c"),
                       op(ref(rng.choice("ab")), "*", rng.choice([0, 2, -3, 1.5]), save="a"), op(rng.choice([3, 7]), "*", ref("b"), save="b"),
                       builtin("str", rng.choice("ab")), builtin("repr", rng.choice("ab")), builtin("bool", rng.choice("ab")),
                       op(ref("a"), rng.choice(["+", "<", "=="]), rng.choice([5, "x"]))])
           for _ in range(rng.randint(4, 12))]),
    "mutations": [
        {"name": "add returns NotImplemented for currency mismatch",
         "old": "        self._same_currency(other)\n        return Money(self.cents + other.cents, self.currency)\n",
         "new": "        return Money(self.cents + other.cents, self.currency)\n"},
        {"name": "negative sign lost", "old": 'sign = "-" if self.cents < 0 else ""', "new": 'sign = ""'},
        {"name": "no reflected multiply", "old": "    __rmul__ = __mul__\n", "new": ""},
        {"name": "eq raises for foreign types", "old": "        if not isinstance(other, Money):\n            return NotImplemented\n        return (self.cents",
         "new": "        if not isinstance(other, Money):\n            raise TypeError\n        return (self.cents"},
    ],
    "sources": ["https://docs.python.org/3.11/reference/datamodel.html#emulating-numeric-types",
                "https://docs.python.org/3.11/library/functools.html#functools.total_ordering"],
}
