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

**Constraints:**

- Accept `date` objects, ISO dates, M-D-YYYY, or the displayed English date format; reject invalid dates or goals.
- Use Python `round`; a date before the supplied `NOW` raises `ValueError`.
