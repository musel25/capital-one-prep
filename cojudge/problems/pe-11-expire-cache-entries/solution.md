## Reference solution

```python
def run_cache(operations):
    entries = {}
    results = []
    for operation in operations:
        key, now = operation["key"], operation["now"]
        if operation["op"] == "put":
            entries[key] = (operation["value"], now + operation["ttl"])
            results.append(None)
        else:
            entry = entries.get(key)
            if entry is not None and now < entry[1]:
                results.append({"hit": True, "value": entry[0]})
            else:
                results.append({"hit": False, "value": None})
    return results
```
