# 12. Enforce per-user request limits

The service needs independent per-user request quotas that reset at fixed time boundaries.

Implement `limit_requests(requests, limit, window)`. Each request has a nonempty ASCII string `user` and a nonnegative integer timestamp `at`. Requests arrive in nondecreasing timestamp order. A request belongs to bucket `at // window`. For each user and bucket, allow at most `limit` requests. Return true for each allowed request and false for each denied request, in input order. The first request beyond the limit is denied. Each new bucket starts with the full quota. Users have independent quotas. Buckets start at multiples of `window`, not at the user's first request. Compare user strings exactly. Empty input returns an empty list. Each call starts with no prior requests. Do not change the input.

**Constraints:**

- limit is an integer from 1 through 100; window is an integer from 1 through 1000.
- Every request contains user and at with the stated types.
- Timestamps are integers greater than or equal to zero with no fixed maximum; booleans are not timestamps.
- Equal timestamps are allowed and each request uses one quota slot when accepted.
- Do not change the input objects. Each call starts with fresh state.
- Python 3.11. Standard library only.

Implement `limit_requests`. **Run** checks the examples. **Submit** checks all 16 cases.
