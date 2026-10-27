# 14. Write a context manager

[Course list](/?course=pybites-oop) · Pybites Advanced · [Original bite](https://pybitesplatform.com/bites/write-a-context-manager/)

Write a [context manager](https://docs.python.org/3/reference/datamodel.html#context-managers) to roll back a transaction on the given `Account` class.

There are two *special (aka *dunder*) methods* you need to define to create a context manager (there is also a convenient decorator - see Write a performance monitoring context manager).

The purpose of the context manager is to roll back any transaction that will make the balance go below 0 (debt != cool).

The rollback should follow [the *Unit of Work *pattern](https://www.cosmicpython.com/book/chapter_06_uow.html), meaning all transactions within a `with` block should be either fully applied or fully discarded, just like a database transaction.

The rest of the class is already defined so you can focus on the context manager part.

See the tests for more detail. Good luck and keep calm and code in Python!

**How to solve it here:** write your code at the top of the editor, like the Pybites Code tab.
The Pybites tests are in the editor below your code (the Tests tab). The tests import your code as
the module `account`. **Run** checks the first three tests. **Submit** runs all
7. A failing test shows its name, the error, and the failed test line. The template and tests are the originals from this free bite.

**Constraints:**

- Python 3.11, standard library only. No network access.
- Do not edit the tests or the supplied runner at the bottom of the editor.
