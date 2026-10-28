# 06. Subclass the dict built-in

[Course list](/?course=pybites-oop) · Pybites Intermediate · [Original bite](https://pybitesplatform.com/bites/subclass-the-dict-built-in/)

**Inputs and required behavior for this version:**

Use string name keys and datetime.date birthday values. Each assigned name is new to this dictionary. Empty dictionaries and February 29 birthdays are valid. Store every entry. Before adding it, compare its month and day with the stored birthdays, ignoring the year. Print MSG.format(name) followed by one newline if any match exists, once per added name. Otherwise print nothing. Construction and update must apply the same rule. Existing-key replacement, datetime values and other input types are outside the contract; no validation is required for them. Instances keep separate entries.

<details>
<summary>Original bite description</summary>

In this Bite, you will subclass `UserDict` from `collections` to support a birthday dictionary.

This dictionary takes names as *keys* and birthday `date`s as *values*. Implement the `__setitem__` *dunder method* to print a message every time somebody gets added with a birthday that is already in the dictionary. It should work like this when running it in the REPL:

```python
>>> from datetime import date
  >>> from bdaydict import BirthdayDict
  >>> bd = BirthdayDict()
  >>> bd['bob'] = date(1987, 6, 15)
  >>> bd['tim'] = date(1984, 7, 15)
  >>> bd['mary'] = date(1987, 6, 15)  # whole date match
  Hey mary, there are more people with your birthday!
  >>> bd['sara'] = date(1987, 6, 14)
  >>> bd['mike'] = date(1981, 7, 15)  # day + month match
  Hey mike, there are more people with your birthday!

```

So if **day and month** are the same, you have a match; the **year can be different**. Use `MSG` to print the message, replacing `{}` with the name key of the newly added person.

Note that this exercise is meant to get you thinking about **subclasses and extending built-in behavior**. Instead of subclassing `dict` directly, we use `UserDict`, which provides better flexibility and ensures that overridden methods behave consistently.

Good luck and have fun!

</details>

**How to solve it here:** write your code at the top of the editor, like the Pybites Code tab.
The Pybites tests are in the editor below your code (the Tests tab). The tests import your code as
the module `bdaydict`. **Run** checks the first three tests. **Submit** runs all
10. A failing test shows its name, the error, and the failed test line. The original template and tests are in Pybites premium, so the template and tests here are a recreation that follows the description.

**Constraints:**

- Python 3.11, standard library only. No network access.
- Do not edit the tests or the supplied runner at the bottom of the editor.
- For an older saved solution, use **+** beside the editor tabs to open the current template in a new tab. Copy your implementation into that tab. This keeps the saved solution and gives you the current tests.
