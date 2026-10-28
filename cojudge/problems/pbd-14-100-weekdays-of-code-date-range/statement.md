# 14. 100 weekdays of code date range

[Course list](/?course=pybites-datetimes-timezones) · [Original bite](https://pybitesplatform.com/bites/100-weekdays-of-code-date-range/)

get_hundred_weekdays(start_date=TODAY) returns a list of exactly 100 date objects, in ascending order. Include start_date if it is Monday-Friday; otherwise begin the next Monday. Skip Saturdays and Sundays. TODAY is fixed at date(2019, 1, 1). No holiday filtering. Use the standard library.

**Source and offline changes:** The premium template and tests are not available in this account. This version uses a recreated template and tests based on the public description.

<details>
<summary>Original public description</summary>

Doing a [#100DaysOfCode can be challenging](https://talkpython.fm/episodes/show/140/level-up-your-python-with-100daysofcode-challenge), and some of it is because you dedicate to do it on workdays AND during weekends.

PyBites coding to the rescue. In this Bite you plan your next 100 days **excluding** weekends.

Complete `get_hundred_weekdays` that takes a `start_date` which defaults to the `TODAY` constant.

Read up on the awesome `dateutil` module and try to use it to generate a list of 100 **weekdays** from `start_date`. By completion you would have a cool new snippet for your coding arsenal :) - good luck and enjoy the ride!

</details>

Write your implementation at the top of the editor. The tests below it import your code as
`weekdays`. **Run** checks the first three tests. **Submit** checks all 8 tests.
A failed test shows its name, error, and test line.

- Python 3.11. Use the standard library. All required data is supplied. No network access.
- Keep the supplied tests and runner. Implement the functions above them.
- For a saved solution, use **+** beside the editor tabs to open the current template in a new tab.
