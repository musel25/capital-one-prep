# 02. Write a property

[Course list](/?course=pybites-datetimes-timezones) · [Original bite](https://pybitesplatform.com/bites/write-a-property/)

name is a string, including an empty string. expires is a naive datetime. Store both values. The read-only expired property returns a bool on each access: expires < the module's NOW. Equality is not expired. Changes to expires take effect on the next access. Other input types and timezone-aware datetimes are outside the contract; no validation is required for them.

**Source and offline changes:** This version keeps the original free template and tests, with added boundary tests.

<details>
<summary>Original public description</summary>

Write a simple `Promo` class. Its constructor receives two variables: `name` (which must be a string) and `expires` (which must be a `datetime` object).

Add a [`property`](https://docs.python.org/3/library/functions.html#property) called `expired` which returns a boolean value indicating whether the promo has expired or not.

Checkout the tests and `datetime` module for more info. Have fun!

</details>

Write your implementation at the top of the editor. The tests below it import your code as
`simple_property`. **Run** checks the first three tests. **Submit** checks all 8 tests.
A failed test shows its name, error, and test line.

- Python 3.11. Use the standard library. All required data is supplied. No network access.
- Keep the supplied tests and runner. Implement the functions above them.
- For a saved solution, use **+** beside the editor tabs to open the current template in a new tab.
