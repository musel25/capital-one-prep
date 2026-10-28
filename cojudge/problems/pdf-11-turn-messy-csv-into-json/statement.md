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

**Constraints:**

- Fields are unquoted and contain no delimiters; preserve string values and empty fields.
- Ignore blank lines; a row with the wrong field count raises `ValueError`.
