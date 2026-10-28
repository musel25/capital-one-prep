# 11. Turn messy csv into json

[Course list](/?course=pybites-data-formats) · [Original bite](https://pybitesplatform.com/bites/turn-messy-csv-into-json/)

Implement `convert_to_json(data=members)`. `data` is a multiline string. The first nonblank line contains comma-separated column names. Each data row can use any mix of comma, pipe (`|`), and semicolon delimiters. Split all three delimiters. Return a JSON string containing a list of dictionaries in row order. Keep all field values as strings, including IDs, leading zeroes, whitespace, and empty fields. Ignore blank lines. Fields are unquoted and cannot contain delimiter characters or newlines. Column names are nonempty and unique. Each data row must have the same number of fields as the header; otherwise raise ValueError. Empty or header-only input returns the JSON representation of an empty list. The local sample has ten records; the first three follow the public example.

**Source and offline changes:** The premium template and tests are not available in this account. This version uses a recreated template and tests based on the public description.

<details>
<summary>Original public description</summary>

At the [1 year mark of our platform](https://twitter.com/pybites/status/943811489537945600) here is Bite 150! In this Bite you are presented with some messed up `csv` (to avoid file IO we pre-loaded it into a multi-line string variable `members`). The first line is the header and can be assumed to only have commas, the 10 data rows though have a mix of `,`, `|` and `;` delimiters.

But no worries, you Python ninjas can do data cleaning for breakfast no?!

Complete `convert_to_json` parsing this output and returning valid `json` like this:

```python
[{"id": "1", "first_name": "Junie", "last_name": "Kybert", "email": "jkybert0@army.mil"},
 {"id": "2", "first_name": "Sid", "last_name": "Churching", "email": "schurching1@tumblr.com"},
 {"id": "3", "first_name": "Cherry", "last_name": "Dudbridge", "email": "cdudbridge2@nifty.com"},
 ... more entries ...
]

```

The tests will check if your output is indeed valid `json` and of course if it contains all data. Good luck!

</details>

Write your implementation at the top of the editor. The tests below it import your code as
`messy_csv`. **Run** checks the first three tests. **Submit** checks all 8 tests.
A failed test shows its name, error, and test line.

- Python 3.11. Use the standard library. All required data is supplied. No network access.
- Keep the supplied tests and runner. Implement the functions above them.
- For a saved solution, use **+** beside the editor tabs to open the current template in a new tab.
