## Reference solution

Paste this code above the supplied tests and runner.

```python
import csv
import io
from collections import defaultdict

data = 'last_name,first_name,country_code\nWatsham,Husain,ID\nHarrold,Alphonso,BR\nApdell,Margo,CN\nTomblings,Deerdre,RU\nWasielewski,Sula,ID\n'

def group_names_by_country(data=data):
    groups = defaultdict(list)
    for row in csv.DictReader(io.StringIO(data)):
        groups[row['country_code']].append(row['first_name'] + ' ' + row['last_name'])
    return groups
```
