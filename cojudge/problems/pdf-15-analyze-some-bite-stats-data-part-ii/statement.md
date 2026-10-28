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

The supplied CSV sample replaces the download.

**Constraints:**

- Return `(title, float_score)` tuples; skip blank or `None` scores, preserve ties, and return at most `n` results.
- Negative `n` raises `ValueError`; support UTF-8 BOM files.
