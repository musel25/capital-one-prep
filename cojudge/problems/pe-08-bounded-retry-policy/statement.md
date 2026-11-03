**The ticket.** The service client tries a request again when the server fails for a short time. It must wait longer before each new try, and it must stop at a limit.

**Why it matters.** Without a limit, a client can try forever. Without a growing wait (backoff), many clients hit a server that is already overloaded. Both make an outage worse.

### Your task

Write `retry_policy(statuses, base_delay, max_delay, max_attempts)`. Return `{'attempts': N, 'delays': [...], 'status': last_status}`. Do not sleep and do not send requests.

`statuses` are the HTTP statuses that the server gives, one for each attempt, in order.

1. Make attempts one at a time. Each attempt reads the next status.
2. Stop when the status is not retryable. Retryable means `429` or `500` and higher.
3. Also stop after `max_attempts` attempts, or when no statuses remain.
4. Before each real retry, add a wait to `delays`: `min(max_delay, base_delay * 2 ** (attempts - 1))`, where `attempts` is the number of attempts so far. So the waits are `base`, `2 × base`, `4 × base`, …, never more than `max_delay`.
5. Add no wait when no other attempt will run.
6. `status` is the last status that you read. With no statuses, return 0 attempts, no delays, and `None`.

**Constraints:**

- `statuses` has 0–100 integers from 100 to 599.
- `max_attempts` is 1–10. `1 <= base_delay <= max_delay`.
