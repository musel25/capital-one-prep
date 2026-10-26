def solve(data):
    delays = []
    for index in range(data["max_attempts"]):
        outcome = data["outcomes"][index]
        attempts = index + 1
        if isinstance(outcome, int) and 200 <= outcome < 300:
            return {"attempts": attempts, "delays": delays, "result": "success"}
        retryable = outcome == "timeout" or outcome in (429, 500, 502, 503, 504)
        if not retryable:
            return {"attempts": attempts, "delays": delays, "result": "failed"}
        if attempts == data["max_attempts"]:
            return {"attempts": attempts, "delays": delays, "result": "exhausted"}
        delays.append(min(data["cap"], data["base"] * 2 ** index))

# Supplied CoJudge adapter. Implement solve(data) above.
import json

class Solution:
    def run(self, payload: str) -> str:
        return json.dumps(solve(json.loads(payload)), ensure_ascii=True, allow_nan=False)
