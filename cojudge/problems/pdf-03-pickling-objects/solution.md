## Reference solution

Paste this code above the supplied tests and runner.

```python
import pickle
from collections import namedtuple

Record = namedtuple("Record", "name score")
DEFAULT_PICKLE = pickle.dumps([Record("Ada", 9), Record("Bo", 7)])

def deserialize(file=None):
    if file is None:
        return pickle.loads(DEFAULT_PICKLE)
    with open(file, 'rb') as source:
        return pickle.load(source)

def serialize(file, data=None):
    if data is None:
        data = deserialize()
    with open(file, 'wb') as destination:
        pickle.dump(data, destination)
```
