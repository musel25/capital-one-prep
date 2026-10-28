# 13. Calculate the number of months passed

[Course list](/?course=pybites-datetimes-timezones) · [Original bite](https://pybitesplatform.com/bites/calculate-the-number-of-months-passed/)

START_DATE is date(2018, 11, 1). get_months_passed(year, month, day) constructs an end date and returns completed calendar months plus one if the remaining days are at least 10. Dates before START_DATE and invalid calendar dates raise ValueError. Non-integer date components raise TypeError. Use the standard library.

**Source and offline changes:** The premium template and tests are not available in this account. This version uses a recreated template and tests based on the public description.

<details>
<summary>Original public description</summary>

Some more fun working with dates! In this Bite you will calculate the number of months between the fixed `START_DATE = date(2018, 11, 1)` and the date you will construct from the input arguments.

You should raise the proper `exception`s and perform the proper upper rounding based on the fact that `>= 10 days` in the *datetime difference* adds another month to the counter.

Best to give you some examples of the expected results so check out the docstring and tests, then start coding Python 💪. You probably want to use [`dateutil.relativedelta`](https://dateutil.readthedocs.io/en/stable/) for this one! Good luck!

</details>

Write your implementation at the top of the editor. The tests below it import your code as
`months_passed`. **Run** checks the first three tests. **Submit** checks all 7 tests.
A failed test shows its name, error, and test line.

- Python 3.11. Use the standard library. All required data is supplied. No network access.
- Keep the supplied tests and runner. Implement the functions above them.
- For a saved solution, use **+** beside the editor tabs to open the current template in a new tab.
