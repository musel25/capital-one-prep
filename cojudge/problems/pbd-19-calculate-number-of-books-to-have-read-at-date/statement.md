# 19. Calculate number of books to have read at date ...

[Course list](/?course=pybites-datetimes-timezones) · [Original bite](https://pybitesplatform.com/bites/calculate-number-of-books-to-have-read-at-date/)

get_number_books_read(goal, at_date=NOW) returns int(round(ISO_week / 52 * goal)); Python round uses ties to even. goal must be a positive integer. NOW is fixed at date(2019, 1, 1). Reject dates before NOW. Accept date objects, ISO YYYY-MM-DD, M-D-YYYY, and strings like "Sunday, March 25th, 2019". For the last form, ignore the weekday text and remove ordinal suffixes. Bad goals or dates raise ValueError. Week 53 is allowed and can exceed the annual goal. WEEKS_PER_YEAR is 52.

**Source and offline changes:** The premium template and tests are not available in this account. This version uses a recreated template and tests based on the public description.

<details>
<summary>Original public description</summary>

For this Bite you are asked to start working on a reading goal feature for a books app.

Code up `get_number_books_read` that takes a yearly # books to read `int` and then calculates the amount of books user should have read based on the `at_date` argument which defaults to `NOW`.

So if the goal is 52, and we call this function week 11, it should return 11. If the goal is 100 and we call this function in week 47 the function should return 90 (47/52*100), rounding to `int`.

Some more examples:

```python
>>> get_number_books_read(100, 'Sunday, March 25th, 2019')
25
>>> get_number_books_read(52, 'Sunday, March 18th, 2019')
12
>>> get_number_books_read(52, '5-20-2018')
Traceback (most recent call last):
  File "", line 1, in
  File "/Users/bbelderbos/code/bitesofpy/186/books.py", line 20, in get_number_books_read
    raise ValueError('Should have positive goal and future date')
ValueError: Should have positive goal and future date

```

Check the docstring, comments and tests for more guidance.

For simplicity you can assume that a year has 52 weeks (hence `WEEKS_PER_YEAR = 52`).

**Hint**: to get the week of the year, look into [`isocalendar`](https://docs.python.org/3/library/datetime.html#datetime.date.isocalendar).

Keep calm and code in Python! 🐍 🔥

</details>

Write your implementation at the top of the editor. The tests below it import your code as
`books`. **Run** checks the first three tests. **Submit** checks all 10 tests.
A failed test shows its name, error, and test line.

- Python 3.11. Use the standard library. All required data is supplied. No network access.
- Keep the supplied tests and runner. Implement the functions above them.
- For a saved solution, use **+** beside the editor tabs to open the current template in a new tab.
