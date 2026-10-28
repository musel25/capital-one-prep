The cache must distinguish cached null values from misses and expire entries at the exact deadline.

Implement `run_cache(operations)`. Process operations in order, starting with an empty cache. Return one result per operation.

- `put` has `key`, `value`, `now`, and `ttl`. Store the value with expiry `now + ttl`, replacing the prior value and deadline. Return `None`.
- `get` has `key` and `now`. Before expiry (`now < expiry`), return `{'hit': True, 'value': STORED_VALUE}`. Otherwise return `{'hit': False, 'value': None}`.

A stored `None` is a hit before expiry. Zero TTL expires immediately. Gets do not change expiry. Compare keys exactly. Use the supplied times; do not use the wall clock or impose a capacity.

**Constraints:**

- Operations are put or get and contain all fields specified for that operation.
- Values can be any JSON value, including null, false, zero, empty containers, and nested objects.
- now and ttl are integers greater than or equal to zero; booleans are not times.
- There is no fixed maximum integer time.
- Floating-point values have at most six decimal places and an absolute value at most 1000000.
- Keys are ASCII strings, including empty strings. Times arrive in nondecreasing order.
- Do not change input objects or their nested values. Each call starts with fresh state.
