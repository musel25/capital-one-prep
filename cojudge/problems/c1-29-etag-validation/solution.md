## Approach

Track current version and body. Each GET compares the current strong tag with the supplied validators after weak-prefix normalization. For q requests and k tags per GET, time is O(qk), with O(q) output space. A production cache also needs freshness policy, Vary handling, and correct merging of validation metadata.

## Python implementation

```python
def solve(data):
    version, body = data["initial"]["version"], data["initial"]["body"]
    out = []
    for request in data["requests"]:
        if request["op"] == "put":
            version += 1
            body = request["body"]
            out.append({"status": 200, "etag": f'"v{version}"', "body": body})
            continue
        etag = f'"v{version}"'
        tags = request["tags"]
        matches = tags is not None and any(tag == "*" or (tag[2:] if tag.startswith("W/") else tag) == etag for tag in tags)
        out.append({"status": 304 if matches else 200, "etag": etag, "body": None if matches else body})
    return out

# Supplied CoJudge adapter. Implement solve(data) above.
import json

class Solution:
    def run(self, payload: str) -> str:
        return json.dumps(solve(json.loads(payload)), ensure_ascii=True, allow_nan=False)

```
