## Reference solution

Paste this code above the supplied tests and runner.

```python
import csv
import io
from collections import Counter, defaultdict

DATA = 'Season,Episode,Character,Line\n1,1,Cartman,Hello there\n1,1,Stan,Hey\n1,2,Cartman,One two three\n1,1,Cartman,Again\n'

def get_num_words_spoken_by_character_per_episode(data=DATA):
    counts = defaultdict(Counter)
    for row in csv.DictReader(io.StringIO(data)):
        counts[row['Character']][row['Episode']] += len(row['Line'].split())
    return counts
```
