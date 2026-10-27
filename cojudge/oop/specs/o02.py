"""Original exercise: validated properties and representation dunder methods."""
from cojudge.oop.steps import builtin, case, error, get, new, obj, put

SPEC = {
    "number": 2, "slug": "member-properties-repr", "title": "Member class: properties, repr and str",
    "difficulty": "Easy", "time": 25, "level": 1,
    "prerequisites": "Exercise 01. Read-only properties.",
    "learn": """A property can also have a **setter**. Write `@email.setter` above a second method
with the same name. Assignment `member.email = "x"` then calls it, so you can validate the value
before you store it. Store the real value in a "private" attribute such as `self._email`. If
`__init__` assigns `self.email = email`, the constructor uses the same validation.

Two dunder methods control how an object looks as text:

- `__repr__` is for developers. A good repr looks like the code that creates the object, for
  example `Member('Ann', 'Lee', 'ann@mail.io')`. Use `!r` in an f-string to quote a value:
  `f"{self.first!r}"`.
- `__str__` is for users. `str(obj)` and `print(obj)` use it.""",
    "scenario": """A club website stores its members. The admin page shows `str(member)`. Logs and the
debugger show `repr(member)`. A typo in an email address must be rejected when it is entered,
not later when the club sends a message.""",
    "task": """Write the class `Member`.

- `Member(first, last, email)`: store `first` and `last` in public attributes. Set the email
  through the `email` setter, so an invalid email raises `ValueError`.
- `full_name`: read-only property. Return `"<first> <last>"`.
- `handle`: read-only property. Return the first letter of `first` followed by `last`, all in
  lowercase. Example: `Ann Lee` → `"alee"`.
- `email`: property with a setter. An email is valid when all of these are true:
  - It contains exactly one `@`.
  - The part before `@` is not empty.
  - The part after `@` contains a `.`, and does not start or end with `.`.

  An invalid value raises `ValueError` and keeps the old email.
- `repr(member)` returns `Member('<first>', '<last>', '<email>')`.
- `str(member)` returns `<first> <last> <<email>>`, for example `Ann Lee <ann@mail.io>`.

A change to `first` or `last` must show in every later result.""",
    "constraints": ["Names contain letters only and are not empty.",
                    "Emails contain no spaces, quotes, or backslashes.", "At most 40 steps per test."],
    "hints": ["Use `value.partition(\"@\")` to split the address once.",
              "Validate first. Assign `self._email` only after every check passes."],
    "starter": '''class Member:
    def __init__(self, first: str, last: str, email: str):
        raise NotImplementedError

    @property
    def full_name(self) -> str:
        raise NotImplementedError

    @property
    def handle(self) -> str:
        raise NotImplementedError

    @property
    def email(self) -> str:
        raise NotImplementedError

    @email.setter
    def email(self, value: str) -> None:
        raise NotImplementedError

    def __repr__(self) -> str:
        raise NotImplementedError

    def __str__(self) -> str:
        raise NotImplementedError
''',
    "reference": '''class Member:
    def __init__(self, first: str, last: str, email: str):
        self.first = first
        self.last = last
        self.email = email

    @property
    def full_name(self) -> str:
        return f"{self.first} {self.last}"

    @property
    def handle(self) -> str:
        return (self.first[0] + self.last).lower()

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        local, _, domain = value.partition("@")
        if (value.count("@") != 1 or not local or "." not in domain
                or domain.startswith(".") or domain.endswith(".")):
            raise ValueError(f"invalid email: {value!r}")
        self._email = value

    def __repr__(self) -> str:
        return f"Member({self.first!r}, {self.last!r}, {self.email!r})"

    def __str__(self) -> str:
        return f"{self.full_name} <{self.email}>"
''',
    "facts": ["property Member full_name", "property Member handle", "property Member email"],
    "java": '''static class Member implements Obj {
    String first, last, email;
    public String type() { return "Member"; }
}
static boolean validEmail(String v) {
    int at = v.indexOf('@');
    if (at < 0 || v.indexOf('@', at + 1) >= 0 || at == 0) return false;
    String domain = v.substring(at + 1);
    return domain.contains(".") && !domain.startsWith(".") && !domain.endsWith(".");
}
Object step(Map<String,Object> op) {
    String d = s(op.get("do"));
    if (d.equals("new")) {
        Member m = new Member();
        m.first = s(arg(op, 0, "first", MISSING)); m.last = s(arg(op, 1, "last", MISSING));
        String e = s(arg(op, 2, "email", MISSING));
        if (!validEmail(e)) throw err("ValueError");
        m.email = e; return m;
    }
    Member m = (Member) target(op);
    String a = op.containsKey("attr") ? s(op.get("attr")) : "";
    if (d.equals("get")) {
        if (a.equals("first")) return m.first;
        if (a.equals("last")) return m.last;
        if (a.equals("email")) return m.email;
        if (a.equals("full_name")) return m.first + " " + m.last;
        if (a.equals("handle")) return (m.first.substring(0, 1) + m.last).toLowerCase();
        throw err("AttributeError");
    }
    if (d.equals("set")) {
        String v = s(val(op.get("value")));
        if (a.equals("full_name") || a.equals("handle")) throw err("AttributeError");
        if (a.equals("email")) { if (!validEmail(v)) throw err("ValueError"); m.email = v; }
        if (a.equals("first")) m.first = v;
        if (a.equals("last")) m.last = v;
        return null;
    }
    if (d.equals("repr")) return "Member('" + m.first + "', '" + m.last + "', '" + m.email + "')";
    if (d.equals("str")) return m.first + " " + m.last + " <" + m.email + ">";
    throw err("AttributeError");
}
''',
    "approach": """`__init__` assigns `self.email`, so construction and later changes share one
validation path. The setter checks the whole value before it assigns `_email`; a rejected value
cannot leave a half-updated object. `full_name` and `handle` are computed properties. `__repr__`
uses `!r` so the strings appear quoted, like the call that creates the object.""",
    "example_notes": [
        "full_name joins the names. handle is the first initial plus the last name, in lowercase.",
        "repr looks like the constructor call. str is the readable form with the email in angle brackets.",
        "An address with two @ signs is invalid. The setter raises ValueError, and the old email stays.",
    ],
    "cases": [
        case("names and handle",
             (new("Member", "Ann", "Lee", "ann@mail.io", save="m"), obj("Member")),
             (get("m", "full_name"), "Ann Lee"), (get("m", "handle"), "alee")),
        case("repr and str",
             (new("Member", "Ann", "Lee", "ann@mail.io", save="m"), obj("Member")),
             (builtin("repr", "m"), "Member('Ann', 'Lee', 'ann@mail.io')"),
             (builtin("str", "m"), "Ann Lee <ann@mail.io>")),
        case("rejected email keeps the old value",
             (new("Member", "Bo", "Kim", "bo@kim.dev", save="m"), obj("Member")),
             (put("m", "email", "bo@@kim.dev"), error("ValueError")), (get("m", "email"), "bo@kim.dev")),
        case("constructor validates the email",
             (new("Member", "Ann", "Lee", "ann.mail.io"), error("ValueError")),
             (new("Member", "Ann", "Lee", "@mail.io"), error("ValueError")),
             (new("Member", "Ann", "Lee", "ann@mailio"), error("ValueError"))),
        case("domain dots at the edges",
             (new("Member", "Cy", "Ng", "cy@ng.org", save="m"), obj("Member")),
             (put("m", "email", "cy@.ng.org"), error("ValueError")), (put("m", "email", "cy@ng.org."), error("ValueError")),
             (put("m", "email", "cy@ng"), error("ValueError")), (get("m", "email"), "cy@ng.org")),
        case("valid change shows everywhere",
             (new("Member", "Ann", "Lee", "ann@mail.io", save="m"), obj("Member")),
             (put("m", "email", "a.lee@work.co.uk"), None), (get("m", "email"), "a.lee@work.co.uk"),
             (builtin("str", "m"), "Ann Lee <a.lee@work.co.uk>")),
        case("renamed member",
             (new("Member", "Ann", "Lee", "ann@mail.io", save="m"), obj("Member")),
             (put("m", "last", "Park"), None), (get("m", "full_name"), "Ann Park"), (get("m", "handle"), "apark"),
             (builtin("repr", "m"), "Member('Ann', 'Park', 'ann@mail.io')")),
        case("handle is lowercase",
             (new("Member", "MARIA", "DelaCruz", "m@dc.ph", save="m"), obj("Member")),
             (get("m", "handle"), "mdelacruz"), (get("m", "full_name"), "MARIA DelaCruz")),
        case("read-only computed properties",
             (new("Member", "Ann", "Lee", "ann@mail.io", save="m"), obj("Member")),
             (put("m", "full_name", "Bob Ray"), error("AttributeError")),
             (put("m", "handle", "bob"), error("AttributeError")), (get("m", "full_name"), "Ann Lee")),
        case("shortest valid email and double dot",
             (new("Member", "Al", "Ox", "a@b.c", save="m"), obj("Member")), (get("m", "email"), "a@b.c"),
             (put("m", "email", "x@y..z"), None), (get("m", "email"), "x@y..z")),
        case("two members are independent",
             (new("Member", "Ann", "Lee", "ann@mail.io", save="a"), obj("Member")),
             (new("Member", "Bo", "Kim", "bo@kim.dev", save="b"), obj("Member")),
             (put("a", "email", "new@mail.io"), None), (get("b", "email"), "bo@kim.dev"),
             (builtin("str", "a"), "Ann Lee <new@mail.io>")),
        case("keyword arguments and empty local part",
             (new("Member", first="Eve", last="Stone", email="eve@stone.net", save="m"), obj("Member")),
             (put("m", "email", "@stone.net"), error("ValueError")),
             (builtin("repr", "m"), "Member('Eve', 'Stone', 'eve@stone.net')")),
    ],
    "generate": lambda rng: (lambda names, emails: (
        [new("Member", *rng.choice(names), "start@club.org", save="m")]
        + [rng.choice([put("m", "email", rng.choice(emails)), get("m", "email"), builtin("str", "m"),
                       builtin("repr", "m"), get("m", "handle"), put("m", "first", rng.choice(names)[0]),
                       put("m", "last", rng.choice(names)[1]), get("m", "full_name")])
           for _ in range(rng.randint(4, 12))]))(
        [("Ann", "Lee"), ("Bo", "Kim"), ("Zoe", "Quinn"), ("Raj", "Patel"), ("Li", "Wu"), ("Omar", "Haddad")],
        ["a@b.co", "x@@y.io", "@y.io", "x@y", "x@.y", "x@y.", "first.last@mail.example.com", "q@r..s",
         "noat.example", "me@home.net", "a@b@c.d", "ok@ok.ok"]),
    "mutations": [
        {"name": "two @ signs accepted", "old": 'value.count("@") != 1 or ', "new": ""},
        {"name": "constructor skips validation", "old": "        self.email = email\n",
         "new": "        self._email = email\n"},
        {"name": "repr without quotes", "old": 'f"Member({self.first!r}, {self.last!r}, {self.email!r})"',
         "new": 'f"Member({self.first}, {self.last}, {self.email})"'},
    ],
    "sources": ["https://docs.python.org/3.11/library/functions.html#property",
                "https://docs.python.org/3.11/reference/datamodel.html#object.__repr__"],
}
