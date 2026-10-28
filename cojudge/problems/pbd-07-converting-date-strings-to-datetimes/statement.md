# 07. Converting date strings to datetimes

[Course list](/?course=pybites-datetimes-timezones) · [Original bite](https://pybitesplatform.com/bites/converting-date-strings-to-datetimes/)

convert_to_datetime parses strings such as Thu, 04 May 2017 20:46:00 +0200. Return the naive local datetime without timezone conversion. get_month_most_posts accepts datetimes and returns YYYY-MM; ties select the earliest month. Empty input raises ValueError.

**Source and offline changes:** The premium template and tests are not available in this account. This version uses a recreated template and tests based on the public description.

<details>
<summary>Original public description</summary>

In this Bite you are provided with a list of publish dates of all our PyBites blog posts. They are in this format: *Thu, 04 May 2017 20:46:00 +0200*.

Write a function called `convert_to_datetime` that takes a date string and convert it to a `datetime` object. You can leave the timezone part (e.g. *+0200*) off.

Secondly complete the `get_month_most_posts` function: it should take a list of `datetime` objects and return the month that we posted the most. You should get **2017-01**. See also the *TESTS* tab how your code will be tested.

Have fun and let us know how you experienced this Bite. Have fun!

</details>

Write your implementation at the top of the editor. The tests below it import your code as
`publish_dates`. **Run** checks the first three tests. **Submit** checks all 6 tests.
A failed test shows its name, error, and test line.

- Python 3.11. Use the standard library. All required data is supplied. No network access.
- Keep the supplied tests and runner. Implement the functions above them.
- For a saved solution, use **+** beside the editor tabs to open the current template in a new tab.
