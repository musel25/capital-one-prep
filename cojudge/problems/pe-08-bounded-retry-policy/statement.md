# 08. Plan capped request retries

The service client needs a deterministic retry plan that never waits after its final attempt.

Implement retry_policy(statuses, base_delay, max_delay, max_attempts). Consume statuses in order, with one status per attempt. A status is retryable exactly when it is 429 or at least 500. Stop on any other status, after max_attempts attempts, or when statuses is exhausted. Before an actual retry after attempt i, append min(max_delay, base_delay * 2**(i-1)) to delays; i starts at 1. Append no delay unless another attempt will run. Return {'attempts': N, 'delays': [...], 'status': last_status}. An empty statuses list returns zero attempts, an empty delays list and null status. Ignore unconsumed statuses. Do not sleep, make requests or change the input list. Each call is independent.

**Constraints:**

- statuses contains 0–100 integer HTTP statuses from 100 through 599.
- max_attempts is an integer from 1 through 10.
- base_delay and max_delay are integers with 1 <= base_delay <= max_delay.
- Inputs satisfy the contract. No input validation, clock access or network access is required.
- Do not change the input objects. Each call starts with fresh state.
- Python 3.11. Standard library only.

Implement `retry_policy`. **Run** checks the examples. **Submit** checks all 16 cases.
