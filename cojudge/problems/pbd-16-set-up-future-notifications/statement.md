# 16. Set up future notifications

[Course list](/?course=pybites-datetimes-timezones) · [Original bite](https://pybitesplatform.com/bites/set-up-future-notifications/)

add_todo(duration, description, start_time=NOW) returns "description @ YYYY-MM-DD HH:MM:SS". NOW is 2019-02-06 22:00. duration contains space-separated nonnegative integer tokens with suffix d, h, m, or s. Accept repeated units and any order. Reject empty strings, unknown units, negative values, and malformed tokens with ValueError.

**Source and offline changes:** The premium template and tests are not available in this account. This version uses a recreated template and tests based on the public description.

<details>
<summary>Original public description</summary>

Let's do another `datetime` processing Bite. Complete `add_todo` below that converts time units to future timestamps.

Here is how it works with given default `start_time` of `NOW`:

```python
>>> from timer import add_todo, NOW
>>> str(NOW)
'2019-02-06 22:00:00'
>>> add_todo("11h 10m", "Wash my car")
'Wash my car @ 2019-02-07 09:10:00'
>>> add_todo("30d", "Code a Bite")
'Code a Bite @ 2019-03-08 22:00:00'
>>> add_todo("5m 3s", "Go to Bed")
'Go to Bed @ 2019-02-06 22:05:03'

```

See the *docstring* and tests for more output examples. Good luck and code more Python!

</details>

Write your implementation at the top of the editor. The tests below it import your code as
`timer`. **Run** checks the first three tests. **Submit** checks all 8 tests.
A failed test shows its name, error, and test line.

- Python 3.11. Use the standard library. All required data is supplied. No network access.
- Keep the supplied tests and runner. Implement the functions above them.
- For a saved solution, use **+** beside the editor tabs to open the current template in a new tab.
