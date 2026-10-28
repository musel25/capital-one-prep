## Reference solution

```python
def parse_flag(value, default):
    if value is None:
        return default
    value = value.strip(" \t\r\n").lower()
    if value in {"true", "1", "yes", "on"}:
        return True
    if value in {"false", "0", "no", "off"}:
        return False
    return None
```
