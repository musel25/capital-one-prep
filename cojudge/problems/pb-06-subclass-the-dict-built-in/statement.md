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

**Constraints:**

- Each assigned name is new. Birthday values are `datetime.date` objects.
