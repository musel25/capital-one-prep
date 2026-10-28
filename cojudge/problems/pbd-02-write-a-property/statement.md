Write a simple `Promo` class. Its constructor receives two variables: `name` (which must be a string) and `expires` (which must be a `datetime` object).

Add a [`property`](https://docs.python.org/3/library/functions.html#property) called `expired` which returns a boolean value indicating whether the promo has expired or not.

Checkout the tests and `datetime` module for more info. Have fun!

**Constraints:**

- Use naive datetimes and the supplied `NOW`; equality is not expired.
- `expired` is read-only and reflects changes to `expires`.
