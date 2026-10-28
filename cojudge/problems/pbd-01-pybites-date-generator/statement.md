# 01. Pybites date generator

[Course list](/?course=pybites-datetimes-timezones) · [Original bite](https://pybitesplatform.com/bites/pybites-date-generator/)

Implement an infinite generator. Its first value is PYBITES_BORN + 100 days. Each later value is 100 days after the previous value. Separate generator objects must keep separate state.

**Source and offline changes:** This version keeps the original free template and tests, with added boundary tests.

<details>
<summary>Original public description</summary>

Write a [*generator*](https://pybit.es/articles/generators/) that yields every 100th day counting forward from the `PYBITES_BORN` date.

Here is how the generator would work if you import and use it in your REPL:

```python
>>> from itertools import islice
>>> from pprint import pprint as pp
>>> from gendates import gen_special_pybites_dates
>>> gen = gen_special_pybites_dates()
>>> pp(list(islice(gen, 5)))
[datetime.datetime(2017, 3, 29, 0, 0),
 datetime.datetime(2017, 7, 7, 0, 0),
 datetime.datetime(2017, 10, 15, 0, 0),
 datetime.datetime(2018, 1, 23, 0, 0),
 datetime.datetime(2018, 5, 3, 0, 0)]
```

**Note:** the tests will take the first 10 dates your generator yields, each exactly 100 days after the previous one.

Keep calm and code in Python, have fun!

**Update** 3rd of Jan 2021: previously we also asked for the PyBites N year marks as well, but this unnecessarily complicated this beginner Bite so simplified the requirements a bit.

</details>

Write your implementation at the top of the editor. The tests below it import your code as
`gendates`. **Run** checks the first three tests. **Submit** checks all 5 tests.
A failed test shows its name, error, and test line.

- Python 3.11. Use the standard library. All required data is supplied. No network access.
- Keep the supplied tests and runner. Implement the functions above them.
- For a saved solution, use **+** beside the editor tabs to open the current template in a new tab.
