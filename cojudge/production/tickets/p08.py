"""Plan bounded retries without sleeping or making requests."""

CASES = [
    {"input": {"statuses": [503, 503, 200], "base_delay": 2, "max_delay": 3, "max_attempts": 3}, "expected": {"attempts": 3, "delays": [2, 3], "status": 200}, "label": "retry server failures with a capped delay"},
    {"input": {"statuses": [400, 200], "base_delay": 1, "max_delay": 8, "max_attempts": 3}, "expected": {"attempts": 1, "delays": [], "status": 400}, "label": "terminal client error ignores later statuses"},
    {"input": {"statuses": [], "base_delay": 1, "max_delay": 1, "max_attempts": 1}, "expected": {"attempts": 0, "delays": [], "status": None}, "label": "empty status source"},
    {"input": {"statuses": [429], "base_delay": 2, "max_delay": 8, "max_attempts": 5}, "expected": {"attempts": 1, "delays": [], "status": 429}, "label": "no wait when no next status exists"},
    {"input": {"statuses": [503, 200], "base_delay": 1, "max_delay": 8, "max_attempts": 1}, "expected": {"attempts": 1, "delays": [], "status": 503}, "label": "attempt budget includes the first call"},
    {"input": {"statuses": [429, 201], "base_delay": 3, "max_delay": 10, "max_attempts": 2}, "expected": {"attempts": 2, "delays": [3], "status": 201}, "label": "429 is retryable"},
    {"input": {"statuses": [499, 200], "base_delay": 1, "max_delay": 4, "max_attempts": 2}, "expected": {"attempts": 1, "delays": [], "status": 499}, "label": "499 is terminal"},
    {"input": {"statuses": [500, 200], "base_delay": 1, "max_delay": 4, "max_attempts": 2}, "expected": {"attempts": 2, "delays": [1], "status": 200}, "label": "500 starts the server-error range"},
    {"input": {"statuses": [599, 204], "base_delay": 1, "max_delay": 4, "max_attempts": 2}, "expected": {"attempts": 2, "delays": [1], "status": 204}, "label": "599 is retryable"},
    {"input": {"statuses": [301, 500], "base_delay": 1, "max_delay": 4, "max_attempts": 2}, "expected": {"attempts": 1, "delays": [], "status": 301}, "label": "redirect is terminal"},
    {"input": {"statuses": [100, 200], "base_delay": 1, "max_delay": 4, "max_attempts": 2}, "expected": {"attempts": 1, "delays": [], "status": 100}, "label": "informational status is terminal"},
    {"input": {"statuses": [501, 502, 503], "base_delay": 2, "max_delay": 20, "max_attempts": 8}, "expected": {"attempts": 3, "delays": [2, 4], "status": 503}, "label": "source exhaustion stops retrying"},
    {"input": {"statuses": [500, 500, 500, 500, 500], "base_delay": 3, "max_delay": 5, "max_attempts": 4}, "expected": {"attempts": 4, "delays": [3, 5, 5], "status": 500}, "label": "cap and attempt budget both apply"},
    {"input": {"statuses": [500, 429, 200], "base_delay": 7, "max_delay": 7, "max_attempts": 10}, "expected": {"attempts": 3, "delays": [7, 7], "status": 200}, "label": "base delay equals cap"},
    {"input": {"statuses": [200], "base_delay": 5, "max_delay": 10, "max_attempts": 10}, "expected": {"attempts": 1, "delays": [], "status": 200}, "label": "immediate success has no delay"},
    {"input": {"statuses": [500, 500, 200], "base_delay": 100000000000000000000, "max_delay": 300000000000000000000, "max_attempts": 3}, "expected": {"attempts": 3, "delays": [100000000000000000000, 200000000000000000000], "status": 200}, "label": "large integer delays remain exact"},
]

SPEC = {
    "number": 8,
    "slug": "bounded-retry-policy",
    "title": "Plan capped request retries",
    "difficulty": "Medium",
    "category": "02-clients-and-reliability",
    "ticket": "The service client needs a deterministic retry plan that never waits after its final attempt.",
    "task": "Implement retry_policy(statuses, base_delay, max_delay, max_attempts). Consume statuses in order, with one status per attempt. A status is retryable exactly when it is 429 or at least 500. Stop on any other status, after max_attempts attempts, or when statuses is exhausted. Before an actual retry after attempt i, append min(max_delay, base_delay * 2**(i-1)) to delays; i starts at 1. Append no delay unless another attempt will run. Return {'attempts': N, 'delays': [...], 'status': last_status}. An empty statuses list returns zero attempts, an empty delays list and null status. Ignore unconsumed statuses. Do not sleep, make requests or change the input list. Each call is independent.",
    "constraints": ["statuses contains 0–100 integer HTTP statuses from 100 through 599.", "max_attempts is an integer from 1 through 10.", "base_delay and max_delay are integers with 1 <= base_delay <= max_delay.", "Inputs satisfy the contract. No input validation, clock access or network access is required."],
    "function": "retry_policy",
    "starter": "def retry_policy(statuses, base_delay, max_delay, max_attempts):\n    raise NotImplementedError\n",
    "cases": CASES,
}

SPEC["reference"] = '''def retry_policy(statuses, base_delay, max_delay, max_attempts):
    attempts = 0
    delays = []
    last_status = None
    while attempts < max_attempts and attempts < len(statuses):
        last_status = statuses[attempts]
        attempts += 1
        retryable = last_status == 429 or last_status >= 500
        if not retryable or attempts >= max_attempts or attempts >= len(statuses):
            break
        delays.append(min(max_delay, base_delay * 2 ** (attempts - 1)))
    return {"attempts": attempts, "delays": delays, "status": last_status}
'''

SPEC["java"] = '''public Object solve(Map<String,Object> d) {
    List<Object> statuses = arr(d.get("statuses")), delays = new ArrayList<>();
    int allowed = Math.min(n(d.get("max_attempts")), statuses.size());
    BigInteger delay = new BigInteger(d.get("base_delay").toString());
    BigInteger cap = new BigInteger(d.get("max_delay").toString());
    Object last = null;
    int attempts = 0;
    while (attempts < allowed) {
        last = statuses.get(attempts++);
        int status = n(last);
        if ((status != 429 && status < 500) || attempts == allowed) break;
        delays.add(delay.min(cap));
        delay = delay.shiftLeft(1);
    }
    return map("attempts", attempts, "delays", delays, "status", last);
}
'''

SPEC["mutations"] = [
    {"name": "do not retry 429", "old": 'last_status == 429 or last_status >= 500', "new": 'last_status >= 500'},
    {"name": "exclude status 500", "old": 'last_status >= 500', "new": 'last_status > 500'},
    {"name": "double the first retry delay", "old": '2 ** (attempts - 1)', "new": '2 ** attempts'},
    {"name": "ignore delay cap", "old": 'min(max_delay, base_delay * 2 ** (attempts - 1))', "new": 'base_delay * 2 ** (attempts - 1)'},
    {"name": "wait after source exhaustion", "old": 'or attempts >= len(statuses)', "new": ''},
    {"name": "wait after attempt budget exhaustion", "old": 'or attempts >= max_attempts', "new": ''},
]
