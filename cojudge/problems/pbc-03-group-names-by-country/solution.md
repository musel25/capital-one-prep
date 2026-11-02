## Reference solution

Paste this code above the supplied tests and runner.

```python
import csv
import io
from collections import defaultdict

data = 'last_name,first_name,country_code\nWatsham,Husain,ID\nHarrold,Alphonso,BR\nApdell,Margo,CN\nTomblings,Deerdre,RU\nWasielewski,Sula,ID\n'

# FOCUS: write the grouping by hand with the collections type named in the task.
# SUPPLIED: _rows reads the CSV text. It is not the skill of this exercise.
#        Use it. Do not edit it.


def _rows(data):
    """Yield one dict per CSV record, keyed by the header names. Blank lines are skipped."""
    return csv.DictReader(io.StringIO(data))


def group_names_by_country(data=data):
    groups = defaultdict(list)
    for row in _rows(data):
        groups[row['country_code']].append(row['first_name'] + ' ' + row['last_name'])
    return groups
```
