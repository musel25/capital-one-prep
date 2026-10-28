# 10. Beautifulsoup ii - scrape us holidays

[Course list](/?course=pybites-collections) · [Original bite](https://pybitesplatform.com/bites/beautifulsoup-ii-scrape-us-holidays/)

Implement `get_us_bank_holidays(html=HTML)`. Use the supplied BeautifulSoup interface to find the first table with CSS class `list-table`. For each data row, read the `datetime` attribute of its `time` element (YYYY-MM-DD) and the fourth `td` cell as the holiday name. Return a new `defaultdict(list)` mapping two-digit month strings to holiday names in document order. Strip name whitespace. Include every listed holiday, including regional and observance rows. Skip header rows and rows with fewer than four cells or no time element. Return an empty defaultdict when the table is absent. The supplied HTML is well formed, has no nested tables, and all present dates use YYYY-MM-DD.

**Source and offline changes:** This premium exercise uses recreated tests and the original cached holiday table. The judge has no BeautifulSoup package. The template supplies a small standard-library adapter named BeautifulSoup. It supports find/find_all(name, class_=...), get, get_text(strip=...), and text. It is limited to the well-formed HTML in this version.

<details>
<summary>Original public description</summary>

In this Bite we use [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) to scrape US holidays from [OfficeHolidays](https://www.officeholidays.com/countries/usa/index.php) to make a lookup of holidays per month.

Check the HTML ([here](https://bites-data.s3.us-east-2.amazonaws.com/us_holidays.html)) for a `table` with CSS class `list-table` and parse its data. You need to populate the given `holidays defaultdict` like this:

```python
>>> from pprint import pprint as pp
  >>> from holidays import get_us_bank_holidays
  >>> pp(get_us_bank_holidays())
  defaultdict(<class 'list'>,
              {'01': ["New Year's Day", 'Martin Luther King Jr. Day'],
               '02': ["Presidents' Day"],
               '04': ['Emancipation Day'],
               '05': ["Mother's Day", 'Memorial Day'],
               '06': ["Father's Day"],
               '07': ['Independence Day'],
               '09': ['Labor Day'],
               '10': ['Columbus Day'],
               '11': ['Veterans Day', 'Thanksgiving', 'Day after Thanksgiving'],
               '12': ['Christmas Day']})

```

By the way, watch out for trailing spaces when parsing the holidays. Have fun and keep coding in Python!

</details>

Write your implementation at the top of the editor. The tests below it import your code as
`holidays`. **Run** checks the first three tests. **Submit** checks all 5 tests.
A failed test shows its name, error, and test line.

- Python 3.11. Use the standard library. All required data is supplied. No network access.
- Keep the supplied tests and runner. Implement the functions above them.
- For a saved solution, use **+** beside the editor tabs to open the current template in a new tab.
