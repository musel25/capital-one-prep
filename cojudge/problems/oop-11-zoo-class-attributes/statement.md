# 11. OOP at the zoo: class attributes

[Course list](/?course=python-oop) · Level 3: Inheritance and composition · Medium · About 30 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Exercise 10. Subclasses.

A **class attribute** is defined in the class body. Every instance shares it, and a
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
on `self`. `type(obj).__name__` gives the name of an object's class.

</details>

**Scenario:** A zoo management app tracks the animals in each zoo. Each species has a fixed
sound and number of legs. Each zoo numbers its own animals: 1, 2, 3, and so on. A number is never
reused, even after an animal moves to another zoo.

Write `Animal`, its subclasses `Lion`, `Parrot`, and `Snake`, and `Zoo`.

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

An assignment to one animal's `sound` changes only that animal.

**Constraints:**

- At most 30 animals and 60 steps per test.
- The tests never change a class attribute through the class.

<details>
<summary><strong>How the tests work</strong></summary>

Each test is a list of steps. The supplied driver at the bottom of the editor runs
the steps on your classes, in order, and records one result per step:

- A step that raises records `{"error": "ExceptionName"}`, and the test continues.
- An object of a class records `{"object": "ClassName"}`. Tuples show as lists.

| Step `do` | What the driver runs |
| --- | --- |
| `new` | `cls(*args, **kwargs)` |
| `get` / `set` | `obj.attr` / `obj.attr = value` (records `null`) |
| `call` | `obj.method(*args, **kwargs)`; `obj` can also be a class name |
| `invoke` | `obj(*args)` |
| `op` | `left <op> right`, for example `a + b` or `a @ b` |
| `item` / `setitem` | `obj[key]` / `obj[key] = value` |
| `repr`, `str`, `len`, `bool`, `list`, `sorted` | the built-in function on `obj` |
| `with` | `with obj as name:` runs the inner `body` steps; `raise` raises that exception at the end of the block. Records `{"body": [...], "error": null or "ExceptionName"}` |
| `check` | the class structure, for example `"is": "property"` checks that `cls.attr` is a `property` |

`"save": "x"` stores a step's result under the name `x`. `{"ref": "x"}` inside a value means
that stored object. Copy an example's input into a custom test to debug it.

</details>

---

Select **Python**. Write your classes above the driver line. Do not edit the driver or the
`Solution.run` adapter. **Run** checks the three examples. **Submit** runs all 32 tests.
This is an original practice exercise.

Python documentation: [1](https://docs.python.org/3.11/tutorial/classes.html#class-and-instance-variables)
