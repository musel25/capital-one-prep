## Reference solution

Paste this code above the supplied tests and runner.

```python
from collections import namedtuple
from datetime import datetime
Opera = namedtuple('Opera', 'author play date')
Composer = namedtuple('Composer', 'name born died')
# Constructed fixture names and dates; not a historical opera database.
composers = {
    'Aster': Composer('Aster', '1700-01-01', '1760-01-01'),
    'Birch': Composer('Birch', '1730-06-01', '1790-01-01'),
    'Cedar': Composer('Cedar', '1761-01-01', '1820-01-01'),
}
operas = [Opera('Aster', 'Early', '1729-01-01'),
          Opera('Aster', 'Together', '1750-01-01'),
          Opera('Aster', 'Farewell', '1760-01-01'),
          Opera('Birch', 'Later', '1780-01-01')]
def _get_date(value):
    return datetime.strptime(value, '%Y-%m-%d')
def operas_both_at_premiere(guest, composer):
    if guest not in composers or composer not in composers:
        raise ValueError('Unknown composer')
    people = [composers[guest], composers[composer]]
    return [opera.play for opera in operas if opera.author == composer and
            all(_get_date(person.born) <= _get_date(opera.date) <= _get_date(person.died) for person in people)]
```
