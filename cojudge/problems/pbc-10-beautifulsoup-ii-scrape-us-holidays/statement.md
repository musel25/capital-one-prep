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

**Constraints:**

- Use the supplied BeautifulSoup interface. HTML is well formed. Dates use `YYYY-MM-DD`; the fourth cell contains the holiday name.
