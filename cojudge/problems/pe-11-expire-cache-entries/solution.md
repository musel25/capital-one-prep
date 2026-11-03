## How it works

Save each value with its deadline. A get is a hit only before the deadline. The check uses the key, not the value, so falsy values are cached correctly.

## Common mistakes

- Keeping a value at the exact deadline (`<=`).
- Treating a cached `None`, `False`, or `0` as a miss.
- Using `ttl` as the deadline instead of `now + ttl`.

## Solution

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
