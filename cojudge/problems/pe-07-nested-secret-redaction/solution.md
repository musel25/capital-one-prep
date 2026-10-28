## Reference solution

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
