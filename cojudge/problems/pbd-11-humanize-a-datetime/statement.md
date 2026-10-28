# 11. Humanize a datetime

[Course list](/?course=pybites-datetimes-timezones) · [Original bite](https://pybitesplatform.com/bites/humanize-a-datetime/)

pretty_date(value, now=NOW) accepts naive datetimes. NOW is fixed at 2019-03-20 12:00. Return "just now" for less than one second; otherwise use whole seconds, minutes, hours, or days with singular/plural and " ago". Use the largest whole unit. At exactly two days return "2 days ago". For older dates return MM/DD/YY. Future dates and non-datetime inputs raise ValueError.

**Source and offline changes:** The premium template and tests are not available in this account. This version uses a recreated template and tests based on the public description.

<details>
<summary>Original public description</summary>

In this Bite you will convert a timedelta object into something readable.

There are modules to do this, but the goal in this Bite is to try to solve it yourself using standard Python.

 - If the date passed into `pretty_date` is <= 2 days ago return the pretty date string, you can use `TIME_OFFSETS` for this

 - If the date passed in is older than that, return the date in the format month/day/year, 2 digits each, e.g. `05/19/18`)

 - If a non `datetime` object is passed into the `pretty_date` function, raise a `ValueError`.

Check out the tests for argument passed into the function -> expected return.

Good luck and keep calm and code in Python!

</details>

Write your implementation at the top of the editor. The tests below it import your code as
`pretty_dates`. **Run** checks the first three tests. **Submit** checks all 10 tests.
A failed test shows its name, error, and test line.

- Python 3.11. Use the standard library. All required data is supplied. No network access.
- Keep the supplied tests and runner. Implement the functions above them.
- For a saved solution, use **+** beside the editor tabs to open the current template in a new tab.
