## Reference solution

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
