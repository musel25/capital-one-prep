## How it works

The function has three cases: a dictionary, a list, and a plain value. Dictionaries and lists build new containers and call the function again for each item. Secret keys get `'[REDACTED]'` instead.

## Common mistakes

- Comparing keys with their original case, so `Token` is missed.
- Not looking inside lists, so `[{"token": 1}]` leaks.
- Stripping keys or matching parts of keys.

## Solution

```python
def redact_secrets(value):
    if isinstance(value, dict):
        return {
            key: "[REDACTED]" if key.lower() in {"password", "token", "secret"}
            else redact_secrets(item)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [redact_secrets(item) for item in value]
    return value
```
