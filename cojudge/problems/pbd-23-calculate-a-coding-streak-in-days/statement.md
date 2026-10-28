# 23. Calculate a coding streak in days

[Course list](/?course=pybites-datetimes-timezones) · [Original bite](https://pybitesplatform.com/bites/calculate-a-coding-streak-in-days/)

extract_dates(text) returns a list of date objects from pipe-table rows whose first cell is YYYY-MM-DD. Ignore headers and borders. Keep duplicates and input order. Invalid ISO-shaped dates raise ValueError. calculate_streak(dates, today=TODAY) returns consecutive unique coding days ending today, or yesterday if today is absent. If both are absent, return 0. Ignore future dates. TODAY is fixed at date(2018, 11, 12).

**Source and offline changes:** The premium template and tests are not available in this account. This version uses a recreated template and tests based on the public description.

<details>
<summary>Original public description</summary>

In this Bite you are going to calculate the amount of days you are on a coding streak (consecutive days coded. You are presented with this DB table like output of date/activity/count:

```python
data = """
    +------------+------------+---------+
    | date       | activity   | count   |
    |------------+------------+---------|
    | 2018-11-11 | pcc        | 1       |
    | 2018-11-10 | 100d       | 1       |
    | 2018-11-09 | 100d       | 2       |
    | 2018-10-23 | pcc        | 1       |
    | 2018-10-15 | pcc        | 1       |
    | 2018-10-05 | bite       | 1       |
    | 2018-09-21 | bite       | 4       |
    | 2018-09-18 | bite       | 2       |
    | 2018-09-18 | bite       | 4       |
    +------------+------------+---------+
"""
```

Here is what you need to do:

- Complete `extract_dates` to extract `date` (not `datetime`) objects.
- Complete `calculate_streak` that takes those `date` objects and returns the streak in (`int`) days.
- Calculate back from `TODAY` that is set to `date(2018, 11, 12)`. Note that a streak can be > 0 if today or yesterday is in the date range. This is because we don't assume *today* to be over yet, so if yesterday was coded that is a valid continuation of a streak. If today was coded that counts towards the streak too of course.

Have fun and keep calm and code in Python. Join our Circle community to learn and share more Python with other passionate Pythonistas.

</details>

Write your implementation at the top of the editor. The tests below it import your code as
`coding_streak`. **Run** checks the first three tests. **Submit** checks all 9 tests.
A failed test shows its name, error, and test line.

- Python 3.11. Use the standard library. All required data is supplied. No network access.
- Keep the supplied tests and runner. Implement the functions above them.
- For a saved solution, use **+** beside the editor tabs to open the current template in a new tab.
