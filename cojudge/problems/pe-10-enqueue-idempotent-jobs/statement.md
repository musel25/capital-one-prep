# 10. Handle duplicate job submissions

The job queue must replay duplicate submissions and reject reuse of a key for a different task.

Implement `enqueue_jobs(requests)`. Each request has a nonempty ASCII string `key` and an ASCII string `task`, which can be empty. Process requests in order. For a new key, store its task, allocate the next integer ID starting at 1, and return `{'status': 'created', 'id': ID}`. For an existing key with the same task, return `{'status': 'replayed', 'id': ORIGINAL_ID}`. For an existing key with a different task, return `{'status': 'conflict', 'id': null}`. A replay or conflict consumes no ID. A conflict changes no stored key, task, or ID. Compare strings exactly. Return one response per request in input order. Empty input returns an empty list. Each function call starts with an empty queue and ID 1. Do not change the input.

**Constraints:**

- All requests contain key and task with the stated string types.
- Keys are nonempty ASCII strings; tasks can be empty.
- Only a newly accepted key allocates an ID.
- Do not change the input objects. Each call starts with fresh state.
- Python 3.11. Standard library only.

Implement `enqueue_jobs`. **Run** checks the examples. **Submit** checks all 14 cases.
