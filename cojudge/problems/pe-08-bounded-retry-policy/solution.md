## Reference solution

```python
def retry_policy(statuses, base_delay, max_delay, max_attempts):
    attempts = 0
    delays = []
    last_status = None
    while attempts < max_attempts and attempts < len(statuses):
        last_status = statuses[attempts]
        attempts += 1
        retryable = last_status == 429 or last_status >= 500
        if not retryable or attempts >= max_attempts or attempts >= len(statuses):
            break
        delays.append(min(max_delay, base_delay * 2 ** (attempts - 1)))
    return {"attempts": attempts, "delays": delays, "status": last_status}
```
