In this Bite you will convert a timedelta object into something readable.

There are modules to do this, but the goal in this Bite is to try to solve it yourself using standard Python.

 - If the date passed into `pretty_date` is <= 2 days ago return the pretty date string, you can use `TIME_OFFSETS` for this

 - If the date passed in is older than that, return the date in the format month/day/year, 2 digits each, e.g. `05/19/18`)

 - If a non `datetime` object is passed into the `pretty_date` function, raise a `ValueError`.

Check out the tests for argument passed into the function -> expected return.

Good luck and keep calm and code in Python!

**Constraints:**

- Use the supplied `NOW`; future datetimes raise `ValueError`.
