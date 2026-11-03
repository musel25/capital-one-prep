**The ticket.** The cache keeps each value for a fixed time (TTL, "time to live"). After that time, the value is old and must not be used.

**Why it matters.** Old cache values show wrong prices or permissions. The tests give the time as a number. So the result does not depend on the real clock, and the tests are repeatable.

### Your task

Write `run_cache(operations)`. Start with an empty cache. Process the operations in order. Return one result for each operation.

1. `put` has `key`, `value`, `now`, and `ttl`. Save the value with the deadline `now + ttl`. Replace an old entry. The result is `None`.
2. `get` has `key` and `now`. If the key is saved and `now < deadline`, return `{'hit': True, 'value': VALUE}`. Otherwise return `{'hit': False, 'value': None}`.
3. A saved `None`, `False`, `0`, or `""` is still a hit.
4. At `now == deadline`, the entry is expired. A `ttl` of `0` expires at once.
5. A `get` does not change the deadline.

**Constraints:**

- Times and TTLs are integers of 0 or more. Times do not go backwards.
- Keys are strings and can be empty. Values can be any JSON value.
