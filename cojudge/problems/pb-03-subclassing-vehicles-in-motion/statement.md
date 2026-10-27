# 03. Subclassing: Vehicles in Motion

[Course list](/?course=pybites-oop) · Pybites Beginner · [Original bite](https://pybitesplatform.com/bites/subclassing-vehicles-in-motion/)

In this exercise, you’ll practice creating Python subclasses and using `super()` to inherit from a parent class.

Subclassing allows you to build specialized versions of a general blueprint, making your code more organized and reusable.

If you're new to this concept, check out our article: [How to Write a Python Subclass](https://pybit.es/articles/python-subclasses/).

You’ll start with a `Vehicle` base class containing attributes common to all vehicles. From there, you’ll create two subclasses — `Car` and `Motorbike` — each adding their own unique attributes and methods. Both subclasses should still have access to all methods from `Vehicle`.

### Your task

[](https://github.com/pybites/bitesofpy_contrib/blob/main/subclass/exercise.md#your-task)

1.  Implement the `Vehicle` class with `brand`, `model`, and `wheels` attributes, plus a `description()` method that returns: `"<brand> <model> with <wheels> wheels"`, for example: `"Toyota Corolla with 4 wheels"`.

1.  Create a `Car` subclass with an extra `doors` attribute and a `honk()` method returning: `"Beep beep!"`.

1.  Create a `Motorbike` subclass with an extra `engine_cc` attribute and a `rev_engine()` method returning: `"<parent class's description method> goes Vroom vroom!"`, for example: `"Yamaha R3 with 2 wheels goes Vroom vroom!"`

1.  Use `super()` in each subclass’s constructor to initialize the shared attributes.

---

💡 *Tip:* In real-world code, you can make constructor parameters **keyword-only** (e.g., `Motorbike(brand="Yamaha", model="R3", wheels=2, engine_cc=321)`) to avoid mixing up arguments. We’re keeping them positional here for simplicity.

Related exercise: Force keyword arguments

---

By the end, you’ll see how inheritance lets you reuse code across multiple classes while still customizing behavior for specific cases. This is a core principle of object-oriented programming (OOP) and a powerful tool in your Python skill set.

---

For more OOP exercises, check out our OOP track.

**How to solve it here:** write your code at the top of the editor, like the Pybites Code tab.
The Pybites tests are in the editor below your code (the Tests tab). The tests import your code as
the module `vehicles`. **Run** checks the first three tests. **Submit** runs all
8. A failing test shows its name, the error, and the failed test line. The original template and tests are in Pybites premium, so the template and tests here are a recreation that follows the description.

**Constraints:**

- Python 3.11, standard library only. No network access.
- Do not edit the tests or the supplied runner at the bottom of the editor.
