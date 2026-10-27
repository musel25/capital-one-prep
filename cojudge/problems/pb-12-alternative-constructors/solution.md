## Reference solution

```python
import re
from urllib.parse import urlparse


class DomainException(Exception):
    """Raised when an invalid is created."""


class Domain:

    def __init__(self, name):
        if not re.match(r'.*\.[a-z]{2,3}$', name):
            raise DomainException(f"invalid domain: {name!r}")
        self.name = name

    def __str__(self):
        return self.name

    @classmethod
    def parse_url(cls, url):
        return cls(urlparse(url).netloc)

    @classmethod
    def parse_email(cls, email):
        return cls(email.split("@")[-1])
```
