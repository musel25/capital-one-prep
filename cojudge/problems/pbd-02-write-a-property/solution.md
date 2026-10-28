## Reference solution

Paste this code above the supplied tests and runner.

```python
from datetime import datetime

NOW = datetime.now()


class Promo:
    def __init__(self, name: str, expires: datetime):
        self.name = name
        self.expires = expires

    @property
    def expired(self) -> bool:
        return self.expires < NOW
```
