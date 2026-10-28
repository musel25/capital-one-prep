The service needs independent per-user request quotas that reset at fixed time boundaries.

Implement `limit_requests(requests, limit, window)`. Return one boolean per request, in input order.

Each request belongs to bucket `at // window`. Allow at most `limit` requests per user in each bucket. Deny the first request beyond the quota. Denied requests use no quota slot.

Buckets start at multiples of `window`, not at a user's first request. Each new bucket has a full quota. Users have independent quotas; compare names exactly. Empty input returns an empty list.

**Constraints:**

- limit is an integer from 1 through 100; window is an integer from 1 through 1000.
- Every request contains user and at with the stated types.
- Timestamps are integers greater than or equal to zero with no fixed maximum; booleans are not timestamps.
- Equal timestamps are allowed and each request uses one quota slot when accepted.
- Each request has a nonempty ASCII `user` string and a nonnegative integer `at`. Requests arrive in nondecreasing timestamp order.
- Do not change input objects or their nested values. Each call starts with fresh state.
