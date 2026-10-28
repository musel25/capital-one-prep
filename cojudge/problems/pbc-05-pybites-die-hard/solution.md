## Reference solution

Paste this code above the supplied tests and runner.

```python
from collections import Counter, namedtuple

Stats = namedtuple("Stats", "user challenge")
EXCLUDED = {"bbelderbos", "juliansequeira", "pybites"}
FILES = ('22/wonderfulboyx', '25/bbelderbos', '25/clamytoe', '21/wonderfulboyx', '25/santiagobenitez', '23/santiagobenitez', '07/santiagobenitez')

def gen_files(tempfile):
    with open(tempfile, encoding='utf-8') as source:
        for line in source:
            if line.strip():
                yield line.strip()

def diehard_pybites(files=FILES):
    users, challenges = Counter(), Counter()
    for path in files:
        challenge, user = path.strip().split('/')
        if user in EXCLUDED:
            continue
        users[user] += 1
        challenges[challenge] += 1
    return Stats(users.most_common(1)[0][0] if users else None,
                 challenges.most_common(1)[0] if challenges else (None, 0))
```
