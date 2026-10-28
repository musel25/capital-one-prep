# 07. Parse a csv file and create a bar chart

[Course list](/?course=pybites-data-formats) · [Original bite](https://pybitesplatform.com/bites/parse-a-csv-file-and-create-a-bar-chart/)

Implement `create_bar_chart(data=DATA)`. Input is CSV text with a `timezone` header and optional other columns. Use CSV parsing to count each nonempty timezone after stripping surrounding whitespace. Ignore empty timezones and blank lines. Print one line per distinct timezone in ascending string order. The line is `timezone left-aligned | plus signs`, with one `+` per record. Use a timezone column width of max(20, longest timezone length), then one space, `|`, one space, and the bar. End each line with a newline. Print nothing for header-only or all-empty input. Return `None`. CSV data has a header even when it has no records.

**Source and offline changes:** The premium template and tests are not available in this account. This version uses a recreated template and tests based on the public description.

The premium template and tests are recreated. Local CSV text replaces the requests download. This version supplies the function name, header, column width, sorting, and empty-record rules because the public description does not expose the original template or full expected chart.

<details>
<summary>Original public description</summary>

*Update 2026: original Bite text left intact. We no longer have a Slack (nor Circle) community, but that does not affect doing this exercise.*

We played a bit with the Slack API the other day and wow: our Pybites community is super international! We really enjoy connecting with Pythonistas from all over the globe.

We put some anonymized data in a csv (using `uuid4` and `faker`) and for this Bite we ask you to use `requests` to load it in, use the `csv` module to parse it into a data structure of your choice, and finally **print** the following output to the screen:

```python
Africa/Algiers       | ++
Africa/Cairo         | +
Africa/Monrovia      | +
Africa/Nairobi       | ++++
...
...
Europe/Moscow        | ++
Europe/Warsaw        | ++
Pacific/Honolulu     | +

```

See the full output under the TESTS tab. Good luck and remember: keep calm and code in Python!

</details>

Write your implementation at the top of the editor. The tests below it import your code as
`timezone_chart`. **Run** checks the first three tests. **Submit** checks all 7 tests.
A failed test shows its name, error, and test line.

- Python 3.11. Use the standard library. All required data is supplied. No network access.
- Keep the supplied tests and runner. Implement the functions above them.
- For a saved solution, use **+** beside the editor tabs to open the current template in a new tab.
