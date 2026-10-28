"""Count requests in independent per-user fixed windows."""

CASES = [
    {"label": "allow only the first requests in a bucket", "input": {"requests": [{"user": "a", "at": 0}, {"user": "a", "at": 1}, {"user": "a", "at": 2}], "limit": 2, "window": 10}, "expected": [True, True, False]},
    {"label": "exact boundary opens a new window", "input": {"requests": [{"user": "a", "at": 9}, {"user": "a", "at": 10}], "limit": 1, "window": 10}, "expected": [True, True]},
    {"label": "users have independent quotas", "input": {"requests": [{"user": "a", "at": 0}, {"user": "b", "at": 0}, {"user": "a", "at": 0}, {"user": "b", "at": 0}], "limit": 1, "window": 10}, "expected": [True, True, False, False]},
    {"label": "empty request list", "input": {"requests": [], "limit": 1, "window": 1}, "expected": []},
    {"label": "denied requests do not reduce next window quota", "input": {"requests": [{"user": "a", "at": 0}, {"user": "a", "at": 1}, {"user": "a", "at": 2}, {"user": "a", "at": 10}], "limit": 1, "window": 10}, "expected": [True, False, False, True]},
    {"label": "one-unit windows and repeated times", "input": {"requests": [{"user": "a", "at": 0}, {"user": "a", "at": 0}, {"user": "a", "at": 1}, {"user": "a", "at": 1}], "limit": 1, "window": 1}, "expected": [True, False, True, False]},
    {"label": "same-time requests consume separate slots", "input": {"requests": [{"user": "a", "at": 7}, {"user": "a", "at": 7}, {"user": "a", "at": 7}, {"user": "a", "at": 7}], "limit": 3, "window": 10}, "expected": [True, True, True, False]},
    {"label": "first request need not start at zero", "input": {"requests": [{"user": "a", "at": 35}, {"user": "a", "at": 39}, {"user": "a", "at": 40}], "limit": 1, "window": 10}, "expected": [True, False, True]},
    {"label": "skipped windows start with full quota", "input": {"requests": [{"user": "a", "at": 0}, {"user": "a", "at": 1000}, {"user": "a", "at": 1001}], "limit": 1, "window": 10}, "expected": [True, True, False]},
    {"label": "user matching is case sensitive", "input": {"requests": [{"user": "a", "at": 0}, {"user": "A", "at": 0}, {"user": "a", "at": 1}], "limit": 1, "window": 10}, "expected": [True, True, False]},
    {"label": "windows are fixed rather than sliding", "input": {"requests": [{"user": "a", "at": 9}, {"user": "a", "at": 10}, {"user": "a", "at": 11}], "limit": 1, "window": 10}, "expected": [True, True, False]},
    {"label": "maximum allowed limit", "input": {"requests": [{"user": "a", "at": 0}] * 101, "limit": 100, "window": 10}, "expected": [True] * 100 + [False]},
    {"label": "large timestamps do not truncate", "input": {"requests": [{"user": "a", "at": 18446744073709551616}, {"user": "a", "at": 18446744073709551617}, {"user": "a", "at": 18446744073709551618}], "limit": 1, "window": 2}, "expected": [True, False, True]},
    {"label": "user strings are not stripped", "input": {"requests": [{"user": "a", "at": 0}, {"user": " a", "at": 0}, {"user": "a", "at": 0}], "limit": 1, "window": 10}, "expected": [True, True, False]},
    {"label": "maximum window boundary", "input": {"requests": [{"user": "a", "at": 999}, {"user": "a", "at": 1000}, {"user": "a", "at": 1999}, {"user": "a", "at": 2000}], "limit": 1, "window": 1000}, "expected": [True, True, False, True]},
    {"label": "users cross the same boundary independently", "input": {"requests": [{"user": "a", "at": 0}, {"user": "b", "at": 8}, {"user": "a", "at": 9}, {"user": "a", "at": 10}, {"user": "b", "at": 10}, {"user": "b", "at": 11}], "limit": 1, "window": 10}, "expected": [True, True, False, True, True, False]},
]

SPEC = {
    "number": 12,
    "slug": "limit-fixed-window-requests",
    "title": "Enforce per-user request limits",
    "difficulty": "Medium",
    "category": "03-stateful-services",
    "ticket": "The service needs independent per-user request quotas that reset at fixed time boundaries.",
    "task": "Implement `limit_requests(requests, limit, window)`. Each request has a nonempty ASCII string `user` and a nonnegative integer timestamp `at`. Requests arrive in nondecreasing timestamp order. A request belongs to bucket `at // window`. For each user and bucket, allow at most `limit` requests. Return true for each allowed request and false for each denied request, in input order. The first request beyond the limit is denied. Each new bucket starts with the full quota. Users have independent quotas. Buckets start at multiples of `window`, not at the user's first request. Compare user strings exactly. Empty input returns an empty list. Each call starts with no prior requests. Do not change the input.",
    "constraints": ["limit is an integer from 1 through 100; window is an integer from 1 through 1000.", "Every request contains user and at with the stated types.", "Timestamps are integers greater than or equal to zero with no fixed maximum; booleans are not timestamps.", "Equal timestamps are allowed and each request uses one quota slot when accepted."],
    "function": "limit_requests",
    "starter": "def limit_requests(requests, limit, window):\n    raise NotImplementedError\n",
    "reference": '''def limit_requests(requests, limit, window):
    states = {}
    results = []
    for request in requests:
        user = request["user"]
        bucket = request["at"] // window
        previous_bucket, used = states.get(user, (None, 0))
        if previous_bucket != bucket:
            used = 0
        allowed = used < limit
        if allowed:
            used += 1
        states[user] = (bucket, used)
        results.append(allowed)
    return results
''',
    "java": '''public Object solve(Map<String,Object> d) {
    int limit = n(d.get("limit"));
    BigInteger window = BigInteger.valueOf(lng(d.get("window")));
    Map<String,Map<BigInteger,Integer>> counts = new HashMap<>();
    List<Object> results = new ArrayList<>();
    for (Object raw : arr(d.get("requests"))) {
        Map<String,Object> request = obj(raw);
        String user = s(request.get("user"));
        BigInteger at = new BigInteger(request.get("at").toString());
        BigInteger bucket = at.divide(window);
        Map<BigInteger,Integer> userCounts = counts.computeIfAbsent(user, k -> new HashMap<>());
        int used = userCounts.getOrDefault(bucket, 0);
        boolean allowed = used < limit;
        if (allowed) userCounts.put(bucket, used + 1);
        results.add(allowed);
    }
    return results;
}''',
    "cases": CASES,
    "mutations": [
        {"name": "allow one extra request", "old": "allowed = used < limit", "new": "allowed = used <= limit"},
        {"name": "share quota across all users", "old": 'user = request["user"]', "new": 'user = "shared"'},
        {"name": "do not reset count for a new bucket", "old": "if previous_bucket != bucket:\n            used = 0", "new": "if previous_bucket != bucket:\n            used = used"},
        {"name": "reset quota at every new timestamp", "old": 'bucket = request["at"] // window', "new": 'bucket = request["at"]'},
    ],
}
