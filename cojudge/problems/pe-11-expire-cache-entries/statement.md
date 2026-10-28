The cache must distinguish cached null values from misses and expire entries at the exact deadline.

Implement `run_cache(operations)`. Process operations in order with an initially empty cache. A put is `{'op': 'put', 'key': STRING, 'value': JSON_VALUE, 'now': INTEGER, 'ttl': INTEGER}`. Store the value with expiry `now + ttl`, replacing any value and deadline for that key. Append null to the output. A get is `{'op': 'get', 'key': STRING, 'now': INTEGER}`. If the key exists and `now < expiry`, append `{'hit': true, 'value': STORED_VALUE}`. Otherwise append `{'hit': false, 'value': null}`. A stored null is a hit before expiry. A zero TTL expires immediately. Gets do not change expiry. Return one result per operation in input order. Keys are ASCII strings and can be empty. Times are nonnegative integers in nondecreasing order; TTLs are nonnegative integers. Compare keys exactly. Each call starts empty. Do not use the wall clock or impose a capacity. Do not change the input.

**Constraints:**

- Operations are put or get and contain all fields specified for that operation.
- Values can be any JSON value, including null, false, zero, empty containers, and nested objects.
- now and ttl are integers greater than or equal to zero; booleans are not times.
- There is no fixed maximum integer time.
- Floating-point values have at most six decimal places and an absolute value at most 1000000.
- Do not change the input objects. Each call starts with fresh state.
- Python 3.11. Standard library only.

Implement `run_cache`. **Run** checks the examples. **Submit** checks all 17 cases.
