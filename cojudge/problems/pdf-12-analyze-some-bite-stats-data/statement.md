# 12. Analyze some bite stats data

[Course list](/?course=pybites-data-formats) · [Original bite](https://pybitesplatform.com/bites/analyze-some-bite-stats-data/)

Implement `BiteStats(data=LOG_DATA)`. `data` is CSV text with columns `bite,user,completed`. Read it with csv.DictReader and store the list of string dictionaries in `self.rows`. Bite IDs are positive integer strings. User names are nonempty strings. The completed field is exactly `True` or `False`. Implement six read-only properties. `total_attempts` counts all rows. `total_users` counts distinct user names. `total_bites` counts distinct bite IDs. `total_completed` counts rows whose completed field is `True`. Each row is one attempt, so repeated attempts and repeated completions count. `most_active_user` returns the name with the most rows; ties use alphabetical order. `most_popular_bite` returns the integer bite ID with the most rows; ties use the smallest integer ID. Header-only data has all four counts equal to zero and both most-popular values equal to None. Do not change self.rows when reading properties. The public description does not list the original six property names; these six statistics define this recreation.

**Source and offline changes:** The premium template and tests are not available in this account. This version uses a recreated template and tests based on the public description.

<details>
<summary>Original public description</summary>

In this Bite we will look at some Bite stats logs (usernames have been anonymized!):

```python
$ head -5 bite_output_log.txt
bite,user,completed
102,ofancourt1,False
101,ofancourt1,False
29,emilham4,False
9,mfilshin6,False

```

Load in the data using `csv`'s awesome `DictReader` storing the result in `self.rows` in the constructor (`__init__`). Next finish the 6 defined `@property` methods using the loaded in data. Each `property` returns a single value. Check out the docstrings and tests for more info.

Good luck and keep calm and code in Python!

</details>

Write your implementation at the top of the editor. The tests below it import your code as
`bite_stats`. **Run** checks the first three tests. **Submit** checks all 8 tests.
A failed test shows its name, error, and test line.

- Python 3.11. Use the standard library. All required data is supplied. No network access.
- Keep the supplied tests and runner. Implement the functions above them.
- For a saved solution, use **+** beside the editor tabs to open the current template in a new tab.
