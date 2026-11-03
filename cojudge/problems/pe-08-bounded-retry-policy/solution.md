## How it works

Each loop pass is one attempt. Stop at a final status, or when the limit or the statuses run out. Otherwise add the next wait. It doubles each time and is capped at `max_delay`.

## Common mistakes

- Not retrying `429`. It means "too many requests, try later".
- Adding a wait after the last attempt.
- Starting the doubling one step too high, so the first wait is `2 × base`.

## Solution

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
