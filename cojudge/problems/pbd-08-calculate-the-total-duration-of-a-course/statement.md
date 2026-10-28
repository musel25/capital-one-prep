# 08. Calculate the total duration of a course

[Course list](/?course=pybites-datetimes-timezones) · [Original bite](https://pybitesplatform.com/bites/calculate-the-total-duration-of-a-course/)

get_total_duration(text) reads one video per nonblank line. A line ends in MM:SS with an optional title before it. Minutes can exceed 59; seconds must be 00-59. Return HH:MM:SS with at least two hour digits. Empty input returns 00:00:00. Invalid lines raise ValueError.

**Source and offline changes:** The premium template and tests are not available in this account. This version uses a recreated template and tests based on the public description.

<details>
<summary>Original public description</summary>

In this Bite you read in a text file with course times (*MM:SS*) per video.

You extract these and calculate the total course duration in *HH:MM:SS*.

See the *docstrings* and tests for more details.

Have fun and we hope you learn a thing or two.

> Trivia: in honor of our [Code Challenges Pilot](https://pybit.es/articles/js_time_scraper_ch/): this was the exercise we used to test the waters when we started out :)

</details>

Write your implementation at the top of the editor. The tests below it import your code as
`course_duration`. **Run** checks the first three tests. **Submit** checks all 6 tests.
A failed test shows its name, error, and test line.

- Python 3.11. Use the standard library. All required data is supplied. No network access.
- Keep the supplied tests and runner. Implement the functions above them.
- For a saved solution, use **+** beside the editor tabs to open the current template in a new tab.
