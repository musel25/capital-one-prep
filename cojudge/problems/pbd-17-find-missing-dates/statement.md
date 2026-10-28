# 17. Find missing dates

[Course list](/?course=pybites-datetimes-timezones) · [Original bite](https://pybitesplatform.com/bites/find-missing-dates/)

Keep the source spelling: get_misssing_dates(dates) returns a set of missing date objects strictly between the minimum and maximum supplied dates. Accept unordered values and duplicates. Empty and singleton sequences return an empty set.

**Source and offline changes:** The premium template and tests are not available in this account. This version uses a recreated template and tests based on the public description.

<details>
<summary>Original public description</summary>

Complete `get_misssing_dates` that takes an (unordered) sequence of `datetime.date` objects. It should determine what the start and end date of this sequence is and return the missing dates.

Here is an example (horizontal scroll code below):

```python
>>> from datetime import date
>>> from missing_dates import get_misssing_dates
>>> date_range = [date(year=2019, month=2, day=n) for n in range(1, 11, 2)]
>>> date_range
[datetime.date(2019, 2, 1), datetime.date(2019, 2, 3), datetime.date(2019, 2, 5), datetime.date(2019, 2, 7), datetime.date(2019, 2, 9)]

# our function returns the missing dates
# = the ones that were not generated in the preceding code
>>> sorted(get_misssing_dates(date_range))
[datetime.date(2019, 2, 2), datetime.date(2019, 2, 4), datetime.date(2019, 2, 6), datetime.date(2019, 2, 8)]

```

Some modules make this fairly easy (hint hint).

Thanks [@shravankumar147](https://twitter.com/shravankumar147) for sharing [this idea on Twitter](https://twitter.com/shravankumar147/status/1097119970482372611) last week :)

Good luck and keep calm and code in Python!

</details>

Write your implementation at the top of the editor. The tests below it import your code as
`missing_dates`. **Run** checks the first three tests. **Submit** checks all 6 tests.
A failed test shows its name, error, and test line.

- Python 3.11. Use the standard library. All required data is supplied. No network access.
- Keep the supplied tests and runner. Implement the functions above them.
- For a saved solution, use **+** beside the editor tabs to open the current template in a new tab.
