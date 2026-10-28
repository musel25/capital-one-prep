# 15. Analyze some bite stats data - part ii

[Course list](/?course=pybites-data-formats) · [Original bite](https://pybitesplatform.com/bites/analyze-some-bite-stats-data-part-ii/)

Implement `get_most_complex_bites(csv_file=None, n=10)`. Read a semicolon-separated UTF-8 CSV with headers `Bite;Difficulty`. `csv_file` is a local string or pathlib path. When it is None, parse the supplied `BITE_STATS` text instead. Support a UTF-8 byte order mark (BOM) at the start of a file. Return at most `n` `(bite_title, difficulty)` tuples, ordered by numeric difficulty descending. Keep source order for equal scores. Convert difficulty to float. Strip surrounding whitespace from the title and difficulty. Ignore blank difficulty values and the exact text `None`. Zero is a valid score. `n` is an integer; a negative n raises ValueError and zero returns an empty list. An empty dataset returns an empty list. Other nonnumeric difficulty values raise ValueError. The CSV has both named columns and can contain quoted fields. Do not change the source file.

**Source and offline changes:** The premium template and tests are not available in this account. This version uses a recreated template and tests based on the public description.

The premium docstring and tests are unavailable. This version states its return shape, tie rule, and limit behavior explicitly. Its small local CSV uses the public description sample instead of a download.

<details>
<summary>Original public description</summary>

In this Bite you will analyze complexity levels of our first 200 Bites of Py exercises.

We loaded [this CSV file](https://bites-data.s3.us-east-2.amazonaws.com/bite_levels.csv) with some stats that look like this:

```python
  $ head bite_levels.csv
Bite;Difficulty
Bite 1. Sum n numbers;3.45
Bite 2. Regex Fun;4.89
Bite 3. Word Values;3.97
Bite 4. Top 10 PyBites tags;4.72
Bite 5. Parse a list of names;4.48
Bite 6. PyBites Die Hard;6.8
Bite 7. Parsing dates from logs;5.76
Bite 8. Rotate string characters;3.5
Bite 9. Palindromes;4.71
...
...
Bite 200. 🥳 Minecraft Enchantable Items;None

```

The last column shows the average complexity score if available, if not it shows `None`.

Complete the `get_most_complex_bites` function below following its *docstring*.

Your code will be tested calling your function with different arguments.

Update: some folks reported hitting a [UTF-8 BOM error](https://www.howtosolutions.net/2019/04/python-fixing-unexpected-utf-8-bom-error-when-loading-json-data/). In that case use `encoding="utf-8-sig"` when opening the csv file.

Have fun and keep calm and code in Python!

</details>

Write your implementation at the top of the editor. The tests below it import your code as
`bite_stats`. **Run** checks the first three tests. **Submit** checks all 7 tests.
A failed test shows its name, error, and test line.

- Python 3.11. Use the standard library. All required data is supplied. No network access.
- Keep the supplied tests and runner. Implement the functions above them.
- For a saved solution, use **+** beside the editor tabs to open the current template in a new tab.
