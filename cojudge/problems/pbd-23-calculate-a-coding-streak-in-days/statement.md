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

**Constraints:**

- Keep duplicate dates when extracting; count unique dates for the streak and ignore future dates.
