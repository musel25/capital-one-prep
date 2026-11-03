**The ticket.** Clients send a job request again when they do not get an answer. Each request has an idempotency key. The same key means "this is the same request".

**Why it matters.** Without the key, a repeated request runs the job twice. For a payment, that charges the customer twice. With the key, the server returns the first result again.

### Your task

Write `enqueue_jobs(requests)`. Process the requests in order. Return one response for each request. Each request has a `key` and a `task`.

1. New key: save the key with its task and give it the next ID (1, 2, 3, …). Return `{'status': 'created', 'id': ID}`.
2. Known key with the same task: return `{'status': 'replayed', 'id': ORIGINAL_ID}`.
3. Known key with a different task: return `{'status': 'conflict', 'id': None}`. Keep the saved task unchanged.
4. Only `created` uses a new ID.
5. Compare keys and tasks exactly. Letter case and spaces count.

**Constraints:**

- 0–300 requests. Keys are nonempty strings. Tasks are strings and can be empty.
