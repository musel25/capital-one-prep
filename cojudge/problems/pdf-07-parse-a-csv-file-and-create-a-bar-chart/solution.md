## Reference solution

Paste this code above the supplied tests and runner.

```python
import csv
import io
from collections import Counter

DATA = 'name,timezone\nAda,Africa/Nairobi\nBo,Europe/Warsaw\nCy,Africa/Nairobi\nDi,Pacific/Honolulu\nEli,Africa/Algiers\n'

def create_bar_chart(data=DATA):
    counts = Counter()
    for row in csv.DictReader(io.StringIO(data)):
        timezone = row['timezone'].strip()
        if timezone:
            counts[timezone] += 1
    width = max(20, max(map(len, counts), default=0))
    for timezone in sorted(counts):
        print(f'{timezone:<{width}} | {"+" * counts[timezone]}')
```
