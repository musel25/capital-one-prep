## Reference solution

```python
import re
from urllib.parse import urlparse

# FOCUS: write __str__ and the two classmethods by hand.
#        A classmethod gets the class as `cls` and returns cls(...),
#        so a subclass gets an instance of the subclass.
# SUPPLIED: the three helpers below do the regex, URL and email work.
#        They are not the skill of this exercise. Use them. Do not edit them.


def _is_valid_domain(name):
    """True for names such as 'pybit.es': text, a dot, 2 or 3 lowercase letters."""
    return re.fullmatch(r'.*\.[a-z]{2,3}', name) is not None


def _host_of_url(url):
    """'https://pybit.es/articles/?q=1' -> 'pybit.es' (a port stays: 'pybit.es:443')."""
    return urlparse(url).netloc


def _domain_of_email(email):
    """'julian@pybit.es' -> 'pybit.es'"""
    return email.split('@')[-1]


class DomainException(Exception):
    """Raised when an invalid is created."""


class Domain:

    def __init__(self, name):
        if not _is_valid_domain(name):
            raise DomainException(f"invalid domain: {name!r}")
        self.name = name

    def __str__(self):
        return self.name

    @classmethod
    def parse_url(cls, url):
        return cls(_host_of_url(url))

    @classmethod
    def parse_email(cls, email):
        return cls(_domain_of_email(email))
```
