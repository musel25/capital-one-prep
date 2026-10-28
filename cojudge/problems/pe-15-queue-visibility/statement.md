# 15. Deliver jobs with a visibility timeout

A worker queue must redeliver unacknowledged jobs after their visibility timeout.

Implement `process_queue(operations, visibility)`. Process operations in input order. `enqueue` has `id` and `at`: append a job and return null. `poll` has `at`: return the earliest unacknowledged job in enqueue order that has never been polled or whose deadline is at or before `at`; return null if none exists. A successful poll sets its deadline to `at + visibility`. `ack` has `id` and `at`: remove the job and return true only if it is currently in flight and `at` is strictly before its deadline. Otherwise, return false without a state change. At exact expiry, acknowledgment fails and polling can redeliver the job. Return a list with one result per operation. An empty list returns an empty list. Do not modify the input. Calls are independent.

**Constraints:**

- 0–300 operations. All required fields are present; op is enqueue, poll, or ack.
- Job IDs are nonempty ASCII strings of at most 80 characters. Each ID is enqueued at most once.
- Times are integers from 0 to 2000000000 in nondecreasing order. Equal times are allowed.
- Visibility is an integer from 1 to 1000. Operations run sequentially; no parallel execution.
- Inputs satisfy the contract; no validation is required.
- Do not change the input objects. Each call starts with fresh state.
- Python 3.11. Standard library only.

Implement `process_queue`. **Run** checks the examples. **Submit** checks all 16 cases.
