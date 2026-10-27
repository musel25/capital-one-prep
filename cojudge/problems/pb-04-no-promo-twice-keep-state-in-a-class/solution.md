## Reference solution

```python
import random

BITES = {6: 'PyBites Die Hard',
         7: 'Parsing dates from logs',
         9: 'Palindromes',
         10: 'Practice exceptions',
         11: 'Enrich a class with dunder methods',
         12: 'Write a user validation function',
         13: 'Convert dict in namedtuple/json',
         14: 'Generate a table of n sequences',
         15: 'Enumerate 2 sequences',
         16: 'Special PyBites date generator',
         17: 'Form teams from a group of friends',
         18: 'Find the most common word',
         19: 'Write a simple property',
         20: 'Write a context manager',
         21: 'Query a nested data structure'}
BITES_DONE = {6, 10, 16, 18, 21}


class NoBitesAvailable(Exception):
    pass


class Promo:

    def __init__(self, bites=None, bites_done=None):
        if bites is None:
            bites = BITES
        if bites_done is None:
            bites_done = BITES_DONE
        self.all_bites = bites.copy()
        self.bites_done = bites_done.copy()

    def _pick_random_bite(self):
        available = sorted(set(self.all_bites) - self.bites_done)
        if not available:
            raise NoBitesAvailable("all Bites have been done")
        return random.choice(available)

    def new_bite(self):
        bite = self._pick_random_bite()
        self.bites_done.add(bite)
        return bite
```
