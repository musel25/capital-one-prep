# 12. Primitive date format inferrer

[Course list](/?course=pybites-datetimes-timezones) · [Original bite](https://pybitesplatform.com/bites/primitive-date-format-inferrer/)

DateFormat is an Enum of allowed strptime patterns. get_dates(values) counts every pattern that can parse each string. An ambiguous string votes for each matching pattern. A value that matches none votes once for nonparsable. Choose the unique most frequent pattern; reject empty input, a pattern tie, or a nonparsable count greater than the winning pattern count with InfDateFmtError. Parse all values with the winning pattern into YYYY-MM-DD, using "Invalid" for failures. Read the current DateFormat dynamically; tests can replace it.

**Source and offline changes:** The premium template and tests are not available in this account. This version uses a recreated template and tests based on the public description.

<details>
<summary>Original public description</summary>

Complete the `get_dates` method given the following:

- a listing of date strings in unknown date format and
- an `enum` class which contains allowed/supported date formats

Although the following assignment text is wordy, once you will see test cases the task definition will become clearer.

The `get_dates` method will return a list of date strings in the format *yyyy-mm-dd*.

The date format of input date strings will be inferred based on the most prevalent allowed date format of items in the list. Allowed/supported date formats are defined in an `enum` class.

The most prevalent allowed date format of items must represent a single most frequent date format. If there are two most frequent formats with the same frequency raise a (custom) `InfDateFmtError` exception.

Items in an input list can be in any format no matter whether or not this format is listed in the DateFormat `enum` class. Items can be even values which cannot represent a date at all. Those items are nonparsable. If the frequency of nonparsable elements is higher than the frequency of other allowed date formats (counted individually for each format) raise a custom `InfDateFmtError` exception.

Once you have the most prevalent date format, parse dates in an input list and return them as a list of strings in the format *yyyy-mm-dd*.

Dates which are not parsable replace with the string *Invalid*.

**Important note**: the list of allowed/supported date formats is supposed to be stored in the `DateFormat enum` class only. The `DateFormat enum` class is subject of change and this change is not under your control.

As a hint, you are provided with a helper method `_maybe_DFs` which shows how to work with the `DateFormat enum` class.

This assignment introduces a very simple date format inferrer. For more serious work you can check out: [`dateparser`](https://dateparser.readthedocs.io) or [`dateinfer`](https://github.com/jeffreystarr/dateinfer)

</details>

Write your implementation at the top of the editor. The tests below it import your code as
`date_inferrer`. **Run** checks the first three tests. **Submit** checks all 8 tests.
A failed test shows its name, error, and test line.

- Python 3.11. Use the standard library. All required data is supplied. No network access.
- Keep the supplied tests and runner. Implement the functions above them.
- For a saved solution, use **+** beside the editor tabs to open the current template in a new tab.
