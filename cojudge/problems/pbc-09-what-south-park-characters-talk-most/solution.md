## Reference solution

Paste this code above the supplied tests and runner.

```python
import csv
import io
from collections import Counter, defaultdict

DATA = 'Season,Episode,Character,Line\n1,1,Cartman,Hello there\n1,1,Stan,Hey\n1,2,Cartman,One two three\n1,1,Cartman,Again\n'

# FOCUS: write the grouping by hand with the collections type named in the task.
# SUPPLIED: _rows reads the CSV text. It is not the skill of this exercise.
#        Use it. Do not edit it.


def _rows(data):
    """Yield one dict per CSV record, keyed by the header names. Blank lines are skipped."""
    return csv.DictReader(io.StringIO(data))


def get_num_words_spoken_by_character_per_episode(data=DATA):
    counts = defaultdict(Counter)
    for row in _rows(data):
        counts[row['Character']][row['Episode']] += len(row['Line'].split())
    return counts
```
