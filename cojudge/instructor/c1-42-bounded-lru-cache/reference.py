from collections import OrderedDict

def solve(data: dict) -> dict:
    cache = OrderedDict()
    results = []
    for op in data["ops"]:
        key = op["key"]
        if op["op"] == "put":
            cache[key] = op["value"]
            cache.move_to_end(key)
            evicted = None
            if len(cache) > data["capacity"]:
                evicted, _ = cache.popitem(last=False)
            results.append(evicted)
        elif op["op"] == "get":
            if key in cache:
                results.append(cache[key])
                cache.move_to_end(key)
            else:
                results.append(None)
        else:
            results.append(key in cache)
            cache.pop(key, None)
    return {"results": results, "entries": [[key, value] for key, value in cache.items()]}

# Supplied CoJudge adapter. Implement solve(data) above.
import json

class Solution:
    def run(self, payload: str) -> str:
        return json.dumps(solve(json.loads(payload)), ensure_ascii=True, allow_nan=False)
