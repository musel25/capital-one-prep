In this Bite you get some more practice with `datetime`'s useful `strptime` and `stftime`.

Complete the two functions: `years_ago` and `convert_eu_to_us_date` following the instructions in their *docstrings*.

This is the definition and difference between the two:

- `strptime`: *parse (convert) string to datetime object.*
- `strftime`: *create formatted string for given time/date/datetime object according to specified format.*

Reference: [8.1.8. strftime() and strptime() Behavior](https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior). Good luck and keep calm and code in Python!

**Constraints:**

- `years_ago` counts completed anniversaries from an ISO date to `reference` (default: 2018-08-01).
- `convert_eu_to_us_date` converts DD/MM/YYYY to MM/DD/YYYY; invalid or future birth dates raise `ValueError`.
