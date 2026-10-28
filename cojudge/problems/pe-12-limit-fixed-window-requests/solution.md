## Reference solution

```python
def limit_requests(requests, limit, window):
    states = {}
    results = []
    for request in requests:
        user = request["user"]
        bucket = request["at"] // window
        previous_bucket, used = states.get(user, (None, 0))
        if previous_bucket != bucket:
            used = 0
        allowed = used < limit
        if allowed:
            used += 1
        states[user] = (bucket, used)
        results.append(allowed)
    return results
```
