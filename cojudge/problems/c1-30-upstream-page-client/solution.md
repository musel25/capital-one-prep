## Approach

A cursor set prevents repeated fetches and an id set preserves the first item for each id. The explicit cap bounds work even without a cycle. Expected time is O(p+i), where p is requested pages and i is items inspected. Extra space is O(p+i). Real clients must add transport errors, response validation, deadlines, and a suitable retry policy.

## Python implementation

```python
def solve(data):
    cursor = data["start"]
    seen_cursors = set()
    seen_ids = set()
    requests = []
    items = []
    error = None
    while cursor is not None:
        if cursor in seen_cursors:
            error = "cycle"
            break
        if len(requests) >= data["max_pages"]:
            error = "limit"
            break
        seen_cursors.add(cursor)
        requests.append(cursor)
        page = data["pages"].get(cursor)
        if page is None:
            error = "missing"
            break
        if page["status"] != 200:
            error = "upstream"
            break
        for item in page["items"]:
            if item["id"] not in seen_ids:
                seen_ids.add(item["id"])
                items.append(dict(item))
        cursor = page["next"]
    return {"items": items, "requests": requests, "error": error}

# Supplied CoJudge adapter. Implement solve(data) above.
import json

class Solution:
    def run(self, payload: str) -> str:
        return json.dumps(solve(json.loads(payload)), ensure_ascii=True, allow_nan=False)

```
