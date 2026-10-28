## Reference solution

Paste this code above the supplied tests and runner.

```python
import csv
from collections import Counter
from io import StringIO

LOG_DATA = 'bite,user,completed\n102,alex,False\n101,alex,True\n29,bea,True\n9,cy,False\n101,bea,True\n29,alex,False\n'


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
        counts = Counter(row['user'] for row in self.rows)
        return min(counts, key=lambda user: (-counts[user], user)) if counts else None

    @property
    def most_popular_bite(self):
        counts = Counter(int(row['bite']) for row in self.rows)
        return min(counts, key=lambda bite: (-counts[bite], bite)) if counts else None
```
