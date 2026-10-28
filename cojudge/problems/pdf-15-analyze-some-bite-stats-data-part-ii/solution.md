## Reference solution

Paste this code above the supplied tests and runner.

```python
import csv
import io

BITE_STATS = """Bite;Difficulty
Bite 1. Sum n numbers;3.45
Bite 2. Regex Fun;4.89
Bite 3. Word Values;3.97
Bite 4. Top 10 PyBites tags;4.72
Bite 5. Parse a list of names;4.48
Bite 6. PyBites Die Hard;6.8
Bite 7. Parsing dates from logs;5.76
Bite 8. Rotate string characters;3.5
Bite 9. Palindromes;4.71
Bite 200. Minecraft Enchantable Items;None
"""


def get_most_complex_bites(csv_file=None, n=10):
    if n < 0:
        raise ValueError('n must be nonnegative')
    if n == 0:
        return []
    if csv_file is None:
        text = BITE_STATS
    else:
        with open(csv_file, encoding='utf-8-sig', newline='') as handle:
            text = handle.read()
    result = []
    for row in csv.DictReader(io.StringIO(text), delimiter=';'):
        score = row['Difficulty'].strip()
        if score in ('', 'None'):
            continue
        result.append((row['Bite'].strip(), float(score)))
    return sorted(result, key=lambda item: -item[1])[:n]
```
