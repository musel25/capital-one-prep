## Reference solution

```python
def summarize_logs(logs):
    out = {}
    for row in logs:
        counts = out.setdefault(row["service"], {"requests": 0, "errors": 0})
        counts["requests"] += 1
        if row["status"] >= 500:
            counts["errors"] += 1
    return out
```
