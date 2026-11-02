## Reference solution

Paste this code above the supplied tests and runner.

```python
import csv
from collections import Counter
from io import StringIO

LOG_DATA = 'bite,user,completed\n102,alex,False\n101,alex,True\n29,bea,True\n9,cy,False\n101,bea,True\n29,alex,False\n'


# FOCUS: read the CSV with csv.DictReader and write six read-only properties with Counter.
# SUPPLIED: _top does the tie rule. It is not the skill of this exercise.
#        Use it. Do not edit it.


def _top(counts):
    """Key with the highest count; on a tie the smallest key. None for an empty Counter."""
    return min(counts, key=lambda key: (-counts[key], key)) if counts else None


class BiteStats:
    def __init__(self, data=LOG_DATA):
        self.rows = list(csv.DictReader(StringIO(data)))

    @property
    def total_attempts(self):
        return len(self.rows)

    @property
    def total_users(self):
        return len({row['user'] for row in self.rows})

    @property
    def total_bites(self):
        return len({int(row['bite']) for row in self.rows})

    @property
    def total_completed(self):
        return sum(row['completed'] == 'True' for row in self.rows)

    @property
    def most_active_user(self):
        return _top(Counter(row['user'] for row in self.rows))

    @property
    def most_popular_bite(self):
        return _top(Counter(int(row['bite']) for row in self.rows))
```
