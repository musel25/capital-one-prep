"""Original exercise: abstract base classes and a template method."""
from cojudge.oop.steps import call, case, check, error, get, new, obj

SPEC = {
    "number": 13, "slug": "abc-payment-methods", "title": "Abstract base classes",
    "difficulty": "Medium", "time": 30, "level": 3,
    "prerequisites": "Exercises 10–12. Subclasses and `super()`.",
    "learn": """An **abstract base class** (ABC) defines what its subclasses must provide. It cannot
be instantiated itself:

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> int: ...

    def describe(self) -> str:          # a normal method that uses the abstract one
        return f"area {self.area()}"
```

`Shape()` raises `TypeError`. A subclass that does not override **every** abstract method is
still abstract, and creating it also raises `TypeError`. This catches a missing method when the
object is created, not later when someone calls it.

An abstract property uses both decorators: `@property` above `@abstractmethod`. A subclass can
satisfy it with a plain class attribute, such as `name = "card"`.

`describe` above is a **template method**: the base class fixes the steps, and each subclass
fills in one step.""",
    "scenario": """A checkout service supports several payment methods. Every method must report its
name and fee, and every charge must produce the same receipt format. The team wants a new method
without a fee rule to fail as soon as it is created.""",
    "task": """Write the abstract class `PaymentMethod` and three concrete subclasses. The starter
also has `Draft`, an unfinished payment method. Do not change `Draft`.

- `PaymentMethod(ABC)`:
  - `name`: abstract property.
  - `fee(amount)`: abstract method.
  - `charge(amount)`: a normal method. `amount` must be an `int` (not a `bool`) of at least 1;
    otherwise raise `ValueError`. Return the receipt
    `{"method": name, "amount": amount, "fee": fee, "total": amount + fee}`.
- `Card`: `name` is `"card"`. The fee is `30 + amount × 29 / 1000`, rounded **up**.
- `BankTransfer`: `name` is `"bank"`. The fee is always `50`.
- `Wallet(balance)`: `name` is `"wallet"`. A negative `balance` raises `ValueError`. Store it in
  `balance`. The fee is `0`. `charge(amount)` raises `ValueError` when `amount` is more than
  `balance`. Otherwise it uses the base `charge`, then subtracts `amount` from `balance`. A
  rejected charge does not change `balance`.

Creating `PaymentMethod` or `Draft` raises `TypeError`.""",
    "constraints": ["Amounts in the tests are integers or booleans from -10 to 10,000,000.", "At most 40 steps per test."],
    "hints": ["`Wallet.charge` can check the balance, then call `super().charge(amount)`, and only then subtract.",
              "Ceiling division: `-(-amount * 29 // 1000)`."],
    "starter": '''from abc import ABC, abstractmethod


class PaymentMethod(ABC):
    def charge(self, amount: int) -> dict:
        raise NotImplementedError


class Card(PaymentMethod):
    pass


class BankTransfer(PaymentMethod):
    pass


class Wallet(PaymentMethod):
    pass


class Draft(PaymentMethod):
    """Unfinished: it has a name but no fee rule. Do not change this class."""
    name = "draft"
''',
    "reference": '''from abc import ABC, abstractmethod


class PaymentMethod(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def fee(self, amount: int) -> int: ...

    def charge(self, amount: int) -> dict:
        if isinstance(amount, bool) or not isinstance(amount, int) or amount < 1:
            raise ValueError("amount must be a positive integer")
        fee = self.fee(amount)
        return {"method": self.name, "amount": amount, "fee": fee, "total": amount + fee}


class Card(PaymentMethod):
    name = "card"

    def fee(self, amount: int) -> int:
        return 30 + -(-amount * 29 // 1000)


class BankTransfer(PaymentMethod):
    name = "bank"

    def fee(self, amount: int) -> int:
        return 50


class Wallet(PaymentMethod):
    name = "wallet"

    def __init__(self, balance: int):
        if balance < 0:
            raise ValueError("balance must not be negative")
        self.balance = balance

    def fee(self, amount: int) -> int:
        return 0

    def charge(self, amount: int) -> dict:
        if amount > self.balance:
            raise ValueError("insufficient balance")
        receipt = super().charge(amount)
        self.balance -= amount
        return receipt


class Draft(PaymentMethod):
    """Unfinished: it has a name but no fee rule. Do not change this class."""
    name = "draft"
''',
    "facts": ["abstract PaymentMethod", "abstract Draft", "subclass Card PaymentMethod",
              "subclass BankTransfer PaymentMethod", "subclass Wallet PaymentMethod"],
    "java": '''static class Pay implements Obj {
    String kind; long balance;
    public String type() { return kind; }
    String name() { return kind.equals("Card") ? "card" : kind.equals("BankTransfer") ? "bank" : "wallet"; }
    long fee(long amount) { return kind.equals("Card") ? 30 + (amount * 29 + 999) / 1000 : kind.equals("BankTransfer") ? 50 : 0; }
}
Object step(Map<String,Object> op) {
    String d = s(op.get("do"));
    Object t = target(op);
    if (d.equals("new")) {
        if (t.equals("PaymentMethod") || t.equals("Draft")) throw err("TypeError");
        Pay p = new Pay(); p.kind = (String) t;
        if (t.equals("Wallet")) { p.balance = lng(arg(op, 0, "balance", MISSING)); if (p.balance < 0) throw err("ValueError"); }
        return p;
    }
    if (t instanceof String && d.equals("get") && s(op.get("attr")).equals("name")) {
        if (t.equals("Card")) return "card"; if (t.equals("BankTransfer")) return "bank"; if (t.equals("Wallet")) return "wallet";
        if (t.equals("Draft")) return "draft";
    }
    Pay p = (Pay) t;
    if (d.equals("get")) {
        String a = s(op.get("attr"));
        if (a.equals("name")) return p.name();
        if (a.equals("balance") && p.kind.equals("Wallet")) return p.balance;
    }
    if (d.equals("call")) {
        String m = s(op.get("method"));
        Object raw = args(op).get(0);
        if (m.equals("fee")) return p.fee(lng(raw));
        if (m.equals("charge")) {
            if (p.kind.equals("Wallet") && !(raw instanceof Boolean) && lng(raw) > p.balance) throw err("ValueError");
            if (p.kind.equals("Wallet") && raw instanceof Boolean && (b(raw) ? 1 : 0) > p.balance) throw err("ValueError");
            if (!isInt(raw) || lng(raw) < 1) throw err("ValueError");
            long amount = lng(raw), fee = p.fee(amount);
            if (p.kind.equals("Wallet")) p.balance -= amount;
            return map("method", p.name(), "amount", amount, "fee", fee, "total", amount + fee);
        }
    }
    throw err("AttributeError");
}
''',
    "approach": """`PaymentMethod` declares `name` and `fee` abstract, so Python refuses to create the
base class or any subclass that misses one of them, such as `Draft`. `charge` is a template
method: it validates once and builds the receipt from the subclass's `name` and `fee`. `Wallet`
adds a precondition and a state change around `super().charge`, in an order that leaves the
balance unchanged when any check fails.""",
    "example_notes": [
        "Card fee: 30 + ceil(1000 × 29 / 1000) = 30 + 29 = 59.",
        "The abstract base class and the unfinished Draft class both raise TypeError when created.",
        "The wallet rejects 600 because the balance is 500, then accepts 200. The balance becomes 300.",
    ],
    "cases": [
        case("card receipt",
             (new("Card", save="c"), obj("Card")),
             (call("c", "charge", 1000), {"method": "card", "amount": 1000, "fee": 59, "total": 1059})),
        case("abstract classes cannot be created",
             (new("PaymentMethod"), error("TypeError")), (new("Draft"), error("TypeError"))),
        case("wallet balance",
             (new("Wallet", 500, save="w"), obj("Wallet")), (call("w", "charge", 600), error("ValueError")),
             (call("w", "charge", 200), {"method": "wallet", "amount": 200, "fee": 0, "total": 200}), (get("w", "balance"), 300)),
        case("card fee rounds up",
             (new("Card", save="c"), obj("Card")), (call("c", "fee", 1), 31), (call("c", "fee", 34), 31),
             (call("c", "fee", 35), 32), (call("c", "fee", 2000), 88)),
        case("bank transfer",
             (new("BankTransfer", save="b"), obj("BankTransfer")),
             (call("b", "charge", 1), {"method": "bank", "amount": 1, "fee": 50, "total": 51}), (get("b", "name"), "bank")),
        case("invalid amounts",
             (new("Card", save="c"), obj("Card")), (call("c", "charge", 0), error("ValueError")),
             (call("c", "charge", -5), error("ValueError")), (call("c", "charge", True), error("ValueError"))),
        case("wallet rejection keeps the balance",
             (new("Wallet", 100, save="w"), obj("Wallet")), (call("w", "charge", -5), error("ValueError")),
             (call("w", "charge", 0), error("ValueError")), (get("w", "balance"), 100),
             (call("w", "charge", 100), {"method": "wallet", "amount": 100, "fee": 0, "total": 100}), (get("w", "balance"), 0)),
        case("wallet exact and empty balance",
             (new("Wallet", 0, save="w"), obj("Wallet")), (call("w", "charge", 1), error("ValueError")),
             (new("Wallet", -1), error("ValueError"))),
        case("names from class attributes",
             (get("Card", "name"), "card"), (get("Wallet", "name"), "wallet"), (get("Draft", "name"), "draft")),
        case("abstract checks",
             (check("abstract", "PaymentMethod"), True), (check("abstract", "Draft"), True),
             (check("abstract", "Card"), False), (check("abstract", "Wallet"), False)),
        case("large card charge",
             (new("Card", save="c"), obj("Card")),
             (call("c", "charge", 10000000), {"method": "card", "amount": 10000000, "fee": 290030, "total": 10290030})),
        case("polymorphic subclasses",
             (check("subclass", "Wallet", of="PaymentMethod"), True), (check("subclass", "BankTransfer", of="PaymentMethod"), True),
             (new("Wallet", balance=70, save="w"), obj("Wallet")), (call("w", "fee", 70), 0),
             (call("w", "charge", 70), {"method": "wallet", "amount": 70, "fee": 0, "total": 70})),
    ],
    "generate": lambda rng: (lambda kind: (
        [new(kind, rng.choice([0, 50, 1000]), save="p") if kind == "Wallet" else new(kind, save="p")]
        + [rng.choice([call("p", "charge", rng.choice([1, 33, 34, 35, 999, 1000, 1001, 0, -3, rng.randint(1, 10 ** 6)])),
                       call("p", "fee", rng.randint(1, 5000)), get("p", "name")])
           for _ in range(rng.randint(2, 8))] + ([get("p", "balance")] if kind == "Wallet" else [])))(
        rng.choice(["Card", "BankTransfer", "Wallet", "Wallet", "Draft", "PaymentMethod"])),
    "mutations": [
        {"name": "fee is not abstract", "old": "    @abstractmethod\n    def fee(self, amount: int) -> int: ...\n",
         "new": "    def fee(self, amount: int) -> int:\n        return 0\n"},
        {"name": "card rounds down", "old": "30 + -(-amount * 29 // 1000)", "new": "30 + amount * 29 // 1000"},
        {"name": "wallet subtracts before validation", "old": "        receipt = super().charge(amount)\n        self.balance -= amount\n",
         "new": "        self.balance -= amount\n        receipt = super().charge(amount)\n"},
        {"name": "booleans accepted", "old": "isinstance(amount, bool) or ", "new": ""},
    ],
    "sources": ["https://docs.python.org/3.11/library/abc.html"],
}
