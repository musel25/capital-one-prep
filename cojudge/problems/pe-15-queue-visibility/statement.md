A worker queue must redeliver unacknowledged jobs after their visibility timeout.

Implement `process_queue(operations, visibility)`. Return one result per operation, in input order.

- `enqueue` has `id` and `at`. Append the job and return `None`.
- `poll` has `at`. Return the earliest unacknowledged job in enqueue order that was never polled or whose deadline is at or before `at`. Set its deadline to `at + visibility`. Return `None` if no job is available.
- `ack` has `id` and `at`. Remove the job and return `True` only when it is in flight and `at` is strictly before its deadline. Otherwise return `False` without a state change.

At exact expiry, acknowledgment fails and polling can redeliver the job. Empty input returns an empty list.

**Constraints:**

- 0–300 operations. All required fields are present; op is enqueue, poll, or ack.
- Job IDs are nonempty ASCII strings of at most 80 characters. Each ID is enqueued at most once.
- Times are integers from 0 to 2000000000 in nondecreasing order. Equal times are allowed.
- Visibility is an integer from 1 to 1000. Operations run sequentially; no parallel execution.
- Do not change input objects or their nested values. Each call starts with fresh state.
