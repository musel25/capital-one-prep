## How it works

Handle the missing value first. Then clean the text and look it up in two sets of known words. Anything else is invalid, so the caller can report a configuration error.

## Common mistakes

- Returning `default` for invalid text. Invalid text must return `None`.
- Forgetting to lowercase, so `OFF` is invalid.
- Forgetting the words `1` and `0`.

## Solution

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
