## Approach

`__init__` assigns `self.email`, so construction and later changes share one
validation path. The setter checks the whole value before it assigns `_email`; a rejected value
cannot leave a half-updated object. `full_name` and `handle` are computed properties. `__repr__`
uses `!r` so the strings appear quoted, like the call that creates the object.

## Reference classes

```python
class Member:
    def __init__(self, first: str, last: str, email: str):
        self.first = first
        self.last = last
        self.email = email

    @property
    def full_name(self) -> str:
        return f"{self.first} {self.last}"

    @property
    def handle(self) -> str:
        return (self.first[0] + self.last).lower()

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        local, _, domain = value.partition("@")
        if (value.count("@") != 1 or not local or "." not in domain
                or domain.startswith(".") or domain.endswith(".")):
            raise ValueError(f"invalid email: {value!r}")
        self._email = value

    def __repr__(self) -> str:
        return f"Member({self.first!r}, {self.last!r}, {self.email!r})"

    def __str__(self) -> str:
        return f"{self.full_name} <{self.email}>"
```
