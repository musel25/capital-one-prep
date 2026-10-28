## Reference solution

```python
def compare_versions(left, right):
    def parse(value):
        core, separator, prerelease = value.split("+", 1)[0].partition("-")
        return tuple(map(int, core.split("."))), prerelease.split(".") if separator else None

    left_core, left_pre = parse(left)
    right_core, right_pre = parse(right)
    if left_core != right_core:
        return (left_core > right_core) - (left_core < right_core)
    if left_pre is None:
        return 0 if right_pre is None else 1
    if right_pre is None:
        return -1
    for a, b in zip(left_pre, right_pre):
        if a == b:
            continue
        if a.isdigit() and b.isdigit():
            return (int(a) > int(b)) - (int(a) < int(b))
        if a.isdigit() != b.isdigit():
            return -1 if a.isdigit() else 1
        return (a > b) - (a < b)
    return (len(left_pre) > len(right_pre)) - (len(left_pre) < len(right_pre))
```
