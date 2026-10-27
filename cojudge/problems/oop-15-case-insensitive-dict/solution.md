## Approach

Every write goes through `__setitem__`, which lowercases the key. `__init__` starts
with an empty dictionary and then calls this class's `update`, and `update` assigns one item at a
time. Every read method lowercases its key before it calls the `dict` version. Overriding only
`__setitem__` and `__getitem__` would look correct in simple tests but fail for the constructor,
`update`, `get`, `in`, and `pop`, because `dict` methods do not call each other.

## Reference classes

```python
_MISSING = object()


class CaseInsensitiveDict(dict):
    def __init__(self, mapping: dict | None = None):
        super().__init__()
        if mapping is not None:
            self.update(mapping)

    def __setitem__(self, key: str, value) -> None:
        super().__setitem__(key.lower(), value)

    def __getitem__(self, key: str):
        return super().__getitem__(key.lower())

    def __contains__(self, key: object) -> bool:
        return super().__contains__(key.lower())

    def get(self, key: str, default=None):
        return super().get(key.lower(), default)

    def update(self, mapping: dict) -> None:
        for key, value in mapping.items():
            self[key] = value

    def pop(self, key: str, default=_MISSING):
        if default is _MISSING:
            return super().pop(key.lower())
        return super().pop(key.lower(), default)
```
