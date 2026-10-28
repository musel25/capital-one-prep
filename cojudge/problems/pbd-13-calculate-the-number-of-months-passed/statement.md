Some more fun working with dates! In this Bite you will calculate the number of months between the fixed `START_DATE = date(2018, 11, 1)` and the date you will construct from the input arguments.

You should raise the proper `exception`s and perform the proper upper rounding based on the fact that `>= 10 days` in the *datetime difference* adds another month to the counter.

Best to give you some examples of the expected results so check out the docstring and tests, then start coding Python 💪. You probably want to use [`dateutil.relativedelta`](https://dateutil.readthedocs.io/en/stable/) for this one! Good luck!

Use the standard library for this version.

**Constraints:**

- Invalid or earlier dates raise `ValueError`; non-integer date components raise `TypeError`.
