## Reference solution

Paste this code above the supplied tests and runner.

```python
from collections import namedtuple
from datetime import datetime
import json


blog = dict(name='PyBites',
            founders=('Julian', 'Bob'),
            started=datetime(year=2016, month=12, day=19),
            tags=['Python', 'Code Challenges', 'Learn by Doing'],
            location='Spain/Australia',
            site='https://pybit.es')


def dict2nt(dict_):
    return namedtuple('Record', dict_)(**dict_)

def nt2json(nt):
    return json.dumps(nt._asdict(), default=str)
```
