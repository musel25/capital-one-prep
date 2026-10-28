The service client needs a deterministic retry plan that never waits after its final attempt.

Implement `retry_policy(statuses, base_delay, max_delay, max_attempts)`. Return `{'attempts': N, 'delays': [...], 'status': last_status}`.

Read one status per attempt, in input order. Retry only status 429 or statuses at least 500. Stop on any other status, at `max_attempts`, or when statuses run out. Ignore unconsumed statuses.

Before an actual retry after attempt `i`, append `min(max_delay, base_delay * 2**(i-1))` to `delays`. Attempt numbers start at 1. Add no delay after the final attempt.

Empty input returns zero attempts, no delays, and `None` status. Produce a plan; do not sleep or make requests.

**Constraints:**

- statuses contains 0–100 integer HTTP statuses from 100 through 599.
- max_attempts is an integer from 1 through 10.
- base_delay and max_delay are integers with 1 <= base_delay <= max_delay.
- Do not change input objects or their nested values. Each call starts with fresh state.
