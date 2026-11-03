## How it works

Copy the settings, then apply each patch entry. Only `None` deletes. Every other value, also `False`, `0`, and empty values, is stored.

## Common mistakes

- Using `if not value:`, which deletes `False`, `0`, and `""`.
- Storing `None` instead of deleting the key.
- Changing the input `settings` instead of a copy.

## Solution

```python
def apply_settings_patch(settings, patch):
    result = settings.copy()
    for key, value in patch.items():
        if value is None:
            result.pop(key, None)
        else:
            result[key] = value
    return result
```
