# 13. Enrich a class with dunder methods

[Course list](/?course=pybites-oop) · Pybites Advanced · [Original bite](https://pybitesplatform.com/bites/enrich-a-class-with-dunder-methods/)

Let's enrich an *Account* class by adding *dunder* (aka special) methods to support the following:

1. length of the object: `len(acc)` returns the number of transactions
1. account comparison: `acc1 >,<,>=.<=,== acc2` returns a boolean comparing account balances
1. indexing: `acc[n]` shows the nth transaction on`account` (0 based)
1. iteration: `list(acc)` returns a sequence of account transactions
1. operator overloading: `acc + int` and `acc - int` can be used to add/subtract money (if given incompatible types for these operations, raise a `TypeError` - **note **that previously this was a `ValueError`, but former is more correct for this scenario)
1. string representation: `str(acc)` returns *NAME account - balance: INT*

The provided template already does some setup for you.

Check out the tests for more specifics. If you're still new to dunder (magic) methods, [here is an article](https://dbader.org/blog/python-dunder-methods) you might find useful. Good luck!

**How to solve it here:** write your code at the top of the editor, like the Pybites Code tab.
The Pybites tests are in the editor below your code (the Tests tab). The tests import your code as
the module `account`. **Run** checks the first three tests. **Submit** runs all
10. A failing test shows its name, the error, and the failed test line. The original template and tests are in Pybites premium, so the template and tests here are a recreation that follows the description.

**Constraints:**

- Python 3.11, standard library only. No network access.
- Do not edit the tests or the supplied runner at the bottom of the editor.
