# 04. Work with datetime's strptime and strftime

[Course list](/?course=pybites-datetimes-timezones) · [Original bite](https://pybitesplatform.com/bites/work-with-datetimes-strptime-and-strftime/)

years_ago(date_string, reference=date(2018, 8, 1)) returns completed anniversaries since an ISO YYYY-MM-DD date. Reject future dates. convert_eu_to_us_date converts DD/MM/YYYY to MM/DD/YYYY. Invalid dates raise ValueError.

**Source and offline changes:** The premium template and tests are not available in this account. This version uses a recreated template and tests based on the public description.

<details>
<summary>Original public description</summary>

In this Bite you get some more practice with `datetime`'s useful `strptime` and `stftime`.

Complete the two functions: `years_ago` and `convert_eu_to_us_date` following the instructions in their *docstrings*.

This is the definition and difference between the two:

- `strptime`: *parse (convert) string to datetime object.*
- `strftime`: *create formatted string for given time/date/datetime object according to specified format.*

Reference: [8.1.8. strftime() and strptime() Behavior](https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior). Good luck and keep calm and code in Python!

</details>

Write your implementation at the top of the editor. The tests below it import your code as
`format_dates`. **Run** checks the first three tests. **Submit** checks all 6 tests.
A failed test shows its name, error, and test line.

- Python 3.11. Use the standard library. All required data is supplied. No network access.
- Keep the supplied tests and runner. Implement the functions above them.
- For a saved solution, use **+** beside the editor tabs to open the current template in a new tab.
