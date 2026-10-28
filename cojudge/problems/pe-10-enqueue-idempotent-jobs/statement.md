The job queue must replay duplicate submissions and reject reuse of a key for a different task.

Implement `enqueue_jobs(requests)`. Process requests in order and return one response per request.

- New key: store its task and allocate the next ID, starting at 1. Return `{'status': 'created', 'id': ID}`.
- Existing key, same task: return `{'status': 'replayed', 'id': ORIGINAL_ID}`.
- Existing key, different task: return `{'status': 'conflict', 'id': None}`.

Replays and conflicts consume no ID. Conflicts change no stored data. Compare strings exactly. Each call starts with an empty queue and ID 1. Empty input returns an empty list.

**Constraints:**

- All requests contain key and task with the stated string types.
- Keys are nonempty ASCII strings; tasks can be empty.
- Only a newly accepted key allocates an ID.
- Tasks are ASCII strings and can be empty.
- Do not change input objects or their nested values. Each call starts with fresh state.
