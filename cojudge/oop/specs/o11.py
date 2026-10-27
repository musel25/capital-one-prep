"""Original exercise: class attributes, instance attributes, and a registry."""
from cojudge.oop.steps import call, case, error, get, new, obj, put

SPEC = {
    "number": 11, "slug": "zoo-class-attributes", "title": "OOP at the zoo: class attributes",
    "difficulty": "Medium", "time": 30, "level": 3,
    "prerequisites": "Exercise 10. Subclasses.",
    "learn": """A **class attribute** is defined in the class body. Every instance shares it, and a
subclass can override it:

```python
class Animal:
    sound = "..."

class Lion(Animal):
    sound = "roar"
```

When Python reads `leo.sound`, it looks in the instance first, then in its class, then in the
base classes. An assignment `leo.sound = "purr"` creates an **instance** attribute on `leo` only.
`Lion.sound` and other lions do not change.

Class attributes are good for constants per class. They are dangerous for **mutable** state such
as a list or dictionary of objects, because all instances share one container. Keep that state
on `self`. `type(obj).__name__` gives the name of an object's class.""",
    "scenario": """A zoo management app tracks the animals in each zoo. Each species has a fixed
sound and number of legs. Each zoo numbers its own animals: 1, 2, 3, and so on. A number is never
reused, even after an animal moves to another zoo.""",
    "task": """Write `Animal`, its subclasses `Lion`, `Parrot`, and `Snake`, and `Zoo`.

- `Animal(name)`: store `name`. Class attributes: `sound = "..."` and `legs = 0`.
  `speak()` returns `"<name> says <sound>"`.
- Class attributes of the subclasses: `Lion`: `sound = "roar"`, `legs = 4`. `Parrot`:
  `sound = "squawk"`, `legs = 2`. `Snake`: `sound = "hiss"`, `legs = 0`.
- `Zoo(name)`: an empty zoo. Each zoo has its own animals and its own numbers.
  - `admit(kind, name)`: `kind` is `"lion"`, `"parrot"`, or `"snake"`; otherwise raise
    `ValueError`. Create the animal, give it the next number of this zoo (starting at 1), and
    return the number.
  - `animal(number)`: return the animal object. An unknown number raises `KeyError`.
  - `release(number)`: remove the animal and return its name. An unknown number raises
    `KeyError`. Numbers are never reused.
  - `roster()`: a list of `"#<number> <name> (<ClassName>)"` in number order.
  - `total_legs()`: the sum of `legs` of the animals in the zoo.

An assignment to one animal's `sound` changes only that animal.""",
    "constraints": ["At most 30 animals and 60 steps per test.", "The tests never change a class attribute through the class."],
    "hints": ["Keep a dictionary `number → animal` and a separate next-number counter on `self`.",
              "A class attribute `KINDS = {\"lion\": Lion, ...}` on `Zoo` maps a kind to its class. That dictionary never changes, so sharing it is safe."],
    "starter": '''class Animal:
    def __init__(self, name: str):
        raise NotImplementedError

    def speak(self) -> str:
        raise NotImplementedError


class Lion(Animal):
    pass


class Parrot(Animal):
    pass


class Snake(Animal):
    pass


class Zoo:
    def __init__(self, name: str):
        raise NotImplementedError

    def admit(self, kind: str, name: str) -> int:
        raise NotImplementedError

    def animal(self, number: int) -> Animal:
        raise NotImplementedError

    def release(self, number: int) -> str:
        raise NotImplementedError

    def roster(self) -> list[str]:
        raise NotImplementedError

    def total_legs(self) -> int:
        raise NotImplementedError
''',
    "reference": '''class Animal:
    sound = "..."
    legs = 0

    def __init__(self, name: str):
        self.name = name

    def speak(self) -> str:
        return f"{self.name} says {self.sound}"


class Lion(Animal):
    sound = "roar"
    legs = 4


class Parrot(Animal):
    sound = "squawk"
    legs = 2


class Snake(Animal):
    sound = "hiss"
    legs = 0


class Zoo:
    KINDS = {"lion": Lion, "parrot": Parrot, "snake": Snake}

    def __init__(self, name: str):
        self.name = name
        self._next = 1
        self._animals: dict[int, Animal] = {}

    def admit(self, kind: str, name: str) -> int:
        if kind not in self.KINDS:
            raise ValueError(f"unknown kind: {kind!r}")
        number = self._next
        self._next += 1
        self._animals[number] = self.KINDS[kind](name)
        return number

    def animal(self, number: int) -> Animal:
        return self._animals[number]

    def release(self, number: int) -> str:
        return self._animals.pop(number).name

    def roster(self) -> list[str]:
        return [f"#{number} {a.name} ({type(a).__name__})" for number, a in self._animals.items()]

    def total_legs(self) -> int:
        return sum(a.legs for a in self._animals.values())
''',
    "facts": ["subclass Lion Animal", "subclass Parrot Animal", "subclass Snake Animal"],
    "java": '''static final Map<String,String[]> SPECIES = Map.of(
    "Animal", new String[]{"...", "0"}, "Lion", new String[]{"roar", "4"},
    "Parrot", new String[]{"squawk", "2"}, "Snake", new String[]{"hiss", "0"});
static class Animal implements Obj {
    String kind, name, sound;
    public String type() { return kind; }
    Animal(String kind, String name) { this.kind = kind; this.name = name; this.sound = SPECIES.get(kind)[0]; }
    long legs() { return Long.parseLong(SPECIES.get(kind)[1]); }
}
static class Zoo implements Obj {
    long next = 1; TreeMap<Long,Animal> animals = new TreeMap<>();
    public String type() { return "Zoo"; }
}
Object step(Map<String,Object> op) {
    String d = s(op.get("do"));
    Object t = target(op);
    if (d.equals("new")) {
        if (t.equals("Zoo")) { arg(op, 0, "name", MISSING); return new Zoo(); }
        return new Animal((String) t, s(arg(op, 0, "name", MISSING)));
    }
    if (t instanceof String && d.equals("get")) {
        String[] sp = SPECIES.get((String) t);
        if (sp != null && s(op.get("attr")).equals("sound")) return sp[0];
        if (sp != null && s(op.get("attr")).equals("legs")) return Long.parseLong(sp[1]);
    }
    if (t instanceof Animal) {
        Animal a = (Animal) t;
        if (d.equals("call") && s(op.get("method")).equals("speak")) return a.name + " says " + a.sound;
        if (d.equals("get")) {
            String at = s(op.get("attr"));
            if (at.equals("name")) return a.name;
            if (at.equals("sound")) return a.sound;
            if (at.equals("legs")) return a.legs();
        }
        if (d.equals("set") && s(op.get("attr")).equals("sound")) { a.sound = s(val(op.get("value"))); return null; }
        throw err("AttributeError");
    }
    Zoo z = (Zoo) t;
    String m = s(op.get("method"));
    List<Object> a = args(op);
    if (m.equals("admit")) {
        String kind = s(a.get(0));
        String cls = kind.equals("lion") ? "Lion" : kind.equals("parrot") ? "Parrot" : kind.equals("snake") ? "Snake" : null;
        if (cls == null) throw err("ValueError");
        long number = z.next++;
        z.animals.put(number, new Animal(cls, s(a.get(1))));
        return number;
    }
    if (m.equals("animal") || m.equals("release")) {
        long number = lng(a.get(0));
        if (!z.animals.containsKey(number)) throw err("KeyError");
        return m.equals("animal") ? z.animals.get(number) : z.animals.remove(number).name;
    }
    if (m.equals("roster")) {
        List<Object> out = new ArrayList<>();
        for (Map.Entry<Long,Animal> e : z.animals.entrySet()) out.add("#" + e.getKey() + " " + e.getValue().name + " (" + e.getValue().kind + ")");
        return out;
    }
    if (m.equals("total_legs")) { long sum = 0; for (Animal x : z.animals.values()) sum += x.legs(); return sum; }
    throw err("AttributeError");
}
''',
    "approach": """Sound and legs are class attributes, so each species defines them once and
`speak` finds them through normal attribute lookup. An assignment on one animal creates an
instance attribute that shadows the class value for that animal only. Each zoo keeps its
dictionary and counter on `self`; a counter instead of `len(...) + 1` keeps numbers unique after
a release. Python dictionaries keep insertion order, which is number order here.""",
    "example_notes": [
        "Each species gets sound and legs from its class attributes. Numbers start at 1.",
        "Changing one lion's sound creates an instance attribute. The class and the other lion keep roar.",
        "Two zoos number their animals separately. A shared class-level dictionary would mix them.",
    ],
    "cases": [
        case("admit and speak",
             (new("Zoo", "City", save="z"), obj("Zoo")), (call("z", "admit", "lion", "Leo"), 1),
             (call("z", "admit", "parrot", "Polly"), 2), (call("z", "roster"), ["#1 Leo (Lion)", "#2 Polly (Parrot)"]),
             (call("z", "total_legs"), 6)),
        case("instance attribute shadows the class attribute",
             (new("Zoo", "City", save="z"), obj("Zoo")), (call("z", "admit", "lion", "Leo"), 1),
             (call("z", "admit", "lion", "Nala"), 2), (call("z", "animal", 1, save="leo"), obj("Lion")),
             (put("leo", "sound", "purr"), None), (call("leo", "speak"), "Leo says purr"),
             (call("z", "animal", 2, save="nala"), obj("Lion")), (call("nala", "speak"), "Nala says roar"),
             (get("Lion", "sound"), "roar")),
        case("zoos are independent",
             (new("Zoo", "North", save="a"), obj("Zoo")), (new("Zoo", "South", save="b"), obj("Zoo")),
             (call("a", "admit", "snake", "Kaa"), 1), (call("b", "admit", "lion", "Simba"), 1),
             (call("a", "roster"), ["#1 Kaa (Snake)"]), (call("b", "total_legs"), 4)),
        case("unknown kind",
             (new("Zoo", "City", save="z"), obj("Zoo")), (call("z", "admit", "tiger", "Raja"), error("ValueError")),
             (call("z", "admit", "Lion", "Leo"), error("ValueError")), (call("z", "admit", "lion", "Leo"), 1)),
        case("numbers are not reused after release",
             (new("Zoo", "City", save="z"), obj("Zoo")), (call("z", "admit", "lion", "A"), 1),
             (call("z", "admit", "lion", "B"), 2), (call("z", "release", 2), "B"), (call("z", "admit", "snake", "C"), 3),
             (call("z", "roster"), ["#1 A (Lion)", "#3 C (Snake)"])),
        case("unknown numbers",
             (new("Zoo", "City", save="z"), obj("Zoo")), (call("z", "animal", 1), error("KeyError")),
             (call("z", "admit", "parrot", "P"), 1), (call("z", "release", 1), "P"), (call("z", "release", 1), error("KeyError")),
             (call("z", "animal", 1), error("KeyError"))),
        case("base animal defaults",
             (new("Animal", "Thing", save="a"), obj("Animal")), (call("a", "speak"), "Thing says ..."),
             (get("a", "legs"), 0), (get("Animal", "sound"), "...")),
        case("class attributes per species",
             (get("Lion", "legs"), 4), (get("Parrot", "legs"), 2), (get("Snake", "legs"), 0),
             (get("Parrot", "sound"), "squawk"), (get("Snake", "sound"), "hiss")),
        case("empty zoo",
             (new("Zoo", "New", save="z"), obj("Zoo")), (call("z", "roster"), []), (call("z", "total_legs"), 0)),
        case("legs after release",
             (new("Zoo", "City", save="z"), obj("Zoo")), (call("z", "admit", "lion", "L"), 1),
             (call("z", "admit", "parrot", "P"), 2), (call("z", "admit", "snake", "S"), 3),
             (call("z", "release", 1), "L"), (call("z", "total_legs"), 2)),
        case("direct subclass instances",
             (new("Parrot", "Kiwi", save="p"), obj("Parrot")), (call("p", "speak"), "Kiwi says squawk"),
             (new("Snake", "Sly", save="s"), obj("Snake")), (get("s", "legs"), 0), (put("p", "sound", "hello"), None),
             (call("p", "speak"), "Kiwi says hello")),
        case("structure and many animals",
             ({"do": "check", "is": "subclass", "cls": "Snake", "of": "Animal"}, True),
             (new("Zoo", "Big", save="z"), obj("Zoo")), (call("z", "admit", "parrot", "A"), 1), (call("z", "admit", "parrot", "B"), 2),
             (call("z", "admit", "parrot", "C"), 3), (call("z", "admit", "lion", "D"), 4), (call("z", "total_legs"), 10)),
    ],
    "generate": lambda rng: (
        [new("Zoo", "A", save="a"), new("Zoo", "B", save="b")]
        + [rng.choice([call(rng.choice("ab"), "admit", rng.choice(["lion", "parrot", "snake", "snake", "eagle"]), rng.choice(["Ari", "Bo", "Cid"])),
                       call(rng.choice("ab"), "release", rng.randint(1, 5)), call(rng.choice("ab"), "roster"),
                       call(rng.choice("ab"), "total_legs")])
           for _ in range(rng.randint(5, 18))]),
    "mutations": [
        {"name": "shared animals dictionary",
         "old": "    def __init__(self, name: str):\n        self.name = name\n        self._next = 1\n        self._animals: dict[int, Animal] = {}\n",
         "new": "    _animals: dict = {}\n\n    def __init__(self, name: str):\n        self.name = name\n        self._next = 1\n"},
        {"name": "numbers reused after release", "old": "        number = self._next\n        self._next += 1\n",
         "new": "        number = len(self._animals) + 1\n"},
        {"name": "parrot legs wrong", "old": '    sound = "squawk"\n    legs = 2\n', "new": '    sound = "squawk"\n    legs = 4\n'},
    ],
    "sources": ["https://docs.python.org/3.11/tutorial/classes.html#class-and-instance-variables"],
}
