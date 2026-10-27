## Reference solution

```python
class RecordScore():
    """Class to track a game's maximum score"""

    def __init__(self):
        self._max = None

    def __call__(self, score):
        if self._max is None or score > self._max:
            self._max = score
        return self._max
```
